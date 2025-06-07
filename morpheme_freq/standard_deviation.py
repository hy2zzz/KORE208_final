# %%
import os
import json
from collections import defaultdict, Counter
import pandas as pd
from konlpy.tag import Kkma
from kiwipiepy import Kiwi

kiwi = Kiwi()
kkma = Kkma()

# 1. JSON 파일 불러오기
def load_jsons_from_multiple_folders(folder_paths):
    all_docs = []
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_docs.extend(data.get("document", []))
    return all_docs

# 2. 연령대별 형태소 분석 (특정 품사만 필터링, 상위 10위까지만 추출)
def analyze_morphs_by_age(documents, target_pos_list, analyzer='kiwi'):
    age_texts = defaultdict(str)

    for doc in documents:
        speakers = doc.get("metadata", {}).get("speaker", [])
        if not speakers:
            continue
        age = speakers[0].get("age")
        text = " ".join(utt.get("form", "") for utt in doc.get("utterance", []))
        age_texts[age] += text + " "

    result = {}
    for age, text in age_texts.items():
        if analyzer == 'kiwi':
            tokens = kiwi.tokenize(text)
            morphs = [(t.form, t.tag) for t in tokens if t.tag in target_pos_list] # 특정 헝태소만 추출
        else:
            tokens = kkma.pos(text)
            morphs = [(form, tag) for form, tag in tokens if tag in target_pos_list]

        # 특정 품사의 전체 빈도 (절대 빈도의 합)
        total = sum(Counter(morphs).values())

        # 상위 형태소 추출
        freq = Counter(morphs)
        top_items = freq.most_common()

        # DataFrame 생성
        df = pd.DataFrame({
            '형태소': [m[0][0] for m in top_items],
            'POS': [m[0][1] for m in top_items],
            '절대빈도': [m[1] for m in top_items]
        })

        # 해당 품사 내에서의 상대빈도
        df['상대빈도'] = df['절대빈도'] / total if total > 0 else 0

        result[age] = df

    return result

# 4. 연령대 간 형태소 상대빈도 비교 (표준편차 기준)
def compare_relative_frequencies(result_dict, output_filename='POS_상대빈도_비교.csv', output_dir='results_freq'):
    os.makedirs(output_dir, exist_ok=True)

    morph_stats = defaultdict(dict)

    for age, df in result_dict.items():
        for _, row in df.iterrows():
            morph_stats[row['형태소']][age] = row['상대빈도']

    comparison_df = pd.DataFrame(morph_stats).T.fillna(0)
    comparison_df['표준편차'] = comparison_df.std(axis=1)
    comparison_df = comparison_df.sort_values(by='표준편차', ascending=False)

    save_path = os.path.join(output_dir, output_filename)
    comparison_df.to_csv(save_path, encoding='utf-8-sig')
    print(f"연령대 비교 표 저장 완료: {save_path}")

# 분석기별 POS 설정
pos_dict = {
    'kiwi': ["EP", "EF", "EC", "ETN", "ETM"], # 어미 (kiwi)
    'kkma': ["EPH", "EPT", "EPP", "EFN", "EFQ", "EFO", "EFA", "EFI", "EFR", "ECE", "ECS", "ECD", "ETN", "ETD"] # 어미 (kkma)
    #'kiwi': ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC"],  # 조사 (kiwi)
    #'kkma': ["JKS", "JKC", "JKG", "JKO", "JKM", "JKI", "JKQ", "JX", "JC"]   # 조사 (kkma)
}

# 실행
if __name__ == '__main__':
    base_dir = "."
    folders = [os.path.join(base_dir, f"NIKL_DIALOGUE_{age}s") for age in [10, 20, 30, 40, 50, 60]]

    documents = load_jsons_from_multiple_folders(folders)
    
    for analyzer in ['kiwi', 'kkma']:
        print(f"\n 분석기: {analyzer.upper()}")
        target_pos = pos_dict[analyzer]

        results = analyze_morphs_by_age(documents, target_pos_list=target_pos, analyzer=analyzer) # 결과 계산
        compare_relative_frequencies(results, output_filename=f'어미빈도_비교_{analyzer}.csv') # 표준편차
# %%
