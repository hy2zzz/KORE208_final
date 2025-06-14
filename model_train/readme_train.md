# 모델 학습 및 평가
## 폴더 구조
- morph_vectors_data(kiwi)/  # 기존 형태소 벡터 파일 및 코드
- morph_vectors_data(kkma)/  # 기존 형태소 벡터 파일 및 코드
- morph_vectors_edit(kiwi)/  # 의존명사, 수사, 대명사 삭제 & 관형사, 부사 추가(목적: 간투사 추가)한 형태소 벡터(수정)
- data_for_model_kiwi(수정).py # 형태소 벡터(수정)을 위한 코드 (kkma 추후 업로드 예정)
- train.py # 학습-평가(8:2) 방식을 사용한 코드
- train_kfold.py # 교차검증(5-fold)방식을 사용한 코드

※
- 두 코드 모두 "model_train"의 하위 디렉토리 내에 "morph_Vectors_(data 또는 edit)((kiwi/kkma))" 폴더가 존재함을 가정
- 사용시 base_dir, print('교차 검증:') 부분을 폴더명과 일치하도록 적절히 수정 필요

## 결과

| 형태소 벡터 | 검증 방식 | 형태소 분석기 | 결과 |
|---|---|---|---|
| data | 8:2 | kiwi | f1 0.76 |
| data | 8:2 | kkma | f1 0.83 |
| edit | 8:2 | kiwi | f1 0.79 |
| data | 5-fold | kiwi | 0.3751 / 0.0625 (평균 / 표준편차) |
| data | 5-fold | kkma | 0.3299 / 0.0409 |
| edit | 5-fold | kiwi | 0.3821 / 0.0550 |
