#%%
import json
import pandas as pd
from kiwipiepy import Kiwi
from konlpy.tag import Kkma
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# 폴더 및 형태소 설정
input_folder = r"C:\Users\mysjh\Documents\corpus\kore_final\original_files_to_analyze\NIKL_DIALOGUE_60s\NIKL_DIALOGUE_60s"
output_folder = r"C:\Users\mysjh\Documents\corpus\results\TF_MORPHEMES_KIWI\60대_형태소_벡터"
use_tfidf = True
target_pos = {
    "조사", "어미",             # 문법적 요소
    "일반명사",                # 의미 있는 명사 (NNG)
    "보조용언", "보조형용사", "동사", "형용사",  # 용언
    "관형사",                  # 관형사
    "일반부사"				     # 부사
}


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

kiwi = Kiwi()

def extract_morphs(text):
    if not text.strip():
        return []
    result = kiwi.analyze(text)[0][0]
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

# TF-IDF 벡터 계산
def build_tfidf_vectors(df):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df["문장"])
    tfidf_df = pd.DataFrame(tfidf.toarray(), columns=[f"TFIDF_{t}" for t in vectorizer.get_feature_names_out()])
    tfidf_df["화자ID"] = df["화자ID"].values
    return tfidf_df

# 병합 및 저장
def merge_and_save(json_path, output_csv):
    utterance_df = load_utterances(json_path)
    morph_df = build_morph_vectors(utterance_df)
    
    # 메타 정보 병합
    meta_df = utterance_df.groupby("화자ID").agg({
        "연령대": "first",
        "문장": lambda x: " ".join(x)
    }).reset_index()
    
    # 모두 병합
    merged = meta_df.merge(morph_df, on="화자ID", how="left")

    if use_tfidf:
        tfidf_df = build_tfidf_vectors(utterance_df)
        merged = merged.merge(tfidf_df, on="화자ID", how="left")

	#저장
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    merged.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"✅ 저장 완료: {output_csv}")

# 폴더 내 반복
def process_all_json(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            print(f"🔍 처리 중: {filename}")
            json_path = os.path.join(input_folder, filename)
            output_csv = os.path.join(output_folder, filename.replace(".json", "_형태소벡터.csv"))
            merge_and_save(json_path, output_csv)

# 실행
process_all_json(input_folder, output_folder)
