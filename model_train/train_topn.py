# %%
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

def load_data_from_folders(base_dir):
    X_all = []
    y_all = []

    for age_folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, age_folder)
        if not os.path.isdir(folder_path):
            continue

        # 폴더명 예: '10대_형태소_벡터' → '10대'
        age_label = age_folder.split('_')[0]

        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)

                # NaN 값 0으로 대체
                df = df.fillna(0)

                # 특성만 추출 (연령대나 발화번호 열 제거)
                X = df.drop(columns=['연령대', '화자ID'], errors='ignore')

                # 레이블 수만큼 age_label 복제
                y = [age_label] * len(X)

                X_all.append(X)
                y_all.extend(y)

    # 하나의 DataFrame과 Series로 결합
    X_all = pd.concat(X_all, ignore_index=True)

    return X_all, y_all

# 상위 n개만 추출
def select_top_n_features_by_pos(X, top_n=5):
    from collections import defaultdict
    pos_dict = defaultdict(list)

    for col in X.columns:
        if '_' in col:
            pos = col.split('_', 1)[0]
            total_freq = X[col].sum()
            pos_dict[pos].append((col, total_freq))

    selected_columns = []
    for pos, items in pos_dict.items():
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        top_items = sorted_items[:top_n]
        selected_columns.extend([col for col, _ in top_items])

    return X[selected_columns]


# 메인 실행
if __name__ == '__main__':
    base_dir = './morph_vectors_topn(kiwi)'  # 예시: '10대_형태소_벡터' 폴더들이 있는 상위 디렉토리

    # 1. 데이터 불러오기
    X, y = load_data_from_folders(base_dir)

    # NaN을 0으로 채움
    X = X.fillna(0)

    # 품사별 상대빈도 상위 N개만 선택
    X = select_top_n_features_by_pos(X, top_n=10)  # top_n은 원하는 값으로 조정


    # 2. 정규화
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. 모델 정의
    model = LogisticRegression(max_iter=1000)

    # 4. 교차검증 수행 (예: 5-fold)
    scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')

    # 5. 결과 출력
    print(f'교차검증 정확도: {scores}')
    print(f'평균 정확도: {np.mean(scores):.4f}, 표준편차: {np.std(scores):.4f}')

print(f"전체 샘플 수: {len(X)}")