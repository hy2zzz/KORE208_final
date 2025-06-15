# 모델 학습 및 평가
1. 텍스트 벡터화
2. 모델 학습 및 평가
3. 연령대 예측

## 폴더 구조
```bash
model_train/
├── morph_vectors_data(kiwi)/     # 수정 전 형태소 벡터
├── morph_vectors_data(kkma)/     
├── morph_vectors_edit(kiwi)/     # 수정 후 형태소 벡터
├── morph_vectors_edit(kkma)/
├── predict_vectors(kiwi)/        # 예측용 형태소 벡터
├── predict_vectors(kkma)/        
├── predict_원본파일/              # 예측에 사용한 원본 json 파일    
├── results/                      # 결과를 모아둔 폴더
├── 1-1data_for_model_kiwi(수정).py   # 수정된 벡터화 코드
├── 1-2data_for_model_kkma(수정).py
├── 2-1train.py                   # 모델 학습 및 평가 코드: 학습-평가(hold-out) 방식 
├── 2-2train_kfold.py             # 모델 학습 및 평가 코드: k-fold 방식
├── 3predict.py                    # train_kfold.py + 모델 예측 코드
├── compare_analyzer.py           # 형태소 분석기 비교용 코드
...
```

## 결과

| 형태소 벡터 | 검증 방식 | 형태소 분석기 | 결과 |
|---|---|---|---|
| data | 8:2 | kiwi | f1 0.76 |
| data | 8:2 | kkma | f1 0.83 |
| edit | 8:2 | kiwi | f1 0.79 |
| data | 5-fold | kiwi | 0.3751 / 0.0625 (평균 / 표준편차) |
| data | 5-fold | kkma | 0.3299 / 0.0409 |
| edit | 5-fold | kiwi | 0.3821 / 0.0550 |
