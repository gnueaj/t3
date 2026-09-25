# Weave Assist HTML 발표자료

## PPTX 변환 수정본 · 2026-09-21

- [수정 PPTX](Weave-Assist-11slides-fixed.pptx)
- [수정 PPTX를 렌더링한 확인용 PDF](Weave-Assist-11slides-fixed-preview.pdf)
- [검수 내용 및 편집 안내](PPTX-validation.md)

기존 11장의 문구·구성과 HTML 원본은 유지했습니다. 한글과 영문 폰트, 굵기, 음수 자간을 다시 지정하고, HTML에서 측정한 줄 위치로 텍스트를 재배치했습니다. Inter와 Noto Sans KR의 사용 굵기를 PPTX에 포함했습니다. 위 로컬 파일은 아래 기존 다운로드 링크와 달리 만료되지 않습니다.

## HTML 발표 화면

- 발표 화면: `index.html`을 브라우저에서 엽니다.
- 11장 · 16:9(1280×720) · 어두운 남색/라벤더.
- 한국어: Noto Sans KR, 영어·숫자: Inter.
- 좌우 방향키 / Page Up·Down / Space로 이동, Home·End로 처음·끝, F로 전체화면.
- 아래 선택 메뉴로 원하는 페이지에 바로 이동할 수 있습니다.
- 글자·표·앱 UI는 HTML 텍스트와 도형입니다. 기억의 연결선은 SVG이며 확대해도 선명합니다.
- 웹폰트·Tailwind·아이콘을 불러오므로 인터넷 연결이 필요합니다.
- 공개 아이콘은 Presenton 검색 결과를 사용했습니다. 티저 원본 이미지는 수정본 `../teaser-final.png`으로 별도 보존되어 있습니다.
- HTML 표지는 티저의 대화 장면을 남색 배경의 HTML UI로 재구성한 버전입니다.
- 슬라이드의 문구는 MD 원문을 발표 화면에 맞게 압축했습니다. 구현 및 비교 평가는 제안 설계/공개 기능 안내 기준입니다.

## 페이지 구성

1. Teaser
2. Motivation
3. Pain Points
4. Solution
5. UX 1 — 전역 검색
6. UX 2 — 자동 완성
7. UX 3 — 먼저 건네는 기억
8. 구현
9. Q&A (3문답)
10. 차별화 포인트
11. 기대효과

## 폰트

- [Noto Sans KR](https://fonts.google.com/noto/specimen/Noto+Sans+KR)
- [Inter](https://fonts.google.com/specimen/Inter)

PPTX를 다른 기기에서 편집할 경우 두 글꼴을 설치하면 글꼴 대체와 줄바꿈 변화를 줄일 수 있습니다.

## 다운로드와 공유

아래 링크는 생성 후 24시간 동안 유효합니다. 로컬 `index.html`은 만료되지 않습니다.

- [온라인 미리보기](https://presenton.ai/presentation-preview?t=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiaHRtbC10by1hbnktcHJldmlldyIsImh0bWxfdG9fYW55X2NyZWF0aW9uIjo2NDEyLCJleHAiOjE3OTAwNjI3MjJ9.XrFpJ0lfjm2uT7rtfvH1RiMSuKxs4eyRyXZhx-XImAs)
- [PowerPoint PPTX](https://api.presenton.ai/s/wHjI8vLu6D-syqBEEz7dVDbPlSrAVQjs)
- [PDF](https://api.presenton.ai/s/EEL4tIu464dWjlYlqOA25F41Np_H1ot1)
- [슬라이드 PNG 묶음](https://api.presenton.ai/s/nfk0eFtTlOlh7PsnmQSllnAXaboQGvo3)

세 내보내기는 동일한 최종 HTML에서 생성했습니다. 검증된 글꼴은 Inter와 Noto Sans KR이며, 11장 모두 텍스트의 슬라이드 경계 초과와 누락된 아이콘이 없음을 로컬 Chromium 렌더링으로 확인했습니다.
