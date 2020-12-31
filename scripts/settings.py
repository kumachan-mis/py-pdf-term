import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

PDF_DIR = os.path.join(DATASET_DIR, "pdf")
XML_DIR = os.path.join(DATASET_DIR, "xml")
CANDIDATE_DIR = os.path.join(DATASET_DIR, "candidate")
METHODS_DIR = os.path.join(DATASET_DIR, "methods")
TECHTERM_DIR = os.path.join(DATASET_DIR, "techterm")
