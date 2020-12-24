from sys import argv, stderr

from pdf_slides_term.tokenizer import JanomeTokenizer


if __name__ == "__main__":
    argc = len(argv)
    if argc != 2:
        stderr.write("Usage: python tokenizer.py [text]\n")
        exit(1)

    results = JanomeTokenizer().tokenize(argv[1])
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
