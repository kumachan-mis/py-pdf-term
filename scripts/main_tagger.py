from sys import argv, stderr

from pdf_slides_term.tagger import MeCabTagger


if __name__ == "__main__":
    argc = len(argv)
    if argc != 2:
        stderr.write("Usage: python main_tagger.py [text]\n")
        exit(1)

    results = MeCabTagger().parse(argv[1])
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
