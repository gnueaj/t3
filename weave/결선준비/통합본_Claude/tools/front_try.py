#!/usr/bin/env python3
"""본 발표의 앞부분(1~N쪽)만 말하며 넘기는 영상으로 찍는다 → 앞부분_미리보기.mp4 (덱 옆). 덱과 전체 영상의 낭독(out/tts)은 건드리지 않는다.

  python tools/front_try.py            1~3쪽(표지, 2쪽의 음성, 3쪽)
  python tools/front_try.py --n 5      1~5쪽
  python tools/front_try.py --check    낭독을 받아쓰기로 글과 견줌

14차 뒤(11월 17일 밤): '한번 이 정도까지만 수정해서 바뀐 앞부분만 랜더링해 줘'. 전체 영상(talk.py, 12분)을 다시 찍지 않고 바뀐 앞부분만 본다.
낭독과 녹화는 out/front/에 따로 둔다(talk.py와 같은 목소리, 같은 틈). 2쪽의 음성은 talk.py처럼 녹화에서 재생이 시작한 때를 찾아 원본을 섞는다.
"""
import argparse
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import make as MK  # noqa: E402
import talk as TK  # noqa: E402

HW = MK.HW
WORK = MK.OUT / 'front'
DST = HERE / '앞부분_미리보기.mp4'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=3)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    seq = MK.SEQ[:a.n]
    assert all(isinstance(k, str) and k != 'mg' for k in seq), '앞부분은 표지와 옮겨 온 인트로 장까지만: %s' % (seq,)
    WORK.mkdir(parents=True, exist_ok=True)
    HW.OUT = TK.OUT = WORK                      # 낭독(tts, _cues.json)과 녹화를 여기에: 전체 영상의 낭독을 지우지 않게
    HW._CUE_CACHE.clear()
    fu = [u for u in TK.foreign_units() if u[0] in seq]
    proxies = [types.SimpleNamespace(key=k, notes=say) for k, _, say in fu]
    says, clips = HW.narrate(proxies, None, a.check)
    for p in proxies:                           # talk.narrate_all과 같은 손질: 장이 열린 뒤 말을 떼기까지의 틈을 장마다
        lead = TK.LEADS.get(p.key, HW.LAT_START)
        says[p.key] = [lead + TK.tts_c.wav_len(clips[p.key][0]) + HW.seg_gaps(p)[0]] + list(says[p.key][1:])
    auto, silent = WORK / '_auto.pptx', WORK / '_silent.mp4'
    secs, plan = TK.build_auto(auto, fu, says, seq=seq)
    TK.seg_secs(plan, says)
    rows, total = TK.estimate(plan)
    print('녹화: %d장, 어림 %d:%04.1f' % (len(secs), total // 60, total % 60))
    print(MK.render_c.video(auto, silent, secs))
    full = WORK / '앞부분_1080p.mp4'
    rows, end = TK.finish(silent, full, plan, clips)
    TK.shrink(full, DST)
    for k, t0, n in rows:
        print('   %-8s %5.1f초부터 %5.1f초' % (k, t0, n))
    print('→', DST, '%.1f초' % end)


if __name__ == '__main__':
    main()
