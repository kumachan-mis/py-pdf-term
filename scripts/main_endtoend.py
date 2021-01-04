import os
from py_slides_term import PySlidesTermExtractor, DomainPDFList
from scripts.utils import generate_pdf_path

script_name = os.path.basename(__file__)

if __name__ == "__main__":
    extractor = PySlidesTermExtractor()
    pdf_paths = list(generate_pdf_path(domain="Compiler"))
    techterm = extractor.extract(
        domain="Compiler",
        pdf_path=pdf_paths[0],
        single_domain_pdfs=DomainPDFList(domain="Compiler", pdf_paths=pdf_paths),
    )

    print(techterm.to_json())
