from typing import Dict

import pytest

from py_slides_term.analysis import TermLeftRightFrequencyAnalyzer
from py_slides_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)


@pytest.fixture
def extractor() -> CandidateTermExtractor:
    return CandidateTermExtractor()


def test_lr_freq(extractor: CandidateTermExtractor) -> None:
    analyzer = TermLeftRightFrequencyAnalyzer()
    candidates = extractor.extract_from_text(
        "Processor,"
        "Unit,"
        "Central processing unit,"
        "Microprocessor,"
        "Application-specific instruction set processor,"
        "Graphics processing unit,"
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
        "floating-point unit",
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
                    "test/slide1.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    expected_left_freq: Dict[str, Dict[str, int]] = {
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
        "floating": dict(),
        "point": dict(),
        "network": dict(),
        "multi": dict(),
        "core": dict(),
        "front": dict(),
        "end": dict(),
        "-": dict(),
    }
    expected_right_freq: Dict[str, Dict[str, int]] = {
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
        "floating": dict(),
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
