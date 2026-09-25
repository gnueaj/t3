# Weave Assist PPTX 수정·검수 기록

수정일: 2026-09-21

## 결과 파일

- `Weave-Assist-11slides-fixed.pptx`: 11장, 16:9, 편집 가능한 텍스트·도형.
- `Weave-Assist-11slides-fixed-preview.pdf`: 위 PPTX를 호환 렌더러로 열어 출력한 확인용 PDF. HTML을 다시 PDF로 출력한 파일이 아닙니다.
- `index.html`: 수정하지 않았습니다.

## 보정 내용

- 한글까지 Inter로 지정되던 문제를 수정했습니다. 한국어에는 Noto Sans KR, 영문·숫자에는 Inter를 지정했습니다.
- HTML의 400·500·600·700 굵기를 정적 폰트로 구분해 포함했습니다. 중간 굵기는 `Inter Medium`, `Inter SemiBold`, `Noto Sans KR Medium`, `Noto Sans KR SemiBold`라는 이름으로 표시됩니다. 서로 다른 폰트 디자인이 아니라 해당 패밀리의 굵기별 글꼴입니다.
- PPTX에 8개 폰트 파일을 Embedded OpenType 형식으로 포함했습니다. 글리프 일부만 추린 것이 아니라 전체 글꼴을 포함했습니다.
- HTML에서 356개 텍스트 줄/인라인 조각의 위치·크기·자간·줄바꿈을 측정해 다시 배치했습니다. 자동 줄바꿈과 자동 축소를 껐습니다.
- 한글과 영문·기호 사이에 렌더러가 임의의 간격을 추가하지 않도록, 폰트별 텍스트 구간을 원본 위치에 배치하고 줄 단위로 그룹화했습니다.
- 기존 SVG 아이콘·연결선은 유지하고, SVG를 지원하지 않는 뷰어를 위한 PNG 대체 이미지 23개를 추가했습니다. 전체 슬라이드를 이미지로 바꾼 파일이 아닙니다.

## 검증 결과

검수 환경: Chromium 원본 HTML 렌더링, LibreOffice Impress 24.2.7.2 + 지정 글꼴, PDF 텍스트 위치 분석, OOXML 구조 및 python-pptx 열기 검사.

| 검사 | 결과 |
|---|---|
| 슬라이드 수 | 11장 |
| 원본 문구 누락 | 0건 |
| 원본 줄에 추가된 줄바꿈 | 0건 |
| 텍스트의 슬라이드 오른쪽 경계 초과 | 0건 |
| 원본 대비 텍스트 기준선 최대 차이 | 약 0.071 px — 위 호환 렌더러 기준 |
| 검수 PDF에서 다른 폰트로 대체된 텍스트 | 없음 — 지정 글꼴 제공 상태에서 확인 |
| HTML 원본 SHA-256 | `e2b7b2157dc9b832d4f8f1246196b2a45016ebe507490f095d6de568cd7bdc1d` |

실제 Microsoft PowerPoint를 실행할 수 있는 연결된 환경은 없어, Microsoft PowerPoint에서의 직접 검수나 모든 OS·뷰어에서의 픽셀 단위 동일성은 보장하지 않습니다. LibreOffice 24.2는 이 PPTX의 내장 폰트를 자동 적용하지 않아, 검수 시 동일한 글꼴 파일을 별도로 제공했습니다. PPTX에 폰트 파일과 연결 정보가 포함된 것은 별도로 확인했습니다.

## 편집 안내

텍스트는 편집할 수 있습니다. 줄 단위 그룹 안에서 수정할 텍스트를 선택하거나 그룹을 해제하면 됩니다. 줄바꿈 재발을 막기 위해 배치를 고정했으므로, 긴 문구로 바꾸는 경우 해당 줄의 텍스트 상자 위치·폭을 조정해야 합니다.

## 글꼴 출처

- Inter: https://fonts.google.com/specimen/Inter
- Noto Sans KR: https://fonts.google.com/noto/specimen/Noto+Sans+KR
- 두 글꼴 모두 SIL Open Font License로 제공됩니다. 폰트의 저작권·라이선스 메타데이터는 유지했습니다.
