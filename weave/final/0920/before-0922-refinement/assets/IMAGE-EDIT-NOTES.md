# 티저·아이콘 수정 기록 · 2026-09-22

## 최종 자산

- `../teaser-final.png`: 0921 티저의 실타래 3곳만 교체한 기준본.
- `icons/weave-spool-outline.png`: UI용 보라색 선·투명 내부 및 배경 PNG, 512×512.
- `icons/weave-spool-filled.png`: 제목용 보라색 채움·투명 내부 틈 및 배경 PNG, 512×512.
- `teaser-cover-experimental.png`: 문구 제거·카드 위치/크기 조정·재구도를 적용한 별도 실험용 배경. 기준 티저를 대체하지 않음.

아이콘은 제공된 원본 PNG의 알파·형태를 그대로 보존하고 검정 픽셀을 `#8B65D9`로 치환했습니다. 사진의 기존 아이콘을 지우는 작업과 실험용 배경 편집에는 내장 imagegen을 사용했습니다(CLI/API fallback 아님).

기준 티저는 생성된 이미지 전체로 덮어쓰지 않고, 세 지정 영역의 배경 복원 결과와 새 아이콘만 원본에 합성했습니다. **1672×941 유지, 세 수정 영역 밖 변경 픽셀 0개**. 영역 좌표와 검증 결과는 `teaser-icon-validation.json`에 있습니다. 이 픽셀 동일성 검증은 실험용 배경에는 적용되지 않습니다.

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
