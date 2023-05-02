from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.methods import MCValueMethod


def test_mcvalue_method_japanese() -> None:
    extractor = CandidateTermExtractor()
    method = MCValueMethod()

    candidates = extractor.extract_from_text(
        "モデル、設計モデル、設計モデル、モデル変換、モデル変換、実装、実装、実装、実装、実装"
    )
    expected_candidates_lemma = [
        "モデル",
        "設計モデル",
        "設計モデル",
        "モデル変換",
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
    assert method_ranking.domain == "test"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["実装"] >= score_dict["モデル"]
    # "実装" is more appropriate as an independent term,
    # not as a part of collocations than "モデル"
    assert score_dict["モデル変換"] >= score_dict["モデル"]
    # "モデル変換" is more appropriate as an independent term,
    # not as a part of collocations than "モデル"
    # even if "モデル" appears more frequently than "モデル変換"


def test_mcvalue_method_english() -> None:
    extractor = CandidateTermExtractor()
    method = MCValueMethod()

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
    assert method_ranking.domain == "test"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["implementation"] >= score_dict["model"]
    # "implementation" is more appropriate as an independent term,
    # not as a part of collocations than "model"
    assert score_dict["model transformation"] >= score_dict["model transformation"]
    # "model transformation" is more appropriate as an independent term,
    # not as a part of collocations than "model"
    # even if "model" appears more frequently than "model transformation"
