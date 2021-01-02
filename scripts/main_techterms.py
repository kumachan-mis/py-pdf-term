import os
import json
from argparse import ArgumentParser

from py_slides_term.techterms import TechnicalTermExtractor
from scripts.utils import (
    generate_domain_candidates,
    generate_domain_term_ranking,
    pdf_to_techterm_path,
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

    domain_candidates_list = generate_domain_candidates()
    domain_term_ranking_list = generate_domain_term_ranking(method_name)
    ziped_list = zip(domain_candidates_list, domain_term_ranking_list)

    for domain_candidates, domain_term_ranking in ziped_list:
        domain_techterm_list = extractor.extract_from_domain(
            domain_candidates, domain_term_ranking
        )

        for pdf_techterm_list in domain_techterm_list.pdfs:
            techterm_path = pdf_to_techterm_path(
                pdf_techterm_list.pdf_path, method_name
            )
            print(f"main_techterms.py: creating {techterm_path} ...")

            techterm_dir_name = os.path.dirname(techterm_path)
            os.makedirs(techterm_dir_name, exist_ok=True)

            with open(techterm_path, "w") as techterm_file:
                json_obj = pdf_techterm_list.to_json()
                json.dump(json_obj, techterm_file, ensure_ascii=False, indent=2)
