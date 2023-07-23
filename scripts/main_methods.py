import json
import os
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any

from py_pdf_term.methods import (
    BaseMultiDomainRankingMethod,
    BaseSingleDomainRankingMethod,
    FLRHMethod,
    FLRMethod,
    HITSMethod,
    MCValueMethod,
    MDPMethod,
    TFIDFMethod,
)
from scripts.settings import METHODS_DIR
from scripts.utils import generate_domain_candidates, get_domains, relpath_from_basedir

script_name = os.path.basename(__file__)


@dataclass(frozen=True)
class CommandLineArguments:
    method_name: str
    method: BaseSingleDomainRankingMethod[Any] | BaseMultiDomainRankingMethod[Any]


def parse_command_line_argments() -> CommandLineArguments:
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mcvalue", help="use MC-Value method", action="store_true")
    group.add_argument("--tfidf", help="use TF-IDF method", action="store_true")
    group.add_argument("--flr", help="use FLR method", action="store_true")
    group.add_argument("--hits", help="use HITS method", action="store_true")
    group.add_argument("--flrh", help="use FLRH method", action="store_true")
    group.add_argument("--mdp", help="use MDP method", action="store_true")
    args = parser.parse_args()

    if args.mcvalue:
        return CommandLineArguments("mcvalue", MCValueMethod())
    elif args.tfidf:
        return CommandLineArguments("tfidf", TFIDFMethod())
    elif args.flr:
        return CommandLineArguments("flr", FLRMethod())
    elif args.hits:
        return CommandLineArguments("hits", HITSMethod())
    elif args.flrh:
        return CommandLineArguments("flrh", FLRHMethod())
    elif args.mdp:
        return CommandLineArguments("mdp", MDPMethod())
    else:
        raise RuntimeError("unreachable statement")


def run_single_domain_method(
    method_name: str, method: BaseSingleDomainRankingMethod[Any]
) -> None:
    file_name = f"{method_name}.json"
    domains = get_domains()
    domain_candidates_list = generate_domain_candidates(domains)

    for candidates in domain_candidates_list:
        ranking_path = os.path.join(METHODS_DIR, candidates.domain, file_name)
        print(f"{script_name}: creating {relpath_from_basedir(ranking_path)} ...")

        term_ranking = method.rank_terms(candidates)

        ranking_dir_name = os.path.dirname(ranking_path)
        os.makedirs(ranking_dir_name, exist_ok=True)

        with open(ranking_path, "w") as ranking_file:
            dict_obj = term_ranking.to_dict()
            json.dump(dict_obj, ranking_file, ensure_ascii=False, indent=2)


def run_multi_domain_method(
    method_name: str, method: BaseMultiDomainRankingMethod[Any]
) -> None:
    file_name = f"{method_name}.json"
    domains = get_domains()
    domain_candidates_list = generate_domain_candidates(domains)

    print(f"{script_name}: preprocessing ...")

    domain_candidates_list = list(domain_candidates_list)
    term_ranking_list = method.rank_terms(domain_candidates_list)
    for term_ranking in term_ranking_list:
        ranking_path = os.path.join(METHODS_DIR, term_ranking.domain, file_name)
        print(f"{script_name}: creating {relpath_from_basedir(ranking_path)} ...")

        ranking_dir_name = os.path.dirname(ranking_path)
        os.makedirs(ranking_dir_name, exist_ok=True)

        with open(ranking_path, "w") as ranking_file:
            dict_obj = term_ranking.to_dict()
            json.dump(dict_obj, ranking_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    args = parse_command_line_argments()

    match args.method:
        case BaseSingleDomainRankingMethod():
            run_single_domain_method(args.method_name, args.method)
        case BaseMultiDomainRankingMethod():
            run_multi_domain_method(args.method_name, args.method)
