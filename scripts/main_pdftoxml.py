import os
from io import BytesIO
from glob import glob
from argparse import ArgumentParser

from pdf_slides_term.pdftoxml import PDFtoXMLConverter
from scripts.settings import PDF_DIR, XML_DIR


def pdf_path_to_xml_path(pdf_path: str) -> str:
    abs_dir_path, pdf_file_name = os.path.split(pdf_path)
    rel_dir_path = os.path.relpath(abs_dir_path, PDF_DIR)
    noext_file_name = os.path.splitext(pdf_file_name)[0]
    return os.path.join(XML_DIR, rel_dir_path, f"{noext_file_name}.xml")


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-f",
        "--file",
        help="use file to file conversion",
        action="store_const",
        dest="type",
        const="file",
    )
    group.add_argument(
        "-s",
        "--stream",
        help="use stream to stream conversion",
        action="store_const",
        dest="type",
        const="stream",
    )
    parser.set_defaults(type="file")
    args = parser.parse_args()

    converter = PDFtoXMLConverter()
    pdf_paths = glob(os.path.join(PDF_DIR, "**", "*.pdf"), recursive=True)
    xml_paths = list(map(pdf_path_to_xml_path, pdf_paths))

    if args.type == "file":
        print("main_pdftoxml.py: file to file conversion")

        for pdf_path, xml_path in zip(pdf_paths, xml_paths):
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"main_pdftoxml.py: {pdf_name} → {xml_name}")
            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)
            converter.convert_between_path(pdf_path, xml_path)

    elif args.type == "stream":
        print("main_pdftoxml.py: stream to stream conversion")

        for pdf_path, xml_path in zip(pdf_paths, xml_paths):
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"main_pdftoxml.py: {pdf_name} →　BytesIO →　{xml_name}")

            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)
            xml_stream = BytesIO()
            with open(pdf_path, "rb") as pdf_file:
                converter.convert_between_stream(pdf_file, xml_stream)
            with open(xml_path, "w") as xml_file:
                xml_file.write(xml_stream.getvalue().decode("utf-8"))
            xml_stream.close()

    else:
        raise RuntimeError("unreachable statement")
