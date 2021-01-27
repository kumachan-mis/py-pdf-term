from argparse import ArgumentParser

from py_slides_term.morphemes import SpaCyTokenizer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("text", help="text to pass SpaCy tokenizer", type=str)
    args = parser.parse_args()

    results = SpaCyTokenizer().tokenize(args.text)
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
