# py-slides-term
A python module for terminology extraction from presentation slides

## Installation
```
pip install py-slides-term
```

## Dependencies
- pdfminer.six
  - https://github.com/pdfminer/pdfminer.six
- spacy
  - https://github.com/explosion/spaCy

You also need to install spaCy models `ja_core_news_sm` and `en_core_web_sm`, which this module depends on.

```
pip install https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-2.3.2/ja_core_news_sm-2.3.2.tar.gz
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
```
