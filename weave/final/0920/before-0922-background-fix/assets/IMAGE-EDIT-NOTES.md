# 티저·아이콘 수정 기록 · 2026-09-22

## 최신 수정 · 프로필 / 아이콘 크기 / 글꼴 / 표지 구도

- ‘나’ 프로필만 짙은 머리·옆으로 내려온 앞머리의 젊은 인물로 교체했습니다. 엄마의 프로필과 사진 속 인물은 그대로입니다. 같은 새 프로필을 티저와 PPT 사진 표지에 사용했습니다.
- UI 실타래는 응답 카드에서 32→27px, 키보드에서 23→20px로 줄였습니다. 보라색 `#8B65D9`는 유지하고, 512px 원본의 선 알파 영역만 2px 확장해 작은 크기에서도 선이 묻히지 않게 했습니다. 제목용 채움 실타래는 변경하지 않았습니다.
- “그때 그거? / Weave [실타래] got it!”와 왼쪽 하단 홍보 문구는 **실제 Noto Sans KR·Inter TTF**를 Chromium에서 렌더링했습니다. 사진 속 앱 화면·상표 로고까지 다시 그린 것은 아닙니다. 편집 가능한 원본은 `teaser-typography.html`, 문구 아래 사진은 `teaser-retouched-base.png`입니다.
- 사진 표지는 오른쪽 책 문구가 사라지는 위치까지 137px를 잘라 **1420×1010**으로 조정했습니다. 약 5%라는 비율보다 ‘The Brighter…가 안 보이는 지점’을 우선한 값입니다. HTML의 왼쪽 그라데이션도 조금 옅게 해 얼굴을 더 드러냈습니다. 크롭 전 수정본은 `teaser-cover-source.png`입니다.
- `teaser-refinement-validation.json`: 기준 티저 1672×941 유지, 지정한 다섯 영역 밖 변경 픽셀 **0개**. 크롭 전 사진 표지도 프로필·아이콘 세 영역 밖 변경 픽셀 **0개**. 비교 기준은 `0920/before-0922-refinement/`입니다.

프로필 교체와 지울 문구·아이콘의 배경 복원에는 **내장 imagegen**을 사용했습니다(CLI/API fallback 아님). 생성 이미지 전체를 덮어쓰지 않고 필요한 부분만 합성했습니다. 글자 주변 배경은 인접한 원본 픽셀에 맞춰 색을 보정했고, 제목·아이콘은 정확한 폰트·원본 로고로 별도 합성했습니다. 이번 두 생성 프롬프트 전체는 `refinement-prompts.json`에 있습니다.

## 이전 아이콘 교체 작업의 자산·기록

- `../teaser-final.png`: 위 최신 수정까지 적용한 0921 티저 기준본.
- `icons/weave-spool-outline.png`: UI용 보라색 선·투명 내부 및 배경 PNG, 512×512.
- `icons/weave-spool-filled.png`: 제목용 보라색 채움·투명 내부 틈 및 배경 PNG, 512×512.
- `teaser-cover-experimental.png`: 문구 제거·카드 위치/크기 조정·재구도를 적용한 별도 실험용 배경. 기준 티저를 대체하지 않음.

최초 아이콘 교체에서는 제공된 원본 PNG의 알파·형태를 그대로 보존하고 검정 픽셀을 `#8B65D9`로 치환했습니다. 이후 UI용 선 굵기 조정은 위 최신 수정에 해당합니다. 사진의 기존 아이콘을 지우는 작업과 실험용 배경 편집에는 내장 imagegen을 사용했습니다(CLI/API fallback 아님).

최초 교체에서 세 아이콘 영역 밖 변경 픽셀은 0개였습니다. `teaser-icon-validation.json`은 **최초 교체 시점의 이력**이며 현재 파일의 최신 검증은 `teaser-refinement-validation.json`을 확인하세요. 실험용 배경을 처음 생성한 작업에는 원본 대비 픽셀 동일성을 주장하지 않습니다.

## 아이콘 출처

- [Flaticon — Spool of thread 2175860](https://www.flaticon.com/free-icon/spool-of-thread_2175860) · UI용
- [Flaticon — Spool of thread 2175772](https://www.flaticon.com/free-icon/spool-of-thread_2175772) · 제목용

사용자가 지정한 자산입니다. 원본 PNG도 `icons/`에 보존했습니다. 원본 상세 페이지의 작가·라이선스 표기를 이 환경에서 확인하지 못했으므로, 외부 공개·상업 사용 전 각 원본의 이용 조건과 작가 표시 요구사항을 확인해 주세요. 이 문서는 별도의 이용권을 부여하지 않습니다.

## 내장 imagegen 편집 프롬프트

### 1. 기존 아이콘 배경 복원

Use case: precise-object-edit. Edit target: the supplied Weave teaser photograph, 1672 x 941. Prepare a clean base for replacing ONLY three purple spool/thread icons with supplied brand artwork later. Erase ONLY these three old purple spool icons and reconstruct the immediately underlying background: (1) the small purple spool just left of the blue Weave label inside the white phone suggestion card, around x=656..697,y=325..364; (2) the tiny spool in the first keyboard toolbar button around x=605..638,y=555..582, retain the pale lavender circular button and glow; (3) the purple spool and its short thread between the large word Weave and got it! at upper right, around x=1335..1414,y=200..264, restoring the blurred plant background. Preserve all the letters, all other text, the phone, UI layout, screen contents, woman, cake card, map, threads connecting cards, Samsung and Galaxy AI marks, lighting and background EXACTLY as the input. Do not add replacement icons yet. No global recoloring, no re-layout, no new text. Same aspect ratio and framing. These are three tiny local erasures only. Return edited image.

### 2. 실험용 표지 배경

Use case: precise-object-edit / compositing. Edit this exact Weave teaser into a photo-background asset for an experimental presentation cover, keeping the same woman, phone, phone screen, cafe, cake memory card, location card, and the NEW outlined purple spool icons in the phone. Requested edits only: completely remove the lower-left Weave Assist title and Korean tagline; completely remove the large upper-right '그때 그거? Weave [spool] got it!' title including its spool, fill with matching out-of-focus cafe background. Move the two floating cards on the right upward by about 70 pixels, enlarge both only slightly (about 6%), and move them left slightly as needed. Preserve their exact contents including Korean text, cake image and map and reconnect the fine glowing purple threads naturally from phone to moved cards. Reduce/crop the rightmost mostly-background area by roughly 10–15% for a more compact composition, keeping both cards and all of the phone screen visible. Result should be a closely faithful photographic composition with the phone and both memory cards as focal points, not a new illustration. Keep original lighting and colors. Keep the woman's face and hands as-is. Do not rewrite phone text. Do not add headlines, graphics or logos. We will overlay crisp HTML text outside this photo later. Target 1456x944 or very similar compact landscape ratio. This is a separate experimental asset, not replacement of the original teaser.

실험용 배경은 생성 편집 결과이므로 사진 속 미세한 디테일은 원본과 달라질 수 있습니다. 발표 제목·설명은 사진에 굽지 않고 HTML 텍스트로 별도 배치했습니다.
