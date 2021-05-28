from py_slides_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_slides_term.methods import FLRHMethod


def test_flrh_method() -> None:
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
            "test",
            [
                PDFCandidateTermList(
                    "test/slide.pdf",
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
    assert score_dict["モデル"] >= score_dict["実装"]
