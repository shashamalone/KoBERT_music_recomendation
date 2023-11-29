
###################
#####  MODEL  #####
###################

#----------- 모델 환경 설정 ---------------------------------------
# # 모델 돌리기 위한 install
# pip install mxnet
# pip install gluonnlp==0.8.0
# pip install pandas tqdm
# pip install sentencepiece
# pip install transformers
# pip install torch


## 깃허브에서 KoBERT 파일 로드
# pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'


# 모델 돌리는데 필요 import
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from sklearn.model_selection import train_test_split


# pre-trained model 가져오기
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')



# BERTSentenceTransform 클래스 정의  

class BERTSentenceTransform:
    r"""BERT style data transformation.

    Parameters
    ----------
    tokenizer : BERTTokenizer.
        Tokenizer for the sentences.
    max_seq_length : int.
        Maximum sequence length of the sentences.
    pad : bool, default True
        Whether to pad the sentences to maximum length.
    pair : bool, default True
        Whether to transform sentences or sentence pairs.
    """

    def __init__(self, tokenizer, max_seq_length,vocab, pad=True, pair=True):
        self._tokenizer = tokenizer
        self._max_seq_length = max_seq_length
        self._pad = pad
        self._pair = pair
        self._vocab = vocab

    def __call__(self, line):
        """Perform transformation for sequence pairs or single sequences.

        The transformation is processed in the following steps:
        - tokenize the input sequences
        - insert [CLS], [SEP] as necessary
        - generate type ids to indicate whether a token belongs to the first
        sequence or the second sequence.
        - generate valid length

        For sequence pairs, the input is a tuple of 2 strings:
        text_a, text_b.

        Inputs:
            text_a: 'is this jacksonville ?'
            text_b: 'no it is not'
        Tokenization:
            text_a: 'is this jack ##son ##ville ?'
            text_b: 'no it is not .'
        Processed:
            tokens: '[CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]'
            type_ids: 0     0  0    0    0     0       0 0     1  1  1  1   1 1
            valid_length: 14

        For single sequences, the input is a tuple of single string:
        text_a.

        Inputs:
            text_a: 'the dog is hairy .'
        Tokenization:
            text_a: 'the dog is hairy .'
        Processed:
            text_a: '[CLS] the dog is hairy . [SEP]'
            type_ids: 0     0   0   0  0     0 0
            valid_length: 7

        Parameters
        ----------
        line: tuple of str
            Input strings. For sequence pairs, the input is a tuple of 2 strings:
            (text_a, text_b). For single sequences, the input is a tuple of single
            string: (text_a,).

        Returns
        -------
        np.array: input token ids in 'int32', shape (batch_size, seq_length)
        np.array: valid length in 'int32', shape (batch_size,)
        np.array: input token type ids in 'int32', shape (batch_size, seq_length)

        """

        # convert to unicode
        text_a = line[0]
        if self._pair:
            assert len(line) == 2
            text_b = line[1]

        tokens_a = self._tokenizer.tokenize(text_a)
        tokens_b = None

        if self._pair:
            tokens_b = self._tokenizer(text_b)

        if tokens_b:
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            self._truncate_seq_pair(tokens_a, tokens_b,
                                    self._max_seq_length - 3)
        else:
            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > self._max_seq_length - 2:
                tokens_a = tokens_a[0:(self._max_seq_length - 2)]

        # The embedding vectors for `type=0` and `type=1` were learned during
        # pre-training and are added to the wordpiece embedding vector
        # (and position vector). This is not *strictly* necessary since
        # the [SEP] token unambiguously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.

        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        #vocab = self._tokenizer.vocab
        vocab = self._vocab
        tokens = []
        tokens.append(vocab.cls_token)
        tokens.extend(tokens_a)
        tokens.append(vocab.sep_token)
        segment_ids = [0] * len(tokens)

        if tokens_b:
            tokens.extend(tokens_b)
            tokens.append(vocab.sep_token)
            segment_ids.extend([1] * (len(tokens) - len(segment_ids)))

        input_ids = self._tokenizer.convert_tokens_to_ids(tokens)

        # The valid length of sentences. Only real  tokens are attended to.
        valid_length = len(input_ids)

        if self._pad:
            # Zero-pad up to the sequence length.
            padding_length = self._max_seq_length - valid_length
            # use padding tokens for the rest
            input_ids.extend([vocab[vocab.padding_token]] * padding_length)
            segment_ids.extend([0] * padding_length)

        return np.array(input_ids, dtype='int32'), np.array(valid_length, dtype='int32'),\
            np.array(segment_ids, dtype='int32')





