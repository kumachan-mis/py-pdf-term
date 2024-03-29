from py_pdf_term.analysis import ContainerTermsAnalyzer
from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)


def test_container() -> None:
    extractor = CandidateTermExtractor()
    analyzer = ContainerTermsAnalyzer()
    candidates = extractor.extract_from_text(
        "Processor,"
        "Unit,"
        "Central processing unit,"
        "Microprocessor,"
        "Application-specific instruction set processor,"
        "Graphic processing unit,"
        "Physics processing unit,"
        "Digital signal processor,"
        "Coprocessor,"
        "Floating-point unit,"
        "Network processor,"
        "Multi-core processor,"
        "Front-end processor,"
    )
    expected_candidates_lemma = [
        "processor",
        "unit",
        "central processing unit",
        "microprocessor",
        "application-specific instruction set processor",
        "graphic processing unit",
        "physics processing unit",
        "digital signal processor",
        "coprocessor",
        "float-point unit",
        "network processor",
        "multi-core processor",
        "front-end processor",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    result = analyzer.analyze(
        DomainCandidateTermList(
            "test",
            [
                PDFCandidateTermList(
                    "test/test.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )

    expected_container_terms: dict[str, set[str]] = {
        "processor": {
            "application-specific instruction set processor",
            "digital signal processor",
            "network processor",
            "multi-core processor",
            "front-end processor",
        },
        "unit": {
            "central processing unit",
            "graphic processing unit",
            "physics processing unit",
            "float-point unit",
        },
        "central processing unit": set(),
        "microprocessor": set(),
        "application-specific instruction set processor": set(),
        "graphic processing unit": set(),
        "physics processing unit": set(),
        "digital signal processor": set(),
        "coprocessor": set(),
        "float-point unit": set(),
        "network processor": set(),
        "multi-core processor": set(),
        "front-end processor": set(),
    }
    assert result.domain == "test"
    assert result.container_terms == expected_container_terms
