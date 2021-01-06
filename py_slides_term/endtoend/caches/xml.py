import os
from glob import glob
from shutil import rmtree
from typing import Union

from ..configs import XMLLayerConfig
from .util import create_dir_name_from_config, create_file_name_from_path
from py_slides_term.pdftoxml import PDFnXMLContent


class XMLLayerCache:
    def __init__(self, cache_dir: str):
        self._cache_dir = cache_dir

    def load(
        self, pdf_path: str, config: XMLLayerConfig
    ) -> Union[PDFnXMLContent, None]:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdf_path, "xml")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as xml_file:
            xml_content = xml_file.read()

        return PDFnXMLContent(pdf_path, xml_content)

    def store(self, pdfnxml: PDFnXMLContent, config: XMLLayerConfig):
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdfnxml.pdf_path, "xml")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as xml_file:
            xml_file.write(pdfnxml.xml_content)

    def remove(self, pdf_path: str, config: XMLLayerConfig):
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdf_path, "xml")
        cache_dir_path = os.path.join(self._cache_dir, dir_name)
        cache_file_path = os.path.join(cache_dir_path, file_name)

        if not os.path.isfile(cache_file_path):
            return

        os.remove(cache_file_path)

        cache_file_paths = glob(os.path.join(cache_dir_path, "*.xml"))
        if not cache_file_paths:
            rmtree(cache_dir_path)
