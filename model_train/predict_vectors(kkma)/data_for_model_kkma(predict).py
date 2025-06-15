#%% 기존 "data_for_model_kkma(수정)"에서 파일 경로만 변경
import json, os
import pandas as pd
from konlpy.tag import Kkma
from collections import Counter

# 사용할 품사 태그
target_pos = {
    "JKS", "JX", "JKO", "JKG",
    "EFN", "EFQ", "EFO", "EFA", "EFI", "EFR",
    "ECS", "ECD", "ECE", "ETN", "ETD",
    "NNG",  # 의존명사, 수사, 대명사 삭제
    "VXA", "VXV", "VA", "VV",
    "MDN", "MDT", "MAG", "MAC"  # 관형사, 부사 추가
}

kkma = Kkma()

# JSON 파일에서 발화 데이터 추출
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

# 형태소 분석 + 필터링
def extract_morphs(text):
    try:
        morphs = kkma.pos(text)
        return [(m[0], m[1]) for m in morphs if m[1] in target_pos]
    except Exception as e:
        print("분석 오류:", e)
        return []

# 형태소 빈도 벡터 생성
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

# JSON → 벡터 CSV 변환
def merge_and_save(json_path, output_csv):
    utter_df = load_utterances(json_path)
    morph_df = build_vectors(utter_df)
    meta_df = utter_df.groupby("화자ID")["연령대"].first().reset_index()
    merged = pd.merge(meta_df, morph_df, on="화자ID", how="left")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    merged.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print("저장 완료:", output_csv)

# 폴더 순회 및 전체 처리
def process_folders(base_dir, output_base):
    os.makedirs(output_base, exist_ok=True)

    for root, dirs, files in os.walk(base_dir):
        relative_path = os.path.relpath(root, base_dir)
        out_dir = os.path.join(output_base, relative_path)
        os.makedirs(out_dir, exist_ok=True)

        for filename in files:
            if filename.endswith(".json"):
                json_path = os.path.join(root, filename)
                base_name = os.path.splitext(filename)[0]
                output_csv = os.path.join(out_dir, f"{base_name}_형태소벡터.csv")
                merge_and_save(json_path, output_csv)

# 실행
if __name__ == "__main__":
    base_dir = "../predict_원본파일"
    output_dir = "../predict_vectors(kkma)"
    process_folders(base_dir, output_dir)

# %%
