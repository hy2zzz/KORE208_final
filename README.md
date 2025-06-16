# 연령대별 형태소 사용 차이를 통한 연령대 분류 모델 학습

## 개요
구어 텍스트를 대상으로 연령대별 사용하는 형태소의 차이를 비교해보고, 연령대를 추측할 수 있는 모델을 학습시키고자 함.

## 구성

1. 데이터 수집
2. 형태소 분석 및 빈도 분석
3. 텍스트 벡터화 및 모델 학습
4. 모델 평가

### 1. 데이터 수집
- 대상 코퍼스: 국립국어원 2024 일상 언어 말뭉치
- 전체 코퍼스에서 다음 조건을 만족하는 데이터 선별
  * 같은 연령대간의 2인 발화: 연령대별 특징 파악 용이
  * 일상적 주제 6가지에서 각 4개씩 선정 = 연령대별로 24개의 파일 선정 (총 144개 파일, 288명의 화자)
    - 여행/휴가/휴일/자연휴양지
    - 반려동물/반려용품
    - 우정/성격/MBTI
    - 연애/결혼/가족/관혼상제
    - 생활/주거환경
    - 회사/학교/학창시절

### 2. 형태소 분석 및 빈도 분석
- 형태소 분석기: kiwi, kkma 사용 (목적: 형태소 분석기별 모델 성능 차이 비교)
- 분석기 선택 이유: kiwi - 이전 과제에서 가장 좋은 성능을 보임  kkma - 조사, 어미 유형 세부 분류
- 빈도 분석: 한 품사 카테고리 내에서의 상대빈도 분석 (목적: 연령에 따라 유의미한 차이가 있는 품사 또는 형태소 파악)

### 3. 텍스트 벡터화 및 모델 학습
- 모델 학습 목적: 구어 텍스트의 발화자 연령대를 추측
- 텍스트 벡터화: 조사(주격조사, 보조사, 목적격조사, 관형격조사), 어미(종결어미, 연결어미, 명사형전성어미, 관형형전성어미), 명사(의존명사, 일반명사, 수사, 대명사), 용언(동사, 형용사, 보조용언) 기준, 형태소별 상대빈도 벡터 생성
- 사용 모델: logistic regression
- 모델 선정 이유: 데이터의 양이 비교적 적고 연령대 라벨이 이미 존재하므로, 지도&비딥러닝의 로지스틱 회귀 모델을 선택
- 모델 학습: 상대빈도 벡터로 학습, kiwi와 kkma의 결과 비교 (형태소 분석기별 모델 학습 성능 비교)

### 4. 모델 평가
- 모델 평가 결과 해석: hold-out(학습-평가), k-fold, 혼동행렬(시각화)
- 연령대 예측해보기
  
## 폴더 구조

```bash
KORE208_FINAL/
├── NIKL_DIALOGUE_00s        # 분석할 데이터가 들어 있는 폴더
├── morpheme_analysis/       # 형태소 분석
│   ├── analyze_morphemes.py
│   ├── results
│   │   ├── results/형태소빈도_00대_kiwi.csv
│   │   ├── results/형태소빈도_00대_kkma.csv
│   │   ├── 형태소빈도_kiwi(합본)
│   │   └── 형태소빈도_kkma(합본)
│   ├── filefiltering.py
│   └── readme_morphs.md
├── morpheme_freq/           # 빈도 분석
│   ├── interjection/
│   ├── results_freq/
│   ├── statistics/
│   └── frequency_top10.py
├── model_train/            # 모델 학습 및 평가
│   ├── morph_vectors_data(kiwi)/     
│   │   ├── 00대_형태소_벡터/
│   │   │   └── SDRW..._형태소벡터.csv
│   │   └── data_for_model_kiwi.py
│   ├── morph_vectors_data(kkma)/     
│   ├── morph_vectors_edit(kiwi)/    
│   ├── morph_vectors_edit(kkma)/
│   ├── predict_vectors(kiwi)/       
│   ├── predict_vectors(kkma)/        
│   ├── predict_원본파일/               
│   │   └── SDRW...(00대).json
│   ├── results/                      
│   ├── TF_MORPHEMES_KIWI/            
│   ├── 1-1data_for_model_kiwi(수정).py   
│   ├── 1-2data_for_model_kkma(수정).py
│   ├── 2-1train.py                  
│   ├── 2-2train_kfold.py           
│   ├── 3predict.py                 
│   ├── compare_analyzer.py          
│   └── readme_train.md
│   ├── README.md
│   └── requirements.txt
...
```

## Git 및 브랜치 사용법
1) 원격 저장소 불러오기: git clone https://github.com/hy2zzz/KORE208_final.git
2) 개발 환경 재현: 가상환경 활성화 후 pip install -r requirements.txt
3) 브랜치 생성: git checkout -b 브랜치명 (예: morphs-20s)
4) "NIKL_DIALOGUE_00s" 폴더에 선별한 파일을 이동시킨 후 분석할 연령대에 맞게 폴더명 변경 (예: "NIKL_DIALOGUE_20s")
5) "analyze_morpheme" 코드의 corpus_dir = "NIKL_DIALOGUE_00s" 부분의 폴더명도 변경
6) 코드 실행 후, 원본 말뭉치 파일과 결과(엑셀) 파일 add (예: git add morpheme_analysis/NIKL_DIALOGUE_20s/) ※ 코드 파일에 추가 및 변경 사항이 있을 경우 코드용 브랜치를 따로 만들어 주세요!
7) 커밋(변경사항 저장): git commit -m "커밋메시지"
8) github에 업로드: git push origin 브랜치명
9) Pull Request: 브랜치의 내용을 main에 합치기