# BERTDataset 클래스 생성      
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len,
                 pad, pair):
        transform = BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len,vocab=vocab, pad=pad, pair=pair)
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))



## 파라미터 설정
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 2
max_grad_norm = 1
log_interval = 200
learning_rate =  3e-5


#device - GPU 설정
device = torch.device("cuda:0")

# 모델 불러오는 경로
model_state_dict_path = '/content/drive/MyDrive/model/model_state_dict.pt'

# BERTClassifier 클래스 정의
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=7,
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


# 모델 생성 및 불러오기
model = BERTClassifier(bertmodel, hidden_size=768, num_classes=7, dr_rate=0.5).to(device)
model.load_state_dict(torch.load(model_state_dict_path))


# 예측함수
def predict(predict_sentence):

    data = [predict_sentence, '0']
    dataset_another = [data]

    # another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False) #벨로그 원래
    another_test = BERTDataset(dataset_another, 0, 1, tokenizer, vocab, max_len, True, False)
    all_test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)


    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(all_test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length= valid_length
        label = label.long().to(device)

    out = model(token_ids, valid_length, segment_ids)

    ## 감정반환 : 행복, 놀람, 분노, 공포, 혐오, 슬픔, 중립
    test_eval=[]
    for i in out:
        logits=i
        logits = logits.detach().cpu().numpy()

        if np.argmax(logits) == 0:
            test_eval.append("행복")
        elif np.argmax(logits) == 1:
            test_eval.append("놀람")
        elif np.argmax(logits) == 2:
            test_eval.append("분노")
        elif np.argmax(logits) == 3:
            test_eval.append("공포")
        elif np.argmax(logits) == 4:
            test_eval.append("혐오")
        elif np.argmax(logits) == 5:
            test_eval.append("슬픔")
        elif np.argmax(logits) == 6:
            test_eval.append("중립")

    return test_eval[0]


###########################################
##### 일기인식 후 노래추천하는 함수   #####
###########################################

# 함수 사용하는데 필요한 import
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# songs_data.csv 파일을 읽어온다. 파일 경로는 실제 데이터 위치에 맞게 수정
# songs_data = pd.read_csv('songs_data.csv') # title, genre, singer, img를 컬럼으로 가지는 csv형태의 파일

# 입력한 텍스트를 벡터화하는 함수
def vectorize_text(text, vectorizer):
    # 입력된 텍스트를 벡터화
    text_vector = vectorizer.transform([text])
    return text_vector



# 입력한 텍스트의 감정을 인식하고 노래를 추천하는 함수
def find_similar_songs(user_text, songs_data, top_n=3):

    # 1차 필터링
    # 입력된 일기의 감정을 인식하고 해당하는 감정에 맞는 음악리스트 불러오기 
    emotion = predict(user_text) #주의!!!!!모델(user_text)을 넣어야함
    songs_emotion_data = songs_data[songs_data['category'] == emotion]

    # 2차 코사인 유사도 기반 추천
    # TF-IDF 벡터화를 사용하는 예시
    vectorizer = TfidfVectorizer()
    
    # 가사 데이터를 벡터화
    lyrics_vector = vectorizer.fit_transform(songs_emotion_data['lyrics'].astype(str))

    # 사용자 입력 문장을 벡터화
    user_vector = vectorize_text(user_text, vectorizer)

    # 코사인 유사도 계산
    similarity_scores = cosine_similarity(user_vector, lyrics_vector).flatten()

    # 상위 n개의 곡 추출
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    # 상위 곡의 정보 출력
    top_songs_info = []
    for index in top_indices:
        song_info = {
            "title": songs_emotion_data.iloc[index]['title'],
            "singer": songs_emotion_data.iloc[index]['singer'],
            "img": songs_emotion_data.iloc[index]['img']
        }
        top_songs_info.append(song_info)

    return top_songs_info
