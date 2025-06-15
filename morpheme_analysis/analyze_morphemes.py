# %%
import os
import json
from collections import Counter, defaultdict
from konlpy.tag import Kkma
from kiwipiepy import Kiwi
import pandas as pd

kkma = Kkma()
kiwi = Kiwi()

# 전체 JSON 불러오기
def load_all_jsons(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                data.extend(json_data.get("document", []))
    return data

# 형태소 분석기
def analyze_morphs(text, analyzer='kiwi'):
    if analyzer == 'kiwi':
        return [(token.form, token.tag) for token in kiwi.tokenize(text)]
    elif analyzer == 'kkma':
        return kkma.pos(text)
    else:
        raise ValueError("지원되지 않는 분석기: 'kiwi' 또는 'kkma'")

# 연령대별 분석
def process_corpus_by_age(docs, analyzer='kiwi'):
    age_texts = defaultdict(str)

    for doc in docs:
        meta = doc.get("metadata", {})
        speakers = meta.get("speaker", [])
        if not speakers:
            continue

        age = speakers[0].get("age")
        utterances = doc.get("utterance", [])
        text = " ".join(utt.get("form", "") for utt in utterances)
        age_texts[age] += text + " "

    result = {}
    for age, text in age_texts.items():
        morphs = analyze_morphs(text, analyzer)
        total_count = len(morphs)
        freq = Counter(morphs)
        df = pd.DataFrame({
            '형태소': [m[0] for m in freq.keys()],
            'POS': [m[1] for m in freq.keys()],
            '절대빈도': list(freq.values())
        })
        df['상대빈도'] = df['절대빈도'] / total_count
        df = df.sort_values(by='절대빈도', ascending=False).reset_index(drop=True)
        result[age] = df
    return result

# 결과 저장
def save_results(result_dict, analyzer, output_dir='results'):
    os.makedirs(output_dir, exist_ok=True)
    for age, df in result_dict.items():
        filename = f"{output_dir}/형태소빈도_{age}_{analyzer}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 저장 완료: {filename}")

# === 실행 ===
if __name__ == "__main__":
    corpus_dir = "./../NIKL_DIALOGUE/NIKL_DIALOGUE_00s"  # 폴더명 변경 필요 예: NIKL_DIALOGUE_20s
    documents = load_all_jsons(corpus_dir)

    # Kiwi 분석기 결과
    kiwi_results = process_corpus_by_age(documents, analyzer='kiwi')
    save_results(kiwi_results, analyzer='kiwi')

    # Kkma 분석기 결과
    kkma_results = process_corpus_by_age(documents, analyzer='kkma')
    save_results(kkma_results, analyzer='kkma')

# %%
