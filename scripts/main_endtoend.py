import json
import os
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Literal

from py_pdf_term import PyPDFTermMultiDomainExtractor, PyPDFTermSingleDomainExtractor
from py_pdf_term.configs import (
    MultiDomainMethodLayerConfig,
    SingleDomainMethodLayerConfig,
)
from scripts.utils import (
    generate_domain_pdfs,
    get_domains,
    pdf_to_techterm_path,
    relpath_from_basedir,
)

script_name = os.path.basename(__file__)


@dataclass(frozen=True)
class CommandLineArguments:
    method_type: Literal["single", "multi"]
    method_name: str
    method: str


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
        return CommandLineArguments("single", "mcvalue", "py_pdf_term.MCValueMethod")
    elif args.tfidf:
        return CommandLineArguments("multi", "tfidf", "py_pdf_term.TFIDFMethod")
    elif args.flr:
        return CommandLineArguments("single", "flr", "py_pdf_term.FLRMethod")
    elif args.hits:
        return CommandLineArguments("single", "hits", "py_pdf_term.HITSMethod")
    elif args.flrh:
        return CommandLineArguments("single", "flrh", "py_pdf_term.FLRHMethod")
    elif args.mdp:
        return CommandLineArguments("multi", "mdp", "py_pdf_term.MDPMethod")
    else:
        raise RuntimeError("unreachable statement")


def run_single_domain_extractor(args: CommandLineArguments) -> None:
    extractor = PyPDFTermSingleDomainExtractor(
        method_config=SingleDomainMethodLayerConfig(
            method=args.method,
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        )
    )

    domains = get_domains()
    domain_pdfs_list = generate_domain_pdfs(domains)
    for domain_pdfs in domain_pdfs_list:
        for pdf_path in domain_pdfs.pdf_paths:
            techterm_path = pdf_to_techterm_path(pdf_path, args.method_name)
            techterm_short_path = relpath_from_basedir(techterm_path)
            print(f"{script_name}: creating {techterm_short_path} ...")

            pdf_techterms = extractor.extract(pdf_path, domain_pdfs)

            techterm_dir_name = os.path.dirname(techterm_path)
            os.makedirs(techterm_dir_name, exist_ok=True)

            with open(techterm_path, "w") as techterm_file:
                dict_obj = pdf_techterms.to_dict()
                json.dump(dict_obj, techterm_file, ensure_ascii=False, indent=2)


def run_multi_domain_extractor(args: CommandLineArguments) -> None:
    extractor = PyPDFTermMultiDomainExtractor(
        method_config=MultiDomainMethodLayerConfig(
            method=args.method,
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        )
    )

    domains = get_domains()
    domain_pdfs_list = list(generate_domain_pdfs(domains))
    for domain_pdfs in domain_pdfs_list:
        for pdf_path in domain_pdfs.pdf_paths:
            techterm_path = pdf_to_techterm_path(pdf_path, args.method_name)
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


if __name__ == "__main__":
    args = parse_command_line_argments()

    match args.method_type:
        case "single":
            run_single_domain_extractor(args)
        case "multi":
            run_multi_domain_extractor(args)
        case _:
            raise RuntimeError("unreachable statement")
