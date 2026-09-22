# Weave Assist · 0921 기준본

중간점검 후 남긴 자료를 기준으로 2026-09-22 수정사항을 반영했습니다.

- 기획서: `슈퍼루키 PPT구성안 (final) c687f0ddc122821aabc60188e272d630.md`
- 티저 기준본: `teaser-final.png`
- 발표자료: 최신 티저 사진 표지를 적용한 `ppt/index.html` 및 같은 폴더의 PDF·PPTX
- 기존 파일명: `ppt/index-experimental.html` 및 `experimental-cover` PDF·PPTX도 최종본과 동일
- 재사용 아이콘: `assets/icons/weave-spool-outline.png`, `assets/icons/weave-spool-filled.png`
- 사진 편집 프롬프트·검증·출처: `assets/IMAGE-EDIT-NOTES.md`

## 이번 수정

최신 티저 수정에서는 글자를 지운 자리의 울렁임·잔상·가로 경계를 복원하고, 왼쪽 아래에 옅고 균일한 정사각 음영을 적용했습니다. 실제 Noto Sans KR·Inter, 새 프로필과 아이콘은 유지했습니다. 사진 표지 오른쪽은 직전보다 약 3% 더 보여 카드 옆 여백을 확보했고, 사진이 나타나는 시작 위치는 유지한 채 그 부분을 조금 더 어둡게 했습니다. 최신 검증·프롬프트는 `assets/IMAGE-EDIT-NOTES.md`, 이번 수정 전 파일은 `../0920/before-0922-background-fix/`에 있습니다.

Page 2·3·4 문구 수정, Page 8 용어 정의, Page 9 답변별 보충 설명과 출처를 반영했습니다. 빠졌던 MD Page 10 ‘왜 삼성인가? / 왜 지금인가?’를 PPT에 추가해 **발표 본편은 12장**입니다. Appendix에는 임베딩 모델의 동작 원리, 키워드·의미 검색의 차이, UX 1 전역 검색과의 관계를 보강했습니다.

Page 10은 삼성·기술 환경의 강점, Page 11은 서비스 비교, Page 12는 세 기대효과입니다. 최신 사진 표지를 기본 HTML·PDF·PPTX에도 적용했습니다. 2~12쪽은 그대로 유지했고, 기존 experimental 파일명도 최종본과 동일하게 맞췄습니다. 이전 HTML UI 표지와 내보내기는 `../0920/before-0922-promote-teaser-cover/`에 보관했습니다.

`Zone.Identifier` 6개는 삭제했고, 실제 이미지·문서는 삭제하지 않았습니다. 이전 최상위 PNG·TXT·MD는 `../0920/`, 이번 수정 직전 기준본은 `../0920/before-0922/`에 보존했습니다.

## 열기

공유 위치: [gnueaj/t3 · main 브랜치](https://github.com/gnueaj/t3/tree/main/weave/final/0921). 발표자료 수정만 반영하며, 자료와 무관한 로컬 커밋은 포함하지 않았습니다.

Git 저장소에서 이 폴더 전체를 받은 뒤 HTML을 여세요. HTML과 `assets` 폴더를 함께 두면 글꼴·아이콘을 인터넷에서 다시 받지 않고 열 수 있습니다. 방향키로 이동하고 F로 전체화면을 켭니다. 휴대폰에서 HTML 실행이 제한되면 PDF를 열어 주세요. 이번 버전부터 임시 ZIP 공유 링크는 새로 만들지 않습니다.

PPTX 텍스트는 편집 가능하지만, 시각적 일치를 위해 배경·도형·UI는 이미지 층으로 고정했습니다. 배치를 크게 바꾸려면 HTML을 수정하는 것이 적합합니다. 상세 검수 범위는 `ppt/PPTX-validation.md`를 참고해 주세요.
