import os
import json
from glob import glob

from pdf_slides_term.candidates.extractor import CandidateTermExtractor
from scripts.settings import XML_DIR, CANDIDATE_DIR


def xml_path_to_candidate_path(xml_path: str) -> str:
    abs_dir_path, xml_file_name = os.path.split(xml_path)
    rel_dir_path = os.path.relpath(abs_dir_path, XML_DIR)
    noext_file_name = os.path.splitext(xml_file_name)[0]
    return os.path.join(CANDIDATE_DIR, rel_dir_path, f"{noext_file_name}.json")


if __name__ == "__main__":
    xml_paths = glob(os.path.join(XML_DIR, "**", "*.xml"), recursive=True)
    candidate_paths = list(map(xml_path_to_candidate_path, xml_paths))

    extractor = CandidateTermExtractor(modifying_particle_augmentation=True)
    for xml_path, candidate_path in zip(xml_paths, candidate_paths):
        candidate_dir_name = os.path.dirname(candidate_path)
        os.makedirs(candidate_dir_name, exist_ok=True)
        candidate_term_list = extractor.extract_from_xml(xml_path)

        with open(candidate_path, "w") as candidate_file:
            json_obj = candidate_term_list.to_json()
            json.dump(json_obj, candidate_file, ensure_ascii=False, indent=2)
