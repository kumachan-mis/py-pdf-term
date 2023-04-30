from argparse import ArgumentParser
from dataclasses import astuple

from py_pdf_term.tokenizers import Tokenizer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("text", help="text to pass to the tokenizer", type=str)
    args = parser.parse_args()

    results = Tokenizer().tokenize(args.text)
    for result in results:
        print(*astuple(result))
