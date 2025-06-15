# %% 학습-평가(8:2) 방식
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

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

                # 특성만 추출
                X = df.drop(columns=['연령대', '화자ID'], errors='ignore')

                y = [age_label] * len(X)

                X_all.append(X)
                y_all.extend(y)

    # 하나의 DataFrame과 Series로 결합
    X_all = pd.concat(X_all, ignore_index=True)

    return X_all, y_all

# 메인 실행
if __name__ == '__main__':
    base_dir = './morph_vectors_edit(kkma)'  # 벡터 파일이 들어 있는 폴더명 (data 또는 edit / (kiwi) 또는 (kkma))

    # 1. 데이터 불러오기
    X, y = load_data_from_folders(base_dir)

    # NaN을 0으로 채움
    X = X.fillna(0)

    # 2. 정규화
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. 학습-평가 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y, random_state=42
    )

    # 4. 로지스틱 회귀 모델 학습
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # 5. 평가
    y_pred = model.predict(X_test)
    print("학습-평가(8:2): kkma") # kiwi 또는 kkma
    print(classification_report(y_test, y_pred))

print(f"전체 샘플 수: {len(X)}")
print(f"학습 샘플 수: {len(X_train)}")
print(f"테스트 샘플 수: {len(X_test)}")

# 한글 폰트 설정 (Windows에서 보통 'Malgun Gothic' 사용)
plt.rcParams['font.family'] = 'Malgun Gothic'

# 마이너스 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False


# 혼동 행렬 (시각화)
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=model.classes_, yticklabels=model.classes_, cmap="Blues")
plt.xlabel("예측한 연령대")
plt.ylabel("실제 연령대")
plt.title("혼동 행렬 (Confusion Matrix)")
plt.show()

# %%
