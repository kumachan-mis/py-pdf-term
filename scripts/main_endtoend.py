import json
import os
from argparse import ArgumentParser

from py_pdf_term import PyPDFTermExtractor
from py_pdf_term.configs import MethodLayerConfig
from scripts.utils import (
    generate_domain_pdfs,
    get_domains,
    pdf_to_techterm_path,
    relpath_from_basedir,
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
        method = "py_pdf_term.MCValueMethod"
    elif args.tfidf:
        method_type = "multi"
        method_name = "tfidf"
        method = "py_pdf_term.TFIDFMethod"
    elif args.lfidf:
        method_type = "multi"
        method_name = "lfidf"
        method = "py_pdf_term.LFIDFMethod"
    elif args.flr:
        method_type = "single"
        method_name = "flr"
        method = "py_pdf_term.FLRMethod"
    elif args.hits:
        method_type = "single"
        method_name = "hits"
        method = "py_pdf_term.HITSMethod"
    elif args.flrh:
        method_type = "single"
        method_name = "flrh"
        method = "py_pdf_term.FLRHMethod"
    elif args.mdp:
        method_type = "multi"
        method_name = "mdp"
        method = "py_pdf_term.MDPMethod"
    else:
        raise RuntimeError("unreachable statement")

    extractor = PyPDFTermExtractor(
        method_config=MethodLayerConfig(
            method_type=method_type,
            method=method,
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        )
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
                    dict_obj = pdf_techterms.to_dict()
                    json.dump(dict_obj, techterm_file, ensure_ascii=False, indent=2)

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
                    dict_obj = pdf_techterms.to_dict()
                    json.dump(dict_obj, techterm_file, ensure_ascii=False, indent=2)
    else:
        raise RuntimeError("unreachable statement")
