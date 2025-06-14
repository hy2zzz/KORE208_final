# 연령대별 형태소 사용 양상 분석

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
- 빈도 분석: 한 품사 카테고리 내에서의 상대빈도 분석, 연령에 따라 유의미한 차이가 있는 품사 또는 형태소 파악

### 3. 텍스트 벡터화 및 모델 학습
- 모델 학습 목적: 구어 텍스트의 발화자 연령대를 추측
- 텍스트 벡터화: 조사(JKS, JX, JKO, JKG), 어미(EF, EC, ETN, ETM), 명사(NNB, NNG, NP, NR), 용언(VX, VV, VA) 기준, 형태소별 상대빈도 벡터 생성
- 사용 모델: logistic regression
- 모델 선정 이유: 데이터의 양이 비교적 적고 연령대 라벨이 이미 존재하므로, 지도&비딥러닝의 로지스틱 회귀 모델을 선택
  
## 폴더 구조

```bash
KORE208_FINAL/
├── NIKL_DIALOGUE_00s/        # 분석할 데이터가 들어 있는 폴더
├── morpheme_analysis/
│   ├── analyze_morphemes.py      # 분석용 코드
│   ├── results/                  # 분석 결과가 저장되는 폴더
│   │   ├── results/형태소빈도_00대_kiwi.csv
│   │   └── results/형태소빈도_00대_kkma.csv
│   └── readme_morphs.md                # 참고 사항
├── morpheme_freq/
│   ├── frequency_조사어미.py #
│   ├── frequency_간투사.py
│   ├── frequnecy_체언용언.py
│   ├── results/
│   │   ├──
│   └── readme_freq.md
├── model_train/
│   ├── morph_vectors_data(kiwi)/
│   ├── morph_vectors_data(kkma)/
│   ├── morph_vectors_edit(kiwi)/
│   ├── train.py
│   ├── train_kfold.py
│   └── readme_train.md
...
```


