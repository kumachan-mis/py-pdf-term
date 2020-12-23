import os
from glob import glob

from pdf_slides_term.pdftoxml import PDFtoXMLConverter
from scripts.settings import DATASET_DIR


PDF_DIR = os.path.join(DATASET_DIR, "pdf")
XML_DIR = os.path.join(DATASET_DIR, "xml")


def pdf_path_to_xml_path(pdf_path):
    abs_dir_path, pdf_file_name = os.path.split(pdf_path)
    rel_dir_path = os.path.relpath(abs_dir_path, PDF_DIR)
    noext_file_name = os.path.splitext(pdf_file_name)[0]
    return os.path.join(XML_DIR, rel_dir_path, f"{noext_file_name}.xml")


if __name__ == "__main__":
    pdf_paths = glob(os.path.join(PDF_DIR, "**", "*.pdf"), recursive=True)
    xml_paths = list(map(pdf_path_to_xml_path, pdf_paths))

    converter = PDFtoXMLConverter()
    for pdf_path, xml_path in zip(pdf_paths, xml_paths):
        xml_dir_name = os.path.dirname(xml_path)
        os.makedirs(xml_dir_name, exist_ok=True)
        converter.pdf_to_xml(pdf_path, xml_path)
