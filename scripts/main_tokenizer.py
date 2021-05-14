from argparse import ArgumentParser
from dataclasses import astuple

from py_slides_term.tokenizer import SpaCyTokenizer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("text", help="text to pass SpaCy tokenizer", type=str)
    args = parser.parse_args()

    results = SpaCyTokenizer().tokenize(args.text)
    for result in results:
        print(*astuple(result))
