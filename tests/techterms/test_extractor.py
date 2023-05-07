from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.stylings import DomainStylingScoreList, PDFStylingScoreList
from py_pdf_term.techterms import TechnicalTermExtractor


def test_extract_from_domain() -> None:
    techterm_extractor = TechnicalTermExtractor(max_num_terms=4, acceptance_rate=0.5)
    candidate_extractor = CandidateTermExtractor()
    p1_candidates = candidate_extractor.extract_from_text(
        "A type system is a logical system which comprise a set of rules "
        "that assigns a property called a type (e.g., integer, floating point, string) "
        "to every term."
    )
    p1_expected_candidates_lemma = [
        "type system",
        "logical system",
        "set",
        "rule",
        "set of rule",
        "property",
        "type",
        "integer",
        "float point",
        "string",
        "term",
    ]
    assert list(map(lambda c: c.lemma(), p1_candidates)) == p1_expected_candidates_lemma

    p2_candidates = candidate_extractor.extract_from_text(
        "Usually the terms are various constructs of a computer program, "
        "such as variables, expressions, functions, or modules."
    )
    p2_expected_candidates_lemma = [
        "term",
        "various construct",
        "computer program",
        "variable",
        "expression",
        "function",
        "module",
    ]
    assert list(map(lambda c: c.lemma(), p2_candidates)) == p2_expected_candidates_lemma

    domain_candidates = DomainCandidateTermList(
        "test",
        [
            PDFCandidateTermList(
                "test/test.pdf",
                [
                    PageCandidateTermList(1, p1_candidates),
                    PageCandidateTermList(2, p2_candidates),
                ],
            )
        ],
    )

    method_ranking = MethodTermRanking.from_dict(
        {
            "domain": "test",
            "ranking": [
                {"term": "type system", "score": 18.0},
                {"term": "type", "score": 17.0},
                {"term": "integer", "score": 16.0},
                {"term": "float point", "score": 15.0},
                {"term": "string", "score": 14.0},
                {"term": "term", "score": 13.0},
                {"term": "set of rule", "score": 12.0},
                {"term": "computer program", "score": 11.0},
                {"term": "set", "score": 10.0},
                {"term": "rule", "score": 9.0},
                # ============== (acceptance_rate border) ============== #
                {"term": "variable", "score": 8.0},
                {"term": "expression", "score": 7.0},
                {"term": "function", "score": 6.0},
                {"term": "module", "score": 5.0},
                {"term": "various construct", "score": 4.0},
                {"term": "logical system", "score": 3.0},
                {"term": "property", "score": 2.0},
            ],
        }
    )
    domain_styling_scores = DomainStylingScoreList.from_dict(
        {
            "domain": "test",
            "pdfs": [
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
            ],
        }
    )
    techterms = techterm_extractor.extract_from_domain(
        domain_candidates, method_ranking, domain_styling_scores
    )

    assert techterms.domain == "test"
    assert len(techterms.pdfs) == 1

    pdf = techterms.pdfs[0]
    assert pdf.pdf_path == "test/test.pdf"
    assert len(pdf.pages) == 2

    page = pdf.pages[0]
    assert page.page_num == 1
    p1_expected_techterms = ["type system", "type", "integer", "floating point"]
    assert list(map(lambda t: t.term, page.terms)) == p1_expected_techterms
    # max_num_terms should work

    page = pdf.pages[1]
    assert page.page_num == 2
    p2_expected_techterms = ["terms", "computer program"]
    assert list(map(lambda t: t.term, page.terms)) == p2_expected_techterms
    # acceptance_rate should work


def test_extract_from_pdf() -> None:
    techterm_extractor = TechnicalTermExtractor(max_num_terms=4, acceptance_rate=0.5)
    candidate_extractor = CandidateTermExtractor()
    p1_candidates = candidate_extractor.extract_from_text(
        "OSI参照モデル(OSI reference model)は、"
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
        "7階層(レイヤー)がある"
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
                {"term": "iso", "score": 9.0},
                # ============== (acceptance_rate border) ============== #
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
    p2_expected_techterms = ["国際標準化機構", "ISO"]
    assert list(map(lambda t: t.term, page.terms)) == p2_expected_techterms
    # acceptance_rate should work
