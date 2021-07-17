from py_pdf_term.candidates import (
    CandidateTermExtractor,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.stylings import PDFStylingScoreList
from py_pdf_term.techterms import TechnicalTermExtractor


def test_extractor() -> None:
    techterm_extractor = TechnicalTermExtractor(max_num_terms=4, acceptance_rate=0.5)
    candidate_extractor = CandidateTermExtractor()
    p1_candidates = candidate_extractor.extract_from_text(
        "OSI参照モデル（OSI reference model）は、"
        "OSIにおいて「コンピュータの持つべき」だとされた、"
        "通信機能を階層構造に分割したモデルである。"
    )
    p1_expected_candidates_lemma = [
        "osi参照モデル",
        "osi reference model",
        "osi",
        "コンピュータ",
        "通信機能",
        "階層構造",
        "分割",
        "モデル",
    ]
    assert list(map(lambda c: c.lemma(), p1_candidates)) == p1_expected_candidates_lemma

    p2_candidates = candidate_extractor.extract_from_text(
        "国際標準化機構 (ISO) によって制定された、ネットワーク構造の設計方針"
        "「開放型システム間相互接続 (Open Systems Interconnection)」に基づいて"
        "7階層（レイヤー）がある"
    )
    p2_expected_candidates_lemma = [
        "国際標準化機構",
        "iso",
        "制定",
        "ネットワーク構造",
        "設計方針",
        "ネットワーク構造の設計方針",
        "開放型システム間相互接続",
        "open systems interconnection",
        "7階層",
        "レイヤー",
    ]
    assert list(map(lambda c: c.lemma(), p2_candidates)) == p2_expected_candidates_lemma

    page_candidates = PDFCandidateTermList(
        "test/test.pdf",
        [
            PageCandidateTermList(1, p1_candidates),
            PageCandidateTermList(2, p2_candidates),
        ],
    )
    method_ranking = MethodTermRanking.from_dict(
        {
            "domain": "test",
            "ranking": [
                {"term": "osi参照モデル", "score": 18.0},
                {"term": "osi reference model", "score": 17.0},
                {"term": "osi", "score": 16.0},
                {"term": "コンピュータ", "score": 15.0},
                {"term": "通信機能", "score": 14.0},
                {"term": "階層構造", "score": 13.0},
                {"term": "分割", "score": 12.0},
                {"term": "モデル", "score": 11.0},
                {"term": "国際標準化機構", "score": 10.0},
                # ============== (acceptance_rate border) ============== #
                {"term": "iso", "score": 9.0},
                {"term": "制定", "score": 8.0},
                {"term": "ネットワーク構造", "score": 7.0},
                {"term": "設計方針", "score": 6.0},
                {"term": "ネットワーク構造の設計方針", "score": 5.0},
                {"term": "開放型システム間相互接続", "score": 4.0},
                {"term": "open systems interconnection", "score": 3.0},
                {"term": "7階層", "score": 2.0},
                {"term": "レイヤー", "score": 1.0},
            ],
        }
    )
    pdf_styling_scores = PDFStylingScoreList.from_dict(
        {
            "pdf_path": "test/test.pdf",
            "pages": [
                {
                    "page_num": 1,
                    "ranking": [
                        {"term": term, "score": 1.0}
                        for term in p1_expected_candidates_lemma
                    ],
                },
                {
                    "page_num": 2,
                    "ranking": [
                        {"term": term, "score": 1.0}
                        for term in p2_expected_candidates_lemma
                    ],
                },
            ],
        }
    )
    techterms = techterm_extractor.extract_from_pdf(
        page_candidates, method_ranking, pdf_styling_scores
    )

    assert techterms.pdf_path == "test/test.pdf"
    assert len(techterms.pages) == 2

    page = techterms.pages[0]
    assert page.page_num == 1
    p1_expected_techterms = ["OSI参照モデル", "OSI reference model", "OSI", "コンピュータ"]
    assert list(map(lambda t: t.term, page.terms)) == p1_expected_techterms
    # max_num_terms should work

    page = techterms.pages[1]
    assert page.page_num == 2
    p2_expected_techterms = ["国際標準化機構"]
    assert list(map(lambda t: t.term, page.terms)) == p2_expected_techterms
    # acceptance_rate should work
