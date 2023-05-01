from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DomainPDFList:
    """Domain name and PDF file paths of the domain

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        pdf_paths:
            PDF file paths of the domain.
    """

    domain: str
    pdf_paths: List[str]
