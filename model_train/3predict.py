# %% 모델 학습 및 평가(k-fold), 저장
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import pickle

# 벡터화를 마친 csv 파일 대상

# 하위 폴더 순회, csv파일 찾기
def load_data_from_folders(base_dir):
    X_all = []
    y_all = []

    for age_folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, age_folder)
        if not os.path.isdir(folder_path):
            continue

        age_label = age_folder.split('_')[0]

        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)

                # NaN 문제 해결
                df = df.fillna(0)
                # 형태소 열만 추출
                X = df.drop(columns=['연령대', '화자ID'], errors='ignore')
                y = [age_label] * len(X)

                X_all.append(X)
                y_all.extend(y)

    X_all = pd.concat(X_all, ignore_index=True)
    return X_all, y_all


# 메인 실행
if __name__ == '__main__':
    base_dir = './morph_vectors_data(kiwi)'  # ‼️경로 변경 필요‼️(kiwi/kkma별로 경로를 수정해야 하는 부분)

    # 1. 데이터 불러오기
    X, y = load_data_from_folders(base_dir)
    X = X.fillna(0)

    # 2. 정규화
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. 특성 목록 저장
    with open('features.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)

    # 4. 모델 정의 및 교차검증
    model = LogisticRegression(max_iter=1000)
    scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')

    print("5-fold: kiwi")  # ‼️이름 변경 필요‼️
    print(f'교차검증 정확도: {scores}')
    print(f'평균 정확도: {np.mean(scores):.4f}, 표준편차: {np.std(scores):.4f}')

    # 5. 전체 데이터로 재학습 및 저장
    model.fit(X_scaled, y)

    with open('logistic_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# %% 연령대 예측해보기
import os
import pandas as pd
import pickle

test_dir = './predict_vectors(kiwi)'  # ‼️경로 변경 필요‼️

# 모델, 스케일러, feature 불러오기
with open('logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('features.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# 예측
print("예측 결과(kiwi)") # ‼️이름 변경 필요‼️
for root, dirs, files in os.walk(test_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            print(f"\n 처리 중: {file_path}")

            df = pd.read_csv(file_path)
            df = df.fillna(0)

            # 열 순서 및 누락된 특성 보완
            X_test = df.reindex(columns=feature_names, fill_value=0)

            # 스케일링 및 예측
            X_scaled = scaler.transform(X_test)
            preds = model.predict(X_scaled)

            for i, pred in enumerate(preds):
                speaker_id = df['화자ID'].iloc[i] if '화자ID' in df.columns else f"화자{i}"
                print(f"화자ID: {speaker_id}, 예측된 연령대: {pred}")
# %%
