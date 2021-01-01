import os
import json
from argparse import ArgumentParser

from pdf_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
    MCValueMethod,
    TFIDFMethod,
    LFIDFMethod,
    FLRMethod,
    HITSMethod,
    FLRHMethod,
    MDPMethod,
)
from scripts.settings import METHODS_DIR
from scripts.utils import generate_domain_candidates


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
        method = MCValueMethod()
    elif args.tfidf:
        method_name = "tfidf"
        method = TFIDFMethod()
    elif args.lfidf:
        method_name = "lfidf"
        method = LFIDFMethod()
    elif args.flr:
        method_name = "flr"
        method = FLRMethod()
    elif args.hits:
        method_name = "hits"
        method = HITSMethod()
    elif args.flrh:
        method_name = "flrh"
        method = FLRHMethod()
    elif args.mdp:
        method_name = "mdp"
        method = MDPMethod(compile_scores=max)
    else:
        raise RuntimeError("unreachable statement")

    file_name = f"{method_name}.json"
    domain_candidates_list = generate_domain_candidates()

    # pyright:reportUnnecessaryIsInstance=false
    if isinstance(method, BaseSingleDomainRankingMethod):
        for candidates in domain_candidates_list:
            ranking_path = os.path.join(METHODS_DIR, candidates.domain, file_name)
            print(f"main_methods.py: creating {ranking_path} ...")

            ranking_dir_name = os.path.dirname(ranking_path)
            os.makedirs(ranking_dir_name, exist_ok=True)
            term_ranking = method.rank_terms(candidates)

            with open(ranking_path, "w") as ranking_file:
                json_obj = term_ranking.to_json()
                json.dump(json_obj, ranking_file, ensure_ascii=False, indent=2)
    elif isinstance(method, BaseMultiDomainRankingMethod):
        print("main_methods.py: preprocessing ...")

        domain_candidates_list = list(domain_candidates_list)
        term_ranking_list = method.rank_terms(domain_candidates_list)
        for term_ranking in term_ranking_list:
            ranking_path = os.path.join(METHODS_DIR, term_ranking.domain, file_name)
            print(f"main_methods.py: creating {ranking_path} ...")

            ranking_dir_name = os.path.dirname(ranking_path)
            os.makedirs(ranking_dir_name, exist_ok=True)

            with open(ranking_path, "w") as ranking_file:
                json_obj = term_ranking.to_json()
                json.dump(json_obj, ranking_file, ensure_ascii=False, indent=2)
