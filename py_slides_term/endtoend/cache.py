import os
import json
from hashlib import sha256
from typing import Union

from .configs import BaseConfig, XMLConfig, CandidateConfig
from py_slides_term.pdftoxml import PDFnXMLContent
from py_slides_term.candidates import PDFCandidateTermList

DEFAULT_CACHE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "__py_slides_term_cache__")
)


class PySlidesTermCache:
    # public
    def __init__(self, cache_dir: str = DEFAULT_CACHE_DIR):
        self._cache_dir = cache_dir

    def load_xml(self, pdf_path: str, config: XMLConfig) -> Union[PDFnXMLContent, None]:
        dir_name = self._create_dir_name(config)
        file_name = self._create_file_name(pdf_path, "xml")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as xml_file:
            xml_content = xml_file.read()

        return PDFnXMLContent(pdf_path, xml_content)

    def store_xml(self, pdfnxml: PDFnXMLContent, config: XMLConfig):
        dir_name = self._create_dir_name(config)
        file_name = self._create_file_name(pdfnxml.pdf_path, "xml")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as xml_file:
            xml_file.write(pdfnxml.xml_content)

    def load_candidates(
        self, pdf_path: str, config: CandidateConfig
    ) -> Union[PDFCandidateTermList, None]:
        dir_name = self._create_dir_name(config)
        file_name = self._create_file_name(pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            obj = json.load(json_file)

        return PDFCandidateTermList.from_json(obj)

    def store_candidates(
        self, candidates: PDFCandidateTermList, config: CandidateConfig
    ):
        dir_name = self._create_dir_name(config)
        file_name = self._create_file_name(candidates.pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(candidates.to_json(), json_file, ensure_ascii=False, indent=2)

    # private
    def _create_dir_name(self, config: BaseConfig) -> str:
        return sha256(json.dumps(config.to_json()).encode()).hexdigest()

    def _create_file_name(self, file_path: str, ext: str) -> str:
        return f"{sha256(file_path.encode()).hexdigest()}.{ext}"
