#%%
import json, os
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter

target_pos = {
    "JKS", "JX", "JKO", "JKG",
    "EF", "EC", "ETN", "ETM",
    "NNG", "VX", "VV", "VA", # 의존명사, 수사, 대명사 삭제
    "MAG", "MAJ", "MM" # 관형사, 부사 추가 (간투사 분석 목적)
}

kiwi = Kiwi()

def load_utterances(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    utterances = []
    for doc in data["document"]:
        speakers = {s["id"]: s["age"] for s in doc["metadata"]["speaker"]}
        for u in doc["utterance"]:
            sid = u["speaker_id"]
            utterances.append({
                "화자ID": sid,
                "연령대": speakers.get(sid, "미상"),
                "문장": u["form"]
            })
    return pd.DataFrame(utterances)

def extract_morphs(text):
    return [(m[0], m[1]) for m in kiwi.analyze(text)[0][0] if m[1] in target_pos]

def build_vectors(df):
    counters = {}
    for row in df.itertuples():
        morphs = extract_morphs(row.문장)
        sid = row.화자ID
        counters.setdefault(sid, Counter()).update(f"{pos}_{form}" for form, pos in morphs)
    
    rows = []
    for sid, counter in counters.items():
        total = sum(counter.values())
        vec = {"화자ID": sid}
        vec.update({k: v / total for k, v in counter.items()})
        rows.append(vec)

    return pd.DataFrame(rows).fillna(0)

def merge_and_save(json_path, output_csv):
    utter_df = load_utterances(json_path)
    morph_df = build_vectors(utter_df)
    meta_df = utter_df.groupby("화자ID")["연령대"].first().reset_index()
    merged = pd.merge(meta_df, morph_df, on="화자ID", how="left")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    merged.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print("저장 완료:", output_csv)

def process_folders(base_dir, output_base):
    for age_folder in os.listdir(base_dir):
        age_path = os.path.join(base_dir, age_folder)
        if not os.path.isdir(age_path): continue

        out_dir = os.path.join(output_base, f"{age_folder}_형태소_벡터")
        os.makedirs(out_dir, exist_ok=True)

        for filename in os.listdir(age_path):
            if filename.endswith(".json"):
                json_path = os.path.join(age_path, filename)
                base_name = os.path.splitext(filename)[0]
                output_csv = os.path.join(out_dir, f"{base_name}_형태소벡터.csv")
                merge_and_save(json_path, output_csv)

if __name__ == "__main__":
    base_dir = os.path.join("..", "NIKL_DIALOGUE")
    output_dir = "morph_vectors_edit(kiwi)"
    process_folders(base_dir, output_dir)

# %%
