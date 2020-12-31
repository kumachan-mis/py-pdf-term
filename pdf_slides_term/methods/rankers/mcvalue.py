from math import log10
from pdf_slides_term.methods.rankers.base import BaseSingleDomainRanker
from pdf_slides_term.methods.rankingdata.mcvalue import MCValueRakingData
from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.share.utils import extended_log10


class MCValueRanker(BaseSingleDomainRanker[MCValueRakingData]):
    # public
    def __init__(self):
        pass

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: MCValueRakingData,
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
        self, candidate: TechnicalTerm, ranking_data: MCValueRakingData
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        term_freq = ranking_data.term_freq[candidate_str]
        container_freqs = ranking_data.container_freqs[candidate_str]
        container_freq_ave = sum(container_freqs.values()) / len(container_freqs)

        term_len_score = log10(len(candidate.morphemes))
        freq_score = extended_log10(term_freq - container_freq_ave)
        term_maxsize_score = (
            log10(ranking_data.term_maxsize[candidate_str])
            if ranking_data.term_maxsize is not None
            else 0.0
        )

        score = term_len_score + freq_score + term_maxsize_score
        return ScoredTerm(candidate_str, score)
