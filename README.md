# 오늘 나의 기분에 맞는 BGM은? (Web Scraping & KoBERT)

KoBERT모델 기반의 Text(예: 일기)에 어울리는 노래 추천 프로젝트

## 🏆 Project Introduction
 1. 엔코아 데이터 애널리시스 33기 mini project
 2. 주제: 일기, 다이어리의 글을 입력하면 감정을 분석해 어울리는 음악 추천
 3. 팀원: 김이정, 김나린, 박지우, 최형규

### 프로젝트 구조도
![슬라이드10](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/b579e600-dbeb-4990-a2df-953d3004df53)
![슬라이드34](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/b889b58a-f20c-4195-8814-096f47c66942)


### ⭐ streamlit 시연 화면
![image](https://github.com/shashamalone/KoBERT_music_recomendation/assets/133465838/09cc71c4-ac1f-4a9d-83d3-fbfa728c387c)

사용자가 자신의 일기데이터를 입력하면, ReUmi 모델이 음악을 추천

    
   

## 📖 Research and Analysis




## 📝 Data Pre-processing

모델에 넣기 위해서 Data pre-processing은 아래의 3단계의 순서로 진행하였다.


## 🏆 Modeling

### KoBERT Model
KoBERT Model은 SKT-Brain에서 개발한 한국어 기반  BERT 모델.
한국어는 다른 언어에 비해 한 단어에 의미가 많아 한국어만을 학습한 모델 필요해 BERT 모델을 한국어에 적용한 모델을 사용
BERT모델은 현존하는 가장 강력한 NLP 언어모델. 언어모델 전이학습 컨셉을 적용한 모델 





## 🏆 Data

< KoBERT 모델 input : 한국어 말뭉치 데이터 >


< Melon Crawling데이터를 학습된 최종 KoBERT 모 >


## 💻 Code
< Meloncralewer.ipypb >

< MusicRecommend.py >





    
