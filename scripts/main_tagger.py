import os
from argparse import ArgumentParser

from .settings import BASE_DIR
from pdf_slides_term.mecab import MeCabTagger


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("text", help="text to pass MeCab tagger", type=str)
    args = parser.parse_args()

    rcfile = os.path.join(BASE_DIR, ".mecabrc")
    results = MeCabTagger("--rcfile", rcfile).parse(args.text)
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
