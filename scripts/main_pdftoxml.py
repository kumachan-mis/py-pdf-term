from os import path, makedirs
from glob import glob

from pdf_slides_term.pdftoxml import pdf_to_xml
from pdf_slides_term.settings import XML_DIR, BASE_DIR


def pdf_path_to_xml_path(pdf_path):
    dir_path, pdf_file_name = path.split(pdf_path)
    xml_file_name = f"{path.splitext(pdf_file_name)[0]}.xml"
    dir_name = path.basename(dir_path)
    return path.join(XML_DIR, dir_name, xml_file_name)


if __name__ == "__main__":
    pdf_dir = path.join(BASE_DIR, "..", "..", "slides")
    pdf_paths = glob(path.join(pdf_dir, "**", "*.pdf"), recursive=True)
    xml_paths = list(map(pdf_path_to_xml_path, pdf_paths))

    for pdf_path, xml_path in zip(pdf_paths, xml_paths):
        xml_dir_name = path.dirname(xml_path)
        makedirs(xml_dir_name, exist_ok=True)
        pdf_to_xml(pdf_path, xml_path)
