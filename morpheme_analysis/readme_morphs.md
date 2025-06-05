# 형태소 분석 및 빈도 분석
1. 전체 형태소 분석
1) 조건에 부합하는 파일 중에서 주제별로 4개씩 선정 (총 24개)
2) "NIKL_DIALOGUE_00s" 폴더에 선별한 파일을 이동 후 분석할 연령대에 맞게 폴더명 변경 (예: "NIKL_DIALOGUE_20s")
3) "analyze_morpheme" 코드의 corpus_dir = "NIKL_DIALOGUE_00s" 폴더명도 변경
※ 브랜치 이름: `morphs-[연령대]` 형식으로 통일

역할 분담

|이름  | 형태소 분석   | 특정 품사 분석 |
|-----|---------------|----------------|
|황혜진 | 10대, 20대, 40대 | 조사, 어미 |
|김도현 | 30대         | 부사(간투사), 조사, 어미 |
|황훈의 |         |    |
|서지현 | 50대, 60대   |    |


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

## Git 및 브랜치 사용법
1) 원격 저장소 불러오기: git clone https://github.com/hy2zzz/KORE208_final.git
2) 개발 환경 재현: 가상환경 활성화 후 pip install -r requirements.txt
3) 브랜치 생성: git checkout -b 브랜치명 (예: morphs-20s)
4) "NIKL_DIALOGUE_00s" 폴더에 선별한 파일을 이동시킨 후 분석할 연령대에 맞게 폴더명 변경 (예: "NIKL_DIALOGUE_20s")
5) "analyze_morpheme" 코드의 corpus_dir = "NIKL_DIALOGUE_00s" 부분의 폴더명도 변경
6) 코드 실행 후, 원본 말뭉치 파일과 결과(엑셀) 파일 add (예: git add morpheme_analysis/NIKL_DIALOGUE_20s/) ※ 코드 파일에 추가 및 변경 사항이 있을 경우 코드용 브랜치를 따로 만들어 주세요!
7) 커밋(변경사항 저장): git commit -m "커밋메시지"
8) github에 업로드: git push origin 브랜치명
9) Pull Request: 브랜치의 내용을 main에 합치기

## 일정
- 6/1 일요일까지 형태소 분석 및 빈도 분석 후 결과 정리
- 6/6 금요일까지 특정 품사 분석 및 시각화 후 모델 학습 진행 논의
