from argparse import ArgumentParser

from py_slides_term.morphemes import JanomeTokenizer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("text", help="text to pass Janome tokenizer", type=str)
    args = parser.parse_args()

    results = JanomeTokenizer().tokenize(args.text)
    for result in results:
        print(result.surface_form, result.pos, result.category, result.subcategory)
