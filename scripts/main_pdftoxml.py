import os
from io import BytesIO
from argparse import ArgumentParser

from py_slides_term.pdftoxml import PDFtoXMLConverter
from scripts.utils import generate_pdf_path, pdf_to_xml_path


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
    pdf_paths = generate_pdf_path()

    if args.type == "file":
        print("main_pdftoxml.py: file to file conversion")

        for pdf_path in pdf_paths:
            xml_path = pdf_to_xml_path(pdf_path)
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"main_pdftoxml.py: {pdf_name} → {xml_name}")

            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)

            converter.convert_between_path(pdf_path, xml_path)

    elif args.type == "stream":
        print("main_pdftoxml.py: stream to stream conversion")

        for pdf_path in pdf_paths:
            xml_path = pdf_to_xml_path(pdf_path)
            pdf_name, xml_name = os.path.basename(pdf_path), os.path.basename(xml_path)
            print(f"main_pdftoxml.py: {pdf_name} →　BytesIO →　{xml_name}")

            xml_stream = BytesIO()
            with open(pdf_path, "rb") as pdf_file:
                converter.convert_between_stream(pdf_file, xml_stream)

            xml_dir_name = os.path.dirname(xml_path)
            os.makedirs(xml_dir_name, exist_ok=True)
            with open(xml_path, "w") as xml_file:
                xml_file.write(xml_stream.getvalue().decode("utf-8"))
            xml_stream.close()

    else:
        raise RuntimeError("unreachable statement")
