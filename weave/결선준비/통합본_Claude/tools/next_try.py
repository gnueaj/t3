#!/usr/bin/env python3
"""9차 후보(next_new.py: 연표 다음의 '앞으로의 Weave' 장, biz_new.py: 비즈니스 임팩트 장)를 말하며 넘기는 영상으로 찍는다. 덱은 바꾸지 않는다.

  python tools/next_try.py               → 후보 모두: <폴더>/<이름>.mp4 와 후보를 모은 덱(클릭으로 넘김), 한눈에 그림
  python tools/next_try.py --only 미래A,임팩트가
  python tools/next_try.py --quick 미래A  → 낭독 없이 빨리 찍어 봄(out/next_try/quick_미래A.mp4와 한눈에 보는 그림)
  python tools/next_try.py --deck        → 후보를 모은 덱과 정적 그림(out/next_try/png)만
  python tools/next_try.py --check       → 영상에 넣은 낭독을 받아쓰기로 글과 견줌
  python tools/next_try.py --sheet       → 찍어 둔 영상에서 한눈에 그림만 다시

낭독은 이 컴퓨터 안에서만 만든다(talk.py와 같은 목소리). 낭독과 녹화는 out/next_try/<후보>/에 따로 둔다.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'tools'))
import make as MK  # noqa: E402
import talk as TK  # noqa: E402
import fx_try as FT  # noqa: E402  (틀을 빌리는 frame, 한눈에 그림 sheet)
import next_new as NX  # noqa: E402

HW = MK.HW
WORK = MK.OUT / 'next_try'
MK.READ_FIRST[:0] = [('SmartThings', '스마트싱스'), ('Bixby', '빅스비'), ('S펜', '에스펜'), ('TV', '티브이'), ('Galaxy AI', '갤럭시 에이아이')]      # 읽는 소리


def cands():
    out = list(NX.CANDIDATES)
    try:
        import biz_new as BZ
        out += BZ.CANDIDATES
    except ImportError:
        pass
    return out


def use(code):
    d = WORK / code
    d.mkdir(parents=True, exist_ok=True)
    HW.OUT = TK.OUT = d
    HW._CUE_CACHE.clear()
    return d


def pick(code):
    return next(c for c in cands() if c[0] == code)


def save(prs, old, dst):
    MK.drop_slides(prs, old)
    MK.samsung_fonts.remap_prs(prs)
    prs.save(str(dst))


def quick(code, hold=1500):
    _, fn, _, _ = pick(code)
    use(code)
    specs = fn()
    for sp in specs:
        sp.holds = [hold] * len(sp.groups)
    prs, old, layout, note_tpl = FT.frame()
    _, _, secs = HW.add_slides(prs, layout, note_tpl, specs, auto=True)
    auto, mp4 = WORK / ('quick_%s.pptx' % code), WORK / ('quick_%s.mp4' % code)
    save(prs, old, auto)
    print(MK.render_c.video(auto, mp4, secs))
    FT.sheet(mp4, WORK / ('quick_%s.jpg' % code), fps=2)
    print('→', mp4, '%.1f초' % HW.video_len(mp4))


def record(code):
    _, fn, label, dst = pick(code)
    d = use(code)
    silent, auto, meta = d / '_silent.mp4', d / '_auto.pptx', d / '_talk.json'
    says, clips = HW.narrate(fn(), None, False)
    specs = fn()                        # 낭독에서 잰 때로 효과를 다시 맞춤
    prs, old, layout, note_tpl = FT.frame()
    plan = []
    TK.talkify(specs, says, 0, plan)
    _, _, secs = HW.add_slides(prs, layout, note_tpl, specs, auto=True)
    for p, sec, sp in zip(plan, secs, specs):
        p['secs'], p['trans'] = sec, (sp.trans[1] / 1000 if sp.trans else 0)
    save(prs, old, auto)
    TK.seg_secs(plan, says)
    meta.write_text(json.dumps(dict(plan=plan, clips={k: [str(c) for c in v] for k, v in clips.items()}), ensure_ascii=False), encoding='utf-8')
    print('녹화 %s' % code)
    print(MK.render_c.video(auto, silent, secs))
    full = d / (code + '_1080p.mp4')
    rows, end = TK.finish(silent, full, plan, clips)
    dst.mkdir(exist_ok=True)
    TK.shrink(full, dst / ('%s.mp4' % code))
    (d / 'timing.json').write_text(json.dumps(dict(rows=rows, total=round(end, 2)), ensure_ascii=False), encoding='utf-8')
    for k, a, n in rows:
        print('   %-8s %5.1f초부터 %5.1f초' % (k, a, n))


def check(code):
    _, fn, _, _ = pick(code)
    d = use(code)
    m = json.loads((d / '_talk.json').read_text(encoding='utf-8'))
    return HW.narrate_check(fn(), {k: [Path(c) for c in v] for k, v in m['clips'].items()})


def deck(codes, dst):
    specs = []
    for code in codes:
        _, fn, _, _ = pick(code)
        use(code)
        specs += fn(deck=True)
    prs, old, layout, note_tpl = FT.frame()
    _, report, _ = HW.add_slides(prs, layout, note_tpl, specs)
    dst.parent.mkdir(exist_ok=True)
    save(prs, old, dst)
    for key, nclick, nnote, _ in report:
        if nclick != nnote:
            print('   ! %s: 클릭 %d ≠ 노트 (클릭) %d' % (key, nclick, nnote))
    print('→', dst.name, '%.1f MB' % (dst.stat().st_size / 1e6), len(specs), '장')
    return dst


def stills(code, times, w=800):
    """찍어 둔 녹화(자막 얹기 전)에서 그 때의 화면을 뽑는다. 돌려줌: PIL 그림 목록."""
    from PIL import Image
    wd = WORK / code
    out = []
    for j, t in enumerate(times):
        png = wd / ('_still%d.png' % j)
        subprocess.run([HW.FFMPEG, '-y', '-loglevel', 'error', '-ss', '%.2f' % t, '-i', str(wd / '_silent.mp4'), '-frames:v', '1',
                        '-vf', 'crop=1920:1062:0:0,scale=%d:-1' % w, str(png)], check=True)
        out.append(Image.open(png).convert('RGB'))
        png.unlink()
    return out


def overview(group, dst, heads):
    """후보마다 클릭이 끝난 순간들을 녹화에서 뽑아 한 장에. group = 후보 코드의 앞머리('미래', '임팩트')."""
    from PIL import Image, ImageDraw, ImageFont
    cs = [c for c in cands() if c[0].startswith(group) and (WORK / c[0] / 'timing.json').exists()]
    if not cs:
        return
    font, small = ImageFont.truetype(str(TK.FONT), 26), ImageFont.truetype(str(TK.FONT), 18)
    rows = []
    for code, fn, label, _ in cs:
        wd = WORK / code
        plan = json.loads((wd / '_talk.json').read_text(encoding='utf-8'))['plan']
        tm = json.loads((wd / 'timing.json').read_text(encoding='utf-8'))
        p_ = plan[-1]                                       # 마지막 장(후보 장)
        a = next(r for r in tm['rows'] if r[0] == p_['key'])[1]
        ss, t0 = p_['seg_secs'], a + p_['trans']
        ts = [t0 + sum(ss[:j + 1]) - 0.3 for j in range(len(ss) - 1)] + [tm['total'] - 0.5]
        rows.append((code, label, stills(code, ts[-heads:], 640)))
    w, h, pad, head, left = 640, 354, 12, 16, 270
    n = max(len(r[2]) for r in rows)
    im = Image.new('RGB', (left + n * (w + pad) + pad, head + len(rows) * (h + pad) + pad), '#FFFFFF')
    d = ImageDraw.Draw(im)
    for i, (code, label, frames) in enumerate(rows):
        y = head + i * (h + pad)
        d.text((left / 2 + 4, y + h / 2 - 16), code, font=font, fill='#1C1A24', anchor='mm')
        d.text((left / 2 + 4, y + h / 2 + 16), label, font=small, fill='#6B4EFF', anchor='mm')
        for j, fr in enumerate(frames):
            im.paste(fr, (left + pad + j * (w + pad), y))
    dst.parent.mkdir(exist_ok=True)
    im.save(dst, quality=90)
    print('→', dst.name, im.size)


def nine(dst):
    """자리 셋 × 후보 셋의 카드 아홉 장을 한 장에(정적 그림 out/next_try/png_미래에서 잘라 냄: 미래A, B, C가 2, 4, 6쪽)."""
    from PIL import Image, ImageDraw, ImageFont
    k = 1600 / 1280
    font, small = ImageFont.truetype(str(TK.FONT), 30), ImageFont.truetype(str(TK.FONT), 22)
    y0, y1 = round((NX.NAME_Y - 12) * k), round((NX.CY + NX.CH + 14) * k)
    cw, ch, pad, head, left = round((NX.CW0 + 24) * k), y1 - y0, 16, 64, 130
    im = Image.new('RGB', (left + 3 * (cw + pad) + pad, head + 3 * (ch + pad) + pad), '#FFFFFF')
    d = ImageDraw.Draw(im)
    for j, t in enumerate(['자리 1', '자리 2', '자리 3']):
        d.text((left + pad + j * (cw + pad) + cw / 2, head / 2 + 2), t, font=font, fill='#1C1A24', anchor='mm')
    for i, (name, page) in enumerate((('가', 2), ('나', 4), ('다', 6))):
        src = Image.open(WORK / 'png_미래' / ('s%02d.png' % page)).convert('RGB')
        y = head + i * (ch + pad)
        d.text((left / 2 + 4, y + ch / 2), name, font=font, fill='#6B4EFF', anchor='mm')
        for j in range(3):
            x, w = NX.card_box(3, j)
            box = (round((x - 12) * k), y0, round((x - 12) * k) + cw, y1)
            im.paste(src.crop(box), (left + pad + j * (cw + pad), y))
    im.save(dst, quality=90)
    print('→', dst.name, im.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    ap.add_argument('--quick')
    ap.add_argument('--deck', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--sheet', action='store_true')
    a = ap.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    codes = [c[0] for c in cands() if not a.only or c[0] in a.only.split(',')]
    if a.quick:
        for code in a.quick.split(','):
            quick(code)
        return
    if a.check:
        for code in codes:
            check(code)
        return
    if not (a.deck or a.sheet):
        for code in codes:
            record(code)
    if not a.sheet:
        for group, folder, name in NX.DECKS:
            cs = [c[0] for c in cands() if c[0].startswith(group)]
            if cs:
                dst = deck(cs, HERE / folder / name)
                print(MK.render_c.png(dst, WORK / ('png_' + group), 1600, 900)[-1])
    for group, folder, name in NX.DECKS:
        overview(group, HERE / folder / '한눈에.jpg', heads=4)
    nine(NX.FUT / '카드_아홉장.jpg')


if __name__ == '__main__':
    main()
