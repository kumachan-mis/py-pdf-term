import os
import json
from argparse import ArgumentParser
from glob import iglob
from typing import List

from pdf_slides_term.methods.flr import FLRMethod
from pdf_slides_term.candidates.data import (
    DomainCandidateTermList,
    XMLCandidateTermList,
)
from scripts.settings import DATASET_DIR


CANDIDATE_DIR = os.path.join(DATASET_DIR, "candidate")
METHODS_DIR = os.path.join(DATASET_DIR, "methods")
METHODS = ["flr"]


def fetch_domain_candidates_list() -> List[DomainCandidateTermList]:
    domains = list(
        filter(
            lambda dir_name: not dir_name.startswith(".")
            and os.path.isdir(os.path.join(CANDIDATE_DIR, dir_name)),
            os.listdir(CANDIDATE_DIR),
        )
    )

    domain_candidates_list = []
    for domain in domains:
        xmls = []
        json_path_pattern = os.path.join(CANDIDATE_DIR, domain, "**", "*.json")
        for json_path in iglob(json_path_pattern, recursive=True):
            with open(json_path, "r") as f:
                obj = json.load(f)
            xmls.append(XMLCandidateTermList.from_json(obj))

        domain_candidates_list.append(DomainCandidateTermList(domain, xmls))

    return domain_candidates_list


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--flr", help="use FLR method", action="store_true")
    group.add_argument("--hits", help="use HITS method", action="store_true")
    args = parser.parse_args()

    if args.flr:
        method_name = "flr"
        method = FLRMethod()
    elif args.hits:
        method_name = "hits"

    ranking_file_name = f"{method_name}.json"
    domain_candidates_list = fetch_domain_candidates_list()
    for candidates in domain_candidates_list:
        ranking_path = os.path.join(METHODS_DIR, candidates.domain, ranking_file_name)
        ranking_dir_name = os.path.dirname(ranking_path)
        os.makedirs(ranking_dir_name, exist_ok=True)
        term_ranking = method.rank_terms(candidates)

        with open(ranking_path, "w") as ranking_file:
            json_obj = term_ranking.to_json()
            json.dump(json_obj, ranking_file, ensure_ascii=False, indent=2)
