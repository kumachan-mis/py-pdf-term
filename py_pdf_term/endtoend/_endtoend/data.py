from dataclasses import dataclass


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
    pdf_paths: list[str]

    @classmethod
    def validate(cls, domain_pdfs: "DomainPDFList") -> None:
        if not domain_pdfs.domain:
            raise ValueError("domain must not be empty")
        if not domain_pdfs.pdf_paths:
            raise ValueError("pdf_paths must not be empty")
