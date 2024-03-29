from py_pdf_term.analysis import TermLeftRightFrequencyAnalyzer
from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)


def test_lr_freq() -> None:
    extractor = CandidateTermExtractor()
    analyzer = TermLeftRightFrequencyAnalyzer()
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
    expected_left_freq: dict[str, dict[str, int]] = {
        "processor": {"set": 1, "signal": 1, "network": 1, "core": 1, "end": 1},
        "unit": {"processing": 3, "point": 1},
        "processing": {"central": 1, "graphic": 1, "physics": 1},
        "central": dict(),
        "microprocessor": dict(),
        "application": dict(),
        "specific": dict(),
        "instruction": {"specific": 1},
        "set": {"instruction": 1},
        "graphic": dict(),
        "physics": dict(),
        "digital": dict(),
        "signal": {"digital": 1},
        "coprocessor": dict(),
        "float": dict(),
        "point": dict(),
        "network": dict(),
        "multi": dict(),
        "core": dict(),
        "front": dict(),
        "end": dict(),
        "-": dict(),
    }
    expected_right_freq: dict[str, dict[str, int]] = {
        "processor": dict(),
        "unit": dict(),
        "processing": {"unit": 3},
        "central": {"processing": 1},
        "microprocessor": dict(),
        "application": dict(),
        "specific": {"instruction": 1},
        "instruction": {"set": 1},
        "set": {"processor": 1},
        "graphic": {"processing": 1},
        "physics": {"processing": 1},
        "digital": {"signal": 1},
        "signal": {"processor": 1},
        "coprocessor": dict(),
        "float": dict(),
        "point": {"unit": 1},
        "network": {"processor": 1},
        "multi": dict(),
        "core": {"processor": 1},
        "front": dict(),
        "end": {"processor": 1},
        "-": dict(),
    }
    assert result.domain == "test"
    assert result.left_freq == expected_left_freq
    assert result.right_freq == expected_right_freq
