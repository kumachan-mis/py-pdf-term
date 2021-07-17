import os
import json

from py_pdf_term.stylings import StylingScorer
from scripts.utils import (
    relpath_from_basedir,
    get_domains,
    generate_domain_candidates,
    pdf_to_styling_path,
)

script_name = os.path.basename(__file__)

if __name__ == "__main__":
    scorer = StylingScorer()
    domains = get_domains()
    domain_candidates_list = generate_domain_candidates(domains)
    for domain_candidates in domain_candidates_list:
        for pdf_candidates in domain_candidates.pdfs:
            styling_path = pdf_to_styling_path(pdf_candidates.pdf_path)
            print(f"{script_name}: creating {relpath_from_basedir(styling_path)} ...")

            styling_score_list = scorer.score_pdf_candidates(pdf_candidates)

            styling_dir_name = os.path.dirname(styling_path)
            os.makedirs(styling_dir_name, exist_ok=True)

            with open(styling_path, "w") as styling_file:
                dict_obj = styling_score_list.to_dict()
                json.dump(dict_obj, styling_file, ensure_ascii=False, indent=2)
