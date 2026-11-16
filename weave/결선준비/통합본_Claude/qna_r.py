"""Appendix 끝의 출처 묶음: 참고 문헌, 사진 출처, 사진과 음악 출처.

R-1은 장마다 각주에 적은 논문과 자료를 갈래별로 모은 것(짧은 표기, 두 단). 3판(11-16)에서 D와 A에 새로 쓴 연구를 더했다.
11차(11-16 저녁): RRF, Vectara 리더보드, 알림 연구 셋(C-7)을 더하고 글자를 9.5 → 9pt로. 오른쪽 단이 장 아래로 넘쳐 Knowledge Graph를 왼쪽 단으로 옮김.
"""
import appendix as AX
from ui import BODY, INK, PURPLE, R, T

import slides_new as N
from qna_lib import Page, frame, lh_of, page_slide, wrapl

REFS_L = [('Reasoning-intensive Retrieval',
           ['Su et al., "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval", ICLR 2025',
            'Taghavi et al., "ImpliRet: Benchmarking the Implicit Fact Retrieval Challenge", arXiv:2506.14407 (2025)',
            'Shao et al., "ReasonIR: Training Retrievers for Reasoning Tasks", COLM 2025',
            'Chen et al., "ReasonEmbed", ACL 2026 (arXiv:2510.08252)',
            'Sun et al., "DIVER: A Multi-Stage Approach for Reasoning-intensive Information Retrieval", arXiv:2508.07995 (2025)',
            'Jin et al., "LaSER: Internalizing Explicit Reasoning into Latent Space for Dense Retrieval", SIGIR 2026',
            'Chen et al., "AgentIR: Reasoning-Aware Retrieval for Deep Research Agents", arXiv:2603.04384 (2026)']),
          ('Query Rewriting',
           ['Ma et al., "Query Rewriting for Retrieval-Augmented Large Language Models" (Rewrite-Retrieve-Read), EMNLP 2023',
            'Moniz et al., "ReALM: Reference Resolution As Language Modeling", SIGDIAL 2024',
            'Zhu et al., "ConvSearch-R1", EMNLP 2025 (arXiv:2505.15776)',
            'Jiang et al., "DeepRetrieval", arXiv:2503.00223 (2025)',
            'Qin et al., "TongSearch-QR", arXiv:2506.11603 (2025)',
            'Chan et al., "RQ-RAG", arXiv:2404.00610 (2024)',
            'Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE), ACL 2023',
            'Wang et al., "Query2doc", EMNLP 2023']),
          ('Knowledge Graph',
           ['Crocker, Horrocks, Nenov, "Semantic Technology in Your Pocket", ISWC 2025 Industry Track',
            'Gutiérrez et al., "HippoRAG", NeurIPS 2024',
            'Han et al., "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights", arXiv:2502.11371 (2025)'])]
REFS_R = [('Multi-hop Retrieval',
           ['Xiong et al., "Multi-Hop Dense Retrieval" (MDR), ICLR 2021',
            'Trivedi et al., "Interleaving Retrieval with Chain-of-Thought Reasoning" (IRCoT), ACL 2023',
            'Zhuang et al., "EfficientRAG: Efficient Retriever for Multi-Hop Question Answering", EMNLP 2024',
            'Kim et al., "Hi-Q: Hierarchical Evidence-guided Query Refinement", NeurIPS 2026',
            '"GRITHopper", EACL 2026 (arXiv:2503.07519)',
            'Cormack, Clarke, Büttcher, "Reciprocal Rank Fusion" (RRF), SIGIR 2009']),
          ('벤치마크',
           ['Wu et al., "LongMemEval", ICLR 2025',
            'Maharana et al., "LoCoMo", ACL 2024',
            'Li et al., "LoCoMo-Plus", arXiv:2602.10715 (2026)',
            '"K-BrowseComp", arXiv:2606.02404 (2026)',
            'Vectara, "Hallucination Leaderboard" (HHEM-2.3, 2026. 10 갱신)']),
          ('알림과 먼저 건네는 제안',
           ['Pielot, Church, de Oliveira, "An In-Situ Study of Mobile Phone Notifications", MobileHCI 2014',
            'Mehrotra et al., "My Phone and Me: Understanding People\'s Receptivity to Mobile Notifications", CHI 2016',
            'Reuters Institute, "Digital News Report 2025". Apple, Human Interface Guidelines (Notifications)']),
          ('모델과 기기',
           ['Google, "EmbeddingGemma 2" (2026. 10)와 LiteRT-LM 모델 카드. FunctionGemma 모델 카드',
            'Android ML Kit GenAI Embeddings API. Android Developers 문서',
            'Apple, "Introducing Apple\'s On-Device and Server Foundation Models" (2024. 06)',
            'Samsung 지원 (Finder), Samsung Newsroom (Galaxy S26, One UI 6.1)'])]
PT = 9


def column(s, key, x, y, w, groups):
    lh = lh_of(PT, 1.5)
    out, yy = [], y
    for i, (name, items) in enumerate(groups):
        out.append(T('%s/g%d' % (key, i), x, yy, w, 22, name, size=12, color=PURPLE, weight='b', anchor='ctr'))
        out.append(R('%s/l%d' % (key, i), x, yy + 25, w, 1, fill='D9CFFF', line=None))
        yy += 32
        for j, it in enumerate(items):
            lines = wrapl(it, PT, w - 4)
            out.append(T('%s/t%d_%d' % (key, i, j), x, yy, w, lh * len(lines) + 4, lines, size=PT, color=BODY, lnspc=lh * 0.75))
            yy += lh * len(lines) + 3
        yy += 14
    assert yy - 14 <= 690, '%s: 단이 장 아래로 넘침 (%d)' % (key, yy - 14)       # 11차: 오른쪽 단이 장 밖으로 나가서 Knowledge Graph를 왼쪽 단으로 옮김
    s.add(key, out)


def s_refs():
    s = page_slide('qr_refs', 'R-1', [('참고 문헌', INK)])
    column(s, 'qr/l', 70, 100, 550, REFS_L)
    column(s, 'qr/r', 660, 100, 550, REFS_R)
    return s


def s_photo():
    return frame(AX.a_credits(), 'R-2')


def s_photo2():
    return frame(N.s_credits2(), 'R-3')


PAGES = [
    Page('R-1', '참고 문헌', s_refs, plain=True, a='각주에 적은 논문과 자료를 갈래별로 모은 장입니다.'),
    Page('R-2', '사진 출처 (How it works)', s_photo, plain=True, a='How it works에 쓴 사진의 출처입니다.'),
    Page('R-3', '사진과 음악 출처', s_photo2, plain=True, a='마무리 장과 6쪽에 쓴 사진, 모션그래픽에 쓴 음악의 출처입니다.'),
]
