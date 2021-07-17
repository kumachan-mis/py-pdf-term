import os
from argparse import ArgumentParser
from xml.etree.ElementTree import tostring

from py_pdf_term.pdftoxml import PDFtoXMLConverter
from scripts.utils import generate_pdf_path, pdf_to_xml_path

script_name = os.path.basename(__file__)

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
        "-e",
        "--element",
        help="use file to element conversion",
        action="store_const",
        dest="type",
        const="element",
    )
    parser.set_defaults(type="file")
    args = parser.parse_args()

    converter = PDFtoXMLConverter()
    pdf_paths = generate_pdf_path()

    if args.type == "file":
        print(f"{script_name}: file to file conversion")

        for pdf_path in pdf_paths:
            xml_path = pdf_to_xml_path(pdf_path)
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"{script_name}: {pdf_name} → {xml_name}")

            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)

            converter.convert_as_file(pdf_path, xml_path)

    elif args.type == "element":
        print(f"{script_name}: file to element conversion")

        for pdf_path in pdf_paths:
            xml_path = pdf_to_xml_path(pdf_path)
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"{script_name}: {pdf_name} →　{xml_name}")

            pdfnxml = converter.convert_as_element(pdf_path)

            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)
            with open(xml_path, "wb") as xml_file:
                xml_content = tostring(pdfnxml.xml_root, encoding="utf-8")
                xml_file.write(xml_content)

    else:
        raise RuntimeError("unreachable statement")
