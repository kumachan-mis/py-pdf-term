import os
import json
from glob import iglob
from typing import List, Iterator

from scripts.settings import PDF_DIR, XML_DIR, CANDIDATE_DIR, METHODS_DIR, TECHTERM_DIR
from pdf_slides_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from pdf_slides_term.methods import DomainTermRanking


def generate_pdf_path() -> Iterator[str]:
    return iglob(os.path.join(PDF_DIR, "**", "*.pdf"), recursive=True)


def pdf_to_xml_path(pdf_path: str) -> str:
    abs_dir_path, pdf_file_name = os.path.split(pdf_path)
    rel_dir_path = os.path.relpath(abs_dir_path, PDF_DIR)
    noext_file_name = os.path.splitext(pdf_file_name)[0]
    return os.path.join(XML_DIR, rel_dir_path, f"{noext_file_name}.xml")


def pdf_to_candidate_path(pdf_path: str) -> str:
    abs_dir_path, pdf_file_name = os.path.split(pdf_path)
    rel_dir_path = os.path.relpath(abs_dir_path, PDF_DIR)
    noext_file_name = os.path.splitext(pdf_file_name)[0]
    return os.path.join(CANDIDATE_DIR, rel_dir_path, f"{noext_file_name}.json")


def pdf_to_techterm_path(pdf_path: str, method_name: str) -> str:
    abs_dir_path, pdf_file_name = os.path.split(pdf_path)
    rel_dir_path = os.path.relpath(abs_dir_path, PDF_DIR)
    noext_file_name = os.path.splitext(pdf_file_name)[0]
    return os.path.join(
        TECHTERM_DIR, rel_dir_path, noext_file_name, f"{method_name}.json"
    )


def get_domains() -> List[str]:
    return list(
        filter(
            lambda dir_name: not dir_name.startswith(".")
            and os.path.isdir(os.path.join(PDF_DIR, dir_name)),
            os.listdir(PDF_DIR),
        )
    )


def generate_domain_candidates() -> Iterator[DomainCandidateTermList]:
    domains = get_domains()
    for domain in domains:
        pdfs = []
        json_path_pattern = os.path.join(CANDIDATE_DIR, domain, "**", "*.json")
        for json_path in iglob(json_path_pattern, recursive=True):
            with open(json_path, "r") as f:
                obj = json.load(f)
            pdfs.append(PDFCandidateTermList.from_json(obj))

        yield DomainCandidateTermList(domain, pdfs)


def generate_domain_term_ranking(method_name: str) -> Iterator[DomainTermRanking]:
    domains = get_domains()
    for domain in domains:
        json_path = os.path.join(METHODS_DIR, domain, f"{method_name}.json")
        with open(json_path, "r") as f:
            obj = json.load(f)
        yield DomainTermRanking.from_json(obj)
