import os
import json
from argparse import ArgumentParser

from py_slides_term import (
    PySlidesTermExtractor,
    CandidateLayerConfig,
    MethodLayerConfig,
)
from scripts.utils import (
    relpath_from_basedir,
    get_domains,
    generate_domain_pdfs,
    pdf_to_techterm_path,
)

script_name = os.path.basename(__file__)

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
        method_type = "single"
        method_name = "mcvalue"
        method = "py_slides_term.MCValueMethod"
    elif args.tfidf:
        method_type = "multi"
        method_name = "tfidf"
        method = "py_slides_term.TFIDFMethod"
    elif args.lfidf:
        method_type = "multi"
        method_name = "lfidf"
        method = "py_slides_term.LFIDFMethod"
    elif args.flr:
        method_type = "single"
        method_name = "flr"
        method = "py_slides_term.FLRMethod"
    elif args.hits:
        method_type = "single"
        method_name = "hits"
        method = "py_slides_term.HITSMethod"
    elif args.flrh:
        method_type = "single"
        method_name = "flrh"
        method = "py_slides_term.FLRHMethod"
    elif args.mdp:
        method_type = "multi"
        method_name = "mdp"
        method = "py_slides_term.MDPMethod"
    else:
        raise RuntimeError("unreachable statement")

    extractor = PySlidesTermExtractor(
        candidate_config=CandidateLayerConfig(
            cache="py_slides_term.CandidateLayerNoCache"
        ),
        method_config=MethodLayerConfig(
            method_type=method_type,
            method=method,
            ranking_cache="py_slides_term.MethodLayerRankingNoCache",
            data_cache="py_slides_term.MethodLayerDataNoCache",
        ),
    )

    file_name = f"{method_name}.json"
    domains = get_domains()

    if method_type == "single":
        domain_pdfs_list = generate_domain_pdfs(domains)
        for domain_pdfs in domain_pdfs_list:
            for pdf_path in domain_pdfs.pdf_paths:
                techterm_path = pdf_to_techterm_path(pdf_path, method_name)
                techterm_short_path = relpath_from_basedir(techterm_path)
                print(f"{script_name}: creating {techterm_short_path} ...")

                pdf_techterms = extractor.extract(
                    domain_pdfs.domain, pdf_path, single_domain_pdfs=domain_pdfs
                )

                techterm_dir_name = os.path.dirname(techterm_path)
                os.makedirs(techterm_dir_name, exist_ok=True)

                with open(techterm_path, "w") as techterm_file:
                    json_obj = pdf_techterms.to_json()
                    json.dump(json_obj, techterm_file, ensure_ascii=False, indent=2)

    elif method_type == "multi":
        domain_pdfs_list = list(generate_domain_pdfs(domains))
        for domain_pdfs in domain_pdfs_list:
            for pdf_path in domain_pdfs.pdf_paths:
                techterm_path = pdf_to_techterm_path(pdf_path, method_name)
                techterm_short_path = relpath_from_basedir(techterm_path)
                print(f"{script_name}: creating {techterm_short_path} ...")

                pdf_techterms = extractor.extract(
                    domain_pdfs.domain, pdf_path, multi_domain_pdfs=domain_pdfs_list
                )

                techterm_dir_name = os.path.dirname(techterm_path)
                os.makedirs(techterm_dir_name, exist_ok=True)

                with open(techterm_path, "w") as techterm_file:
                    json_obj = pdf_techterms.to_json()
                    json.dump(json_obj, techterm_file, ensure_ascii=False, indent=2)
    else:
        raise RuntimeError("unreachable statement")
