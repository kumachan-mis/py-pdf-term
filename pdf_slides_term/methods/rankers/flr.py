from math import log10

from pdf_slides_term.methods.rankers.base import BaseSingleDomainRanker
from pdf_slides_term.methods.rankingdata.flr import FLRRakingData
from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


class FLRRanker(BaseSingleDomainRanker[FLRRakingData]):
    # public
    def __init__(self):
        pass

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRRakingData
    ) -> DomainTermRanking:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(candidate, ranking_data),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self, candidate: TechnicalTerm, ranking_data: FLRRakingData
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        term_maxsize_score = (
            log10(ranking_data.term_maxsize[candidate_str])
            if ranking_data.term_maxsize is not None
            else 0.0
        )
        term_freq_score = log10(ranking_data.term_freq[candidate_str])

        concat_score = 0.0
        for morpheme in candidate.morphemes:
            morpheme_str = str(morpheme)
            left_score = sum(ranking_data.left_freq[morpheme_str].values())
            right_score = sum(ranking_data.right_freq[morpheme_str].values())
            concat_score += 0.5 * (log10(left_score + 1) + log10(right_score + 1))

        concat_score /= len(candidate.morphemes)

        score = term_maxsize_score + term_freq_score + concat_score
        return ScoredTerm(candidate_str, score)
