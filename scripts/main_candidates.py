import os
import json

from py_pdf_term.pdftoxml import PDFnXMLPath
from py_pdf_term.candidates import CandidateTermExtractor
from scripts.utils import (
    relpath_from_basedir,
    generate_pdf_path,
    pdf_to_xml_path,
    pdf_to_candidate_path,
)

script_name = os.path.basename(__file__)

if __name__ == "__main__":
    extractor = CandidateTermExtractor()
    pdf_paths = generate_pdf_path()
    for pdf_path in pdf_paths:
        candidate_path = pdf_to_candidate_path(pdf_path)
        print(f"{script_name}: creating {relpath_from_basedir(candidate_path)} ...")

        xml_path = pdf_to_xml_path(pdf_path)
        pdfnxml = PDFnXMLPath(pdf_path, xml_path)
        candidate_term_list = extractor.extract_from_xml_file(pdfnxml)

        candidate_dir_name = os.path.dirname(candidate_path)
        os.makedirs(candidate_dir_name, exist_ok=True)

        with open(candidate_path, "w") as candidate_file:
            dict_obj = candidate_term_list.to_dict()
            json.dump(dict_obj, candidate_file, ensure_ascii=False, indent=2)
