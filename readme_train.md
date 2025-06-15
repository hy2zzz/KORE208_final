# 모델 학습 및 평가
1. 텍스트 벡터화
2. 모델 학습 및 평가
3. 연령대 예측

## 폴더 구조
```bash
model_train/
├── morph_vectors_data(kiwi)/     # 수정 전 형태소 벡터 및 코드
├── morph_vectors_data(kkma)/     
├── morph_vectors_edit(kiwi)/     # 수정 후 형태소 벡터
├── morph_vectors_edit(kkma)/
├── predict_vectors(kiwi)/        # 예측용 형태소 벡터 및 코드
├── predict_vectors(kkma)/        
├── predict_원본파일/              # 예측에 사용한 원본 json 파일    
├── results/                      # 결과를 모아둔 폴더
├── 1-1data_for_model_kiwi(수정).py   # 수정된 벡터화 코드 (결과: morph_vectors_edit)
├── 1-2data_for_model_kkma(수정).py
├── 2-1train.py                   # 모델 학습 및 평가 코드: 학습-평가(hold-out) 방식 + 혼동행렬 시각화
├── 2-2train_kfold.py             # 모델 학습 및 평가 코드: k-fold 방식
├── 3predict.py                    # train_kfold.py + 모델 예측 코드
├── compare_analyzer.py           # 형태소 분석기 비교용 코드
...
```

## 결과

1. 텍스트 벡터화
- 기존 형태소 벡터(data폴더)와 수정된 형태소 벡터(edit폴더) 간 차이가 거의 없음 → 둘 중 하나만 다루는 것도 고려
2. 모델 학습 및 평가
- 평가 방식에 따른 결과 차이
- 혼동행렬(hold-out방식): 행-실제값, 열-예측값, 대각선-예측이 정확하게 맞음
3. 예측
- 학습 데이터 선정 조건(6개의 주제+2인 발화)에 부합하는 발화 파일 6개 (학습 및 평가에 사용되지 않은 파일)
- kiwi와 kkma 모두 완벽하게 정확하진 않지만, 대략적인 연령대를 구분할 수 있다고 판단됨
- kkma가 kiwi보다 오류가 많았고(지난 과제), 형태소를 잘게 분석하는 경향이 있어(compare_analyzer.py결과, results파일 참고) 과적합 등으로 인해 성능이 떨어질 것으로 예상했으나, 예측 결과 큰 차이가 없었고 오히려 더 정확히 연령대를 예측하기도 함.
