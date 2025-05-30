# 형태소 분석 및 빈도 분석

1) 조건에 부합하는 파일 중에서 주제별로 4개씩 선정 (총 24개)
2) "NIKL_DIALOGUE_00s" 폴더에 선별한 파일을 이동 후 분석할 연령대에 맞게 폴더명 변경 (예: "NIKL_DIALOGUE_20s")
3) "analyze_morpheme" 코드의 corpus_dir = "NIKL_DIALOGUE_00s" 폴더명도 변경

## 역할 분담

| 이름 | 담당 연령대 | 브랜치 이름 예시 |
|------|--------------|------------------|
| 황혜진 | 20대         | `morphs-20s`     |
| 김도현 | 30대         |    |
| 황훈의 | 40대         |    |
| 서지현 | 50대, 60대   |    |

※ 브랜치 이름: `morphs-[연령대]` 형식으로 통일

## 폴더 구조

```bash
KORE208_FINAL/
├── morpheme_analysis/
│   ├── NIKL_DIALOGUE_00s        # 분석할 데이터가 들어 있는 폴더
│   ├── analyze_morphemes.py     # 분석용 코드
│   ├── results                  # 분석 결과가 저장되는 폴더
│   │   ├── results/형태소빈도_00대_kiwi.csv
│   │   └── results/형태소빈도_00대_kkma.csv
│   └── readme_morphs.md                # 참고 사항
```

## 일정
- 6/1 일요일까지 형태소 분석 및 빈도 분석 후 결과 정리