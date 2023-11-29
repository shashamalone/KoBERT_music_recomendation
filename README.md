# 오늘 나의 기분에 맞는 BGM은? (Web Scraping & KoBERT)

KoBERT모델 기반의 Text(예: 일기)에 어울리는 노래 추천 프로젝트

## 🏆 Project Introduction
 2. 주제: 일기, 다이어리의 글을 입력하면 감정을 분석해 어울리는 음악 추천
 3. 팀원: 김이정(PM, Developer), 김나린(Front-End, Developer), 박지우(Developer), 최형규(Dveloper)
 4. 프로젝트 기간 : : 11/13(금) ~ 11/28(화)

### 프로젝트 구조도
![슬라이드10](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/b579e600-dbeb-4990-a2df-953d3004df53)
![슬라이드34](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/b889b58a-f20c-4195-8814-096f47c66942)


### ⭐ streamlit 시연 화면
![image](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/09cc71c4-ac1f-4a9d-83d3-fbfa728c387c)

사용자가 자신의 일기데이터를 입력하면, ReUmi 모델이 음악을 추천

    
   

## 📖 Research and Analysis
사람들은 가사를 통해 기분 전환을 하며, 노래 감상 시에 가사를 고려한다. 또한 SNS에서 자신의 감정을 담은 글들을 공유한다. 이러한 일상의 감정들에 어울리는 노래를 추천하는 서비스를 구현하고자 ReUMI모델을 만들게 되었다. 기존의 노래 플랫폼 멜론 , 지니 , 유튜브 등 에서 추천하는 노래들은 사용자의 선호 알고리즘 에 의한 추천일 뿐 , 사용자의 현재 감정에 초점을 맞추는 형태는 아니였기에 "감정"을 읽는 프로젝트 'Read Your Mind'를 주제로 정하였다.




## 📝 Crawling

사용자에게 추천해주기 위한 장르별 음악을 Melon에서 Selenium을 활용해 크롤링하였다.
- 스테디셀러 50개, 인기곡 50개를 장르별로 크롤링
- 노래제목, 가수, 가사,이미지, 좋아요 컬럼으로 정리
- 결과 : Melon_song_data.csv

  
Melon_song_data를 완성된 ReUmi Model에 넣어 감정 categroy결과를 컬럼으로 저장했다.
이는 1차 필터링에서 사용자의 일기에서 느껴지는 감정과 동일한 노래리스트를 뽑는데에 사용하였다.
- 결과 : total_melon_emotion.csv
![image](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/70468ede-a83d-4081-b44d-127ad996cb0a)



## 🏆 Modeling

### KoBERT Model
KoBERT Model은 SKT-Brain에서 개발한 한국어 기반  BERT 모델.

### Model 학습을 위한 Data Sets 구축

KoBERT 모델 학습을 위한 AI HUB의 한국어 데이터
1. 감성 대화 말뭉치 58271 개
2. 한국어 연속성 대화 데이터 셋 55630 개
3. 감정 분류를 위한 음성 데이터 셋 43991 개
- 최종 데이터셋 총 개수 157,862개
- 감정 Label : 행복, 슬픔 , 분노 , 공포 , 혐오 , 놀람 + 중립(7개)
- 모델에 넣기 위해 위의 3개의 파일을 감정 Label 7개에 맞춰 재라벨링을 진행하였다.

### ReUmi Model
ReUmi Model은 한국어 대화 데이터셋 약 15만개를 KoBERT모델에 학습시켜 완성한 최종 모델
![image](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/fcd92187-18fa-4d5a-85de-dcf676b5683b)
- train acc : 0.9154 , val acc : 0.7957
- Setting parameters
num_classes=7   
max_len = 64   
batch_size = 64   
warmup_ratio = 0.1   
num_epochs = 7   
max_grad_norm = 1   
log_interval = 200   
learning_rate =  3e-5   




## 💻 Code
- Meloncralewer.ipypb

< MusicRecommend.py >
- ReadYourMind.pt
- model_state_dict.pt

< streamlit >
- style.css 
- normalize.css 





    
