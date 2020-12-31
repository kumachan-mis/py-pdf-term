import os
import json
from argparse import ArgumentParser
from glob import iglob
from typing import List, Iterator

from pdf_slides_term.techterms.extractor import TechnicalTermExtractor
from pdf_slides_term.candidates.data import (
    DomainCandidateTermList,
    XMLCandidateTermList,
)
from pdf_slides_term.methods.data import DomainTermRanking
from scripts.settings import XML_DIR, CANDIDATE_DIR, METHODS_DIR, TECHTERM_DIR


def get_domains() -> List[str]:
    return list(
        filter(
            lambda dir_name: not dir_name.startswith(".")
            and os.path.isdir(os.path.join(CANDIDATE_DIR, dir_name)),
            os.listdir(CANDIDATE_DIR),
        )
    )


def generate_domain_candidates() -> Iterator[DomainCandidateTermList]:
    domains = get_domains()
    for domain in domains:
        xmls = []
        json_path_pattern = os.path.join(CANDIDATE_DIR, domain, "**", "*.json")
        for json_path in iglob(json_path_pattern, recursive=True):
            with open(json_path, "r") as f:
                obj = json.load(f)
            xmls.append(XMLCandidateTermList.from_json(obj))

        yield DomainCandidateTermList(domain, xmls)


def generate_domain_term_ranking(method_name: str) -> Iterator[DomainTermRanking]:
    domains = get_domains()
    for domain in domains:
        json_path = os.path.join(METHODS_DIR, domain, f"{method_name}.json")
        with open(json_path, "r") as f:
            obj = json.load(f)
        yield DomainTermRanking.from_json(obj)


def xml_path_to_techterm_path(xml_path: str, method_name: str) -> str:
    abs_dir_path, xml_file_name = os.path.split(xml_path)
    rel_dir_path = os.path.relpath(abs_dir_path, XML_DIR)
    noext_file_name = os.path.splitext(xml_file_name)[0]
    return os.path.join(
        TECHTERM_DIR, rel_dir_path, noext_file_name, f"{method_name}.json"
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mcvalue", help="use MC-Value method", action="store_true")
    group.add_argument("--tfidf", help="use TF-IDF method", action="store_true")
    group.add_argument("--lfidf", help="use LF-IDF method", action="store_true")
    group.add_argument("--flr", help="use FLR method", action="store_true")
    group.add_argument("--hits", help="use HITS method", action="store_true")
    group.add_argument("--flrh", help="use FLRH method", action="store_true")
    group.add_argument("--mdp", help="use MDP method", action="store_true")
    args = parser.parse_args()

    if args.mcvalue:
        method_name = "mcvalue"
    elif args.tfidf:
        method_name = "tfidf"
    elif args.lfidf:
        method_name = "lfidf"
    elif args.flr:
        method_name = "flr"
    elif args.hits:
        method_name = "hits"
    elif args.flrh:
        method_name = "flrh"
    elif args.mdp:
        method_name = "mdp"
    else:
        raise RuntimeError("unreachable statement")

    extractor = TechnicalTermExtractor()

    domain_candidates_generator = generate_domain_candidates()
    domain_term_ranking_generator = generate_domain_term_ranking(method_name)
    for domain_candidates, domain_term_ranking in zip(
        domain_candidates_generator, domain_term_ranking_generator
    ):
        domain_techterm_list = extractor.extract_from_domain(
            domain_candidates, domain_term_ranking
        )

        for xml_techterm_list in domain_techterm_list.xmls:
            techterm_path = xml_path_to_techterm_path(
                xml_techterm_list.xml_path, method_name
            )
            techterm_dir_name = os.path.dirname(techterm_path)
            os.makedirs(techterm_dir_name, exist_ok=True)

            with open(techterm_path, "w") as techterm_file:
                json_obj = xml_techterm_list.to_json()
                json.dump(json_obj, techterm_file, ensure_ascii=False, indent=2)
