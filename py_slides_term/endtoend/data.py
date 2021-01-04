from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DomainPDFList:
    domain: str
    pdf_paths: List[str]
