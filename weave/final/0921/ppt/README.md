# Weave Assist 발표자료 · 2026-09-22

## 기준본 · 12장

- [HTML 발표 화면](index.html)
- [PDF — HTML 기준](Weave-Assist.pdf)
- [PowerPoint — 글꼴 내장·텍스트 편집 가능](Weave-Assist-12slides-fixed.pptx)
- [PPTX 재렌더링 확인용 PDF](Weave-Assist-12slides-fixed-preview.pdf)
- [검수 범위 및 편집 안내](PPTX-validation.md)

## 사진 표지 실험본 · 별도 12장

- [HTML 실험본](index-experimental.html)
- [PDF 실험본](Weave-Assist-experimental-cover.pdf)
- [PowerPoint 실험본](Weave-Assist-experimental-cover.pptx)
- [표지 PNG 미리보기](cover-experimental.png)

실험본은 1쪽만 다릅니다. 티저 사진을 오른쪽 약 68%에 배치하고, 사진 속 제목·하단 문구를 제거한 뒤 기억 카드 두 장을 위로 올렸습니다. 발표 제목은 이미지가 아닌 선명한 텍스트로 남겼습니다. 사진은 내장 imagegen으로 편집했으며, 기준 티저와 픽셀 단위로 동일한 자산은 아닙니다.

‘나’ 프로필과 두 UI 실타래 수정은 유지했습니다. 사진 표지의 오른쪽은 직전보다 43px(약 3%) 더 보여 카드 옆 여백을 확보했습니다. 사진이 나타나는 시작 위치는 그대로 두고, 해당 부분을 조금 더 어둡게 해서 점진적으로 밝아지게 조정했습니다. 첫 장 상단 영문 설명과 전 페이지의 반복 영문 푸터는 삭제 상태로 유지했습니다.

최신 티저 PNG는 `assets/teaser-final.png`입니다. 제목과 왼쪽 하단 문구의 실제 Noto Sans KR·Inter를 유지한 채, 글자를 지운 배경의 잔상·울렁임·가로선을 복원했습니다. 하단 음영은 옅은 정사각형으로 정리했습니다. `assets/teaser-typography.html`에서 해당 문구와 음영의 원본 배치를 볼 수 있습니다.

## 반영 사항

Page 2 동기·설문 출처, Page 3 페르소나 문구, Page 4 세 UX 표현, Page 8 Search index / Indexing 정의, Page 9 Q&A 보충 설명을 반영했습니다. MD의 ‘왜 삼성인가? / 왜 지금인가?’를 Page 10에 추가했습니다. 서비스 비교는 Page 11, 세 기대효과는 Page 12입니다.

Page 5~7의 시나리오·구성과 서비스 비교의 내용은 유지했습니다. 새 실타래는 기존 Weave 버튼과 표지 제목에 적용했습니다. 모델 정의·입력 형식·학습 예시·구동 파이프라인은 0921 기획서 맨 아래 Technical details 부록에 있습니다. 이번에는 임베딩 모델과 전역 검색의 관계도 보강했습니다.

## 실행·편집

Git 저장소에서 폴더 전체를 받은 뒤 HTML을 엽니다. `assets` 폴더를 옮기거나 지우지 마세요. 폰트·CSS 실행 스크립트·아이콘을 함께 포함해 오프라인에서도 열 수 있습니다.

방향키 / Page Up·Down / Space 이동, Home·End 처음·끝, F 전체화면. 휴대폰에서 로컬 HTML 열기가 제한되면 PDF를 사용하세요.

폰트는 한국어 Noto Sans KR, 영어·숫자 Inter입니다. 사용한 400·500·600·700 굵기를 HTML 자산과 PPTX에 포함했습니다. 글꼴 라이선스는 `assets/fonts/*-OFL.txt`에 있습니다.

PPTX에는 브라우저에서 측정한 줄 위치와 자간을 적용했습니다. **텍스트는 편집 가능하고, 배경·도형·UI는 2배 해상도 이미지 층으로 고정**했습니다. 이는 슬라이드 전체를 한 장의 이미지로 만든 방식과 다릅니다. 긴 문구로 수정하면 텍스트 위치도 수동 조정해야 할 수 있습니다.

## 검수

기준본·실험본 각 12장을 오프라인 Chromium에서 열어 폰트·이미지 로드와 텍스트 경계를 확인했습니다. PPTX는 LibreOffice에서 다시 PDF로 렌더링해 추가 줄바꿈·텍스트 누락·오른쪽 경계 초과를 검사했습니다. 실제 Microsoft PowerPoint에서 직접 실행한 검수는 아닙니다.

## 자산 출처

- [Inter](https://fonts.google.com/specimen/Inter), [Noto Sans KR](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
- 일반 UI 아이콘: 기존 Presenton 공개 아이콘
- 새 실타래: 사용자 지정 [Flaticon 2175860](https://www.flaticon.com/free-icon/spool-of-thread_2175860), [Flaticon 2175772](https://www.flaticon.com/free-icon/spool-of-thread_2175772)
- 사진: 0921 티저 기준본에서 별도 편집

Flaticon 작가·라이선스 상세는 원본 페이지에서 확인해 주세요. 자산 편집 기록은 `assets/IMAGE-EDIT-NOTES.md`에 있습니다. 발표자 확인용 출처 링크는 관련 슬라이드와 0921 기획서에 남겼습니다.

## 다운로드와 공유

이번 버전부터 `weave/final/0921` 전체를 `gnueaj/t3` Git 저장소로 공유합니다. 임시 ZIP 링크는 새로 만들지 않으며, 과거 ZIP·Presenton 링크는 이번 수정본을 가리키지 않습니다. 사진 표지를 사용하려면 `index-experimental.html` 또는 `Weave-Assist-experimental-cover.pdf` / `.pptx`를 선택하세요.
