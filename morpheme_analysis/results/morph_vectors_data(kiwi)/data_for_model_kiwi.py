#%%
#%%
import json
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter
import os

# 폴더 및 형태소 설정
input_folder = r"C:\Users\mysjh\Documents\corpus\kore_final\original_files_to_analyze\NIKL_DIALOGUE_60s\NIKL_DIALOGUE_60s"
output_folder = r"C:\Users\mysjh\Documents\corpus\results\morph_vectors_only"
target_pos = {
    "JKS", "JX", "JKO", "JKG",         # 조사
    "EF", "EC", "ETN", "ETM",          # 어미
    "NNB", "NNG", "NP", "NR"           # 의존명사, 일반명사, 수사, 대명사
    "VX",                              # 보조용언
    "VV", "VA"                         # 동사, 형용사
}

# 분석기 초기화

# 발화 불러오기
def load_utterances(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    utterances = []
    for doc in data["document"]:
        speakers = {s["id"]: s["age"] for s in doc["metadata"]["speaker"]}
        for u in doc["utterance"]:
            sid = u["speaker_id"]
            age = speakers.get(sid, "미상")
            utterances.append({
                "화자ID": sid,
                "연령대": age,
                "문장": u["form"]
            })
    return pd.DataFrame(utterances)

# 형태소 분석 및 상대빈도 계산
def extract_morphs(text):
    result = kiwi.analyze(text)[0][0]
    print("🧪 분석 결과 예시:", result[:5])
    return [m[0] for m in result if m[1] in target_pos]

def build_morph_vectors(df):
    counts = {}
    for row in df.itertuples():
        morphs = extract_morphs(row.문장)
        sid = row.화자ID
        if sid not in counts:
            counts[sid] = Counter()
        counts[sid].update(morphs)

    rows = []
    for sid, counter in counts.items():
        total = sum(counter.values())
        vec = {f"형태소_{k}": v / total for k, v in counter.items()}
        vec["화자ID"] = sid
        rows.append(vec)
    return pd.DataFrame(rows).fillna(0)

# 병합 및 저장
def merge_and_save(json_path, output_csv):
    utterance_df = load_utterances(json_path)
    morph_df = build_morph_vectors(utterance_df)
    
    # 연령대 정보
    meta_df = utterance_df.groupby("화자ID").agg({
        "연령대": "first"
    }).reset_index()

    merged = pd.merge(meta_df, morph_df, on="화자ID", how="left")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    merged.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {output_csv}")

# 폴더 내 반복
def process_all_json(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(input_folder, filename)
            output_csv = os.path.join(output_folder, filename.replace(".json", "_형태소벡터.csv"))
            merge_and_save(json_path, output_csv)

# 실행
process_all_json(input_folder, output_folder)
