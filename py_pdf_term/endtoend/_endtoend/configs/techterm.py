from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class TechnicalTermLayerConfig(BaseLayerConfig):
    """Configuration for a technical term layer.

    Args
    ----
        max_num_terms:
            Maximum number of terms in a page of a PDF file to be extracted. The N-best
            candidates are extracted as technical terms. The default value is 10.
        acceptance_rate:
            Acceptance rate of the ranking method scores. The candidates whose
            ranking method scores are lower than the acceptance rate are filtered out
            even if they are in the N-best candidates. The default value is 0.75.
    """

    max_num_terms: int = 10
    acceptance_rate: float = 0.75
