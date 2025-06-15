# %%
import os
import pandas as pd

def analyze_morph_vector_data(root_dir):
    total_morphs = set()
    total_dims_per_speaker = []

    for age_dir in os.listdir(root_dir):
        age_path = os.path.join(root_dir, age_dir)
        if not os.path.isdir(age_path):
            continue

        for fname in os.listdir(age_path):
            if not fname.endswith(".csv"):
                continue
            file_path = os.path.join(age_path, fname)
            df = pd.read_csv(file_path)

            # 형태소 열만 선택
            morph_df = df.select_dtypes(include="number").drop(
                columns=["화자ID", "연령대"], errors="ignore"
            )

            # 전체 형태소 종류 저장
            total_morphs.update(morph_df.columns)

            # 화자 한 명당 벡터 차원 수 계산
            total_dims_per_speaker.extend((row != 0).sum() for _, row in morph_df.iterrows())

    return {
        "전체 형태소 종류 수": len(total_morphs),
        "화자당 평균 벡터 차원 수": round(sum(total_dims_per_speaker) / len(total_dims_per_speaker), 2)
        if total_dims_per_speaker else 0
    }

# 경로 설정
kiwi_root = "./morph_vectors_data(kiwi)"
kkma_root = "./morph_vectors_data(kkma)"

kiwi_stats = analyze_morph_vector_data(kiwi_root)
kkma_stats = analyze_morph_vector_data(kkma_root)

# 결과 출력
print("\n Kiwi 분석기 결과")
for k, v in kiwi_stats.items():
    print(f"   {k}: {v}")

print("\n Kkma 분석기 결과")
for k, v in kkma_stats.items():
    print(f"   {k}: {v}")