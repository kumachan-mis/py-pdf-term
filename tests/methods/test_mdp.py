from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.methods import MDPMethod


def test_mdp_method_japanese() -> None:
    extractor = CandidateTermExtractor()
    method = MDPMethod()

    computer_architecture_candidates = extractor.extract_from_text(
        "パイプライン、パイプライン、IF、問題、問題"
    )
    expected_computer_architecture_candidates_lemma = [
        "パイプライン",
        "パイプライン",
        "if",
        "問題",
        "問題",
    ]
    assert (
        list(map(lambda c: c.lemma(), computer_architecture_candidates))
        == expected_computer_architecture_candidates_lemma
    )

    pattern_recognition_candidates = extractor.extract_from_text(
        "主成分分析、主成分分析、PCA、問題、問題"
    )
    expected_pattern_recognition_candidates_lemma = [
        "主成分分析",
        "主成分分析",
        "pca",
        "問題",
        "問題",
    ]
    assert (
        list(map(lambda c: c.lemma(), pattern_recognition_candidates))
        == expected_pattern_recognition_candidates_lemma
    )

    domain_candidates_list = [
        DomainCandidateTermList(
            "コンピュータアーキテクチャ",
            [
                PDFCandidateTermList(
                    "pipelining.pdf",
                    [
                        PageCandidateTermList(1, computer_architecture_candidates),
                    ],
                )
            ],
        ),
        DomainCandidateTermList(
            "パターン認識",
            [
                PDFCandidateTermList(
                    "principal_component_analysis.pdf",
                    [
                        PageCandidateTermList(1, pattern_recognition_candidates),
                    ],
                )
            ],
        ),
    ]

    method_ranking = method.rank_domain_terms("コンピュータアーキテクチャ", domain_candidates_list)
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "コンピュータアーキテクチャ"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(
        expected_computer_architecture_candidates_lemma
    )
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["パイプライン"] >= score_dict["if"]
    # "パイプライン" appears more frequently than "IF"
    assert score_dict["パイプライン"] >= score_dict["問題"]
    # "パイプライン" is more domain-specific than "問題"

    method_ranking = method.rank_domain_terms("パターン認識", domain_candidates_list)
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "パターン認識"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_pattern_recognition_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["主成分分析"] >= score_dict["pca"]
    # "主成分分析" appears more frequently than "PCA"
    assert score_dict["主成分分析"] >= score_dict["問題"]
    # "主成分分析" is more domain-specific than "問題"


def test_mdp_method_english() -> None:
    extractor = CandidateTermExtractor()
    method = MDPMethod()

    computer_architecture_candidates = extractor.extract_from_text(
        "pipelining, pipelining, memory, problem, problem"
    )
    expected_computer_architecture_candidates_lemma = [
        "pipeline",
        "pipeline",
        "memory",
        "problem",
        "problem",
    ]
    assert (
        list(map(lambda c: c.lemma(), computer_architecture_candidates))
        == expected_computer_architecture_candidates_lemma
    )

    pattern_recognition_candidates = extractor.extract_from_text(
        "principal component analysis, principal component analysis, PCA,"
        "problem, problem"
    )
    expected_pattern_recognition_candidates_lemma = [
        "principal component analysis",
        "principal component analysis",
        "pca",
        "problem",
        "problem",
    ]
    assert (
        list(map(lambda c: c.lemma(), pattern_recognition_candidates))
        == expected_pattern_recognition_candidates_lemma
    )

    domain_candidates_list = [
        DomainCandidateTermList(
            "Computer Architecture",
            [
                PDFCandidateTermList(
                    "pipelining.pdf",
                    [
                        PageCandidateTermList(1, computer_architecture_candidates),
                    ],
                )
            ],
        ),
        DomainCandidateTermList(
            "Pattern Recognition",
            [
                PDFCandidateTermList(
                    "principal_component_analysis.pdf",
                    [
                        PageCandidateTermList(1, pattern_recognition_candidates),
                    ],
                )
            ],
        ),
    ]

    method_ranking = method.rank_domain_terms(
        "Computer Architecture", domain_candidates_list
    )
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "Computer Architecture"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(
        expected_computer_architecture_candidates_lemma
    )
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["pipeline"] >= score_dict["memory"]
    # "pipeline" appears more frequently than "memory"
    assert score_dict["pipeline"] >= score_dict["problem"]
    # "pipeline" is more domain-specific than "problem"

    method_ranking = method.rank_domain_terms(
        "Pattern Recognition", domain_candidates_list
    )
    ranking = method_ranking.ranking
    score_dict = dict(map(lambda e: (e.term, e.score), ranking))
    assert method_ranking.domain == "Pattern Recognition"
    assert len(ranking) == len(score_dict)
    assert set(score_dict.keys()) == set(expected_pattern_recognition_candidates_lemma)
    assert ranking == sorted(ranking, key=lambda e: e.score, reverse=True)

    assert score_dict["principal component analysis"] >= score_dict["pca"]
    # "principal component analysis" appears more frequently than "PCA"
    assert score_dict["principal component analysis"] >= score_dict["problem"]
    # "principal component analysis" is more domain-specific than "problem"
