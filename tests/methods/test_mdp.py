from py_slides_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_slides_term.methods import MDPMethod


def test_mdp_method() -> None:
    extractor = CandidateTermExtractor()
    method = MDPMethod()

    their_candidates = extractor.extract_from_text("主成分分析、主成分分析、問題、問題")
    expected_candidates_lemma = ["主成分分析", "主成分分析", "問題", "問題"]
    assert list(map(lambda c: c.lemma(), their_candidates)) == expected_candidates_lemma

    our_candidates = extractor.extract_from_text("パイプライン、パイプライン、IF、問題、問題")
    expected_candidates_lemma = ["パイプライン", "パイプライン", "if", "問題", "問題"]
    assert list(map(lambda c: c.lemma(), our_candidates)) == expected_candidates_lemma

    method_ranking = method.rank_domain_terms(
        "ourtest",
        [
            DomainCandidateTermList(
                "theirtest",
                [
                    PDFCandidateTermList(
                        "theirtest/slide.pdf",
                        [
                            PageCandidateTermList(1, their_candidates),
                        ],
                    )
                ],
            ),
            DomainCandidateTermList(
                "ourtest",
                [
                    PDFCandidateTermList(
                        "ourtest/slide.pdf",
                        [
                            PageCandidateTermList(1, our_candidates),
                        ],
                    )
                ],
            ),
        ],
    )
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "ourtest"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["パイプライン"] >= score_dict["if"]
    # "パイプライン" appears more frequently than "IF"
    assert score_dict["パイプライン"] >= score_dict["問題"]
    # "パイプライン" is more domain-specific than "問題"
