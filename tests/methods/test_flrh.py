from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.methods import FLRHMethod


def test_flrh_method_japanese() -> None:
    extractor = CandidateTermExtractor()
    method = FLRHMethod()

    candidates = extractor.extract_from_text(
        "モデル、概念モデル、要求モデル、設計モデル、モデル変換、実装、実装、実装、実装、実装"
    )
    expected_candidates_lemma = [
        "モデル",
        "概念モデル",
        "要求モデル",
        "設計モデル",
        "モデル変換",
        "実装",
        "実装",
        "実装",
        "実装",
        "実装",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    method_ranking = method.rank_terms(
        DomainCandidateTermList(
            "ソフトウェア工学",
            [
                PDFCandidateTermList(
                    "software_engineering.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "ソフトウェア工学"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["モデル"] >= score_dict["実装"]
    # more compound terms are consist of "モデル" than "実装"


def test_flrh_method_in_english() -> None:
    extractor = CandidateTermExtractor()
    method = FLRHMethod()

    candidates = extractor.extract_from_text(
        "model, concept model, requirements model, design model, model transformation,"
        "implementation, implementation, implementation, implementation, implementation"
    )
    expected_candidates_lemma = [
        "model",
        "concept model",
        "requirement model",
        "design model",
        "model transformation",
        "implementation",
        "implementation",
        "implementation",
        "implementation",
        "implementation",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    method_ranking = method.rank_terms(
        DomainCandidateTermList(
            "Software Engineering",
            [
                PDFCandidateTermList(
                    "software_engineering.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "Software Engineering"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["model"] >= score_dict["implementation"]
    # more compound terms are consist of "model" than "implementation"
