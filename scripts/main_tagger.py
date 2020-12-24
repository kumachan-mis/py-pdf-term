import sys
import os

from scripts.settings import BASE_DIR
from pdf_slides_term.mecab.tagger import MeCabTagger


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python main_tagger.py [text]\n")
        exit(1)

    rcfile = os.path.join(BASE_DIR, ".mecabrc")
    results = MeCabTagger("--rcfile", rcfile).parse(sys.argv[1])
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
