Welcome to py-pdf-term's documentation!
=======================================

py-pdf-term is a fully-configurable terminology extraction module written in Python.

input
    PDF files, widely-spread data format for sharing information with other people.
output
    terminology list per PDF page, convertable to JSON format.


Motivation
==========

There are countless number of implementations of terminology extraction algorithms.
Many of them support personal trials to demonstrate efficacy of the algorithm.
However, they don't consider real application so that it is difficult to use in practical softwares.

The goal is to support both of laboratory use and practical use of terminology extraction.


Installation
============
.. code-block::

    pip install py-pdf-term

You also need to install spaCy models ja_core_news_sm and en_core_web_sm, which this module depends on.

.. code-block::

    pip install https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.2.0/ja_core_news_sm-3.2.0.tar.gz
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.2.0/en_core_web_sm-3.2.0.tar.gz


Features
========

The module provides rich configurations for laboratory use and for practical use.

For laboratory use
------------------

switch of ranking algorithms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are countless number of algorithms rank terminology.
The more algorithms are proposed, the more essential selecting a suitable one comes to be.
Sometimes you need to implement original one for a specific case you face to.
This module enables you to select a ranking algorithm with a configuration.

plug-in of little ingenuities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Trying little ingenuities again and again is also essential to have an ideal output.
For example: removing garbage words, considering one more attribute of words.
This module enables you to plug your ingenuities into the process as classes.

For practical use
-----------------

i/o customizing
^^^^^^^^^^^^^^^
In practical softwares, files are often not in a local storage. 
I/O functions for a remote storage are more complicated than built-in ones
such as `open`/`close`/`read`/`write`.
This module enables you to replace I/O functions with yours.

cache mechanism
^^^^^^^^^^^^^^^
In practical softwares, performance is one of the biggest problems though experimental ones don't care it.
Additionally, it is not a common case that a number of files are provided as a bulk dataset.
It is more common that small data are provided day by day.
In this assumption, it is effective with performance to save intermediate output.
This module has cache mechanism to save intermediate output. I/O functions for caches can be also customized.


5-layers architecture
=====================

This module follows 5-layers architecture.
The layers are pushed in a stack. A layer calls the upper layers (black dashed arrows). 
If a layer's cache has target data, the layer returns them. Otherwise, it runs actual caluculation.
In case that all layers don't have target data in their cache,
caluculations are go from the top to the bottom (red bold arrows).

.. container:: twocol

    .. container:: column

        XML Layer
            This layer coverts a PDF file to a XML file containing sentensized texts with styling attributes
            such as font size, font color and coordinate in the PDF page.
            This layer depends on `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`_.

        Candidate Term Layer
            This layer extracts candidates of terminologies from a XML data.
            It splits texts into tokens, then constructs candidates from tokens.
            This layer depends on `spaCy <https://spacy.io>`_.

        Method Layer
            This layer calculates method scores of candidates based on
            occurence/co-occurence/concatenation frequency, document frequency, colocation likelihood and so on.
            It's up to an algorithm what values are used to find scores.

        Styling Layer
            This layer calculates styling scores of candidates based on
            font size, font color and coordinate in the PDF page and so on.
            Styling scores reflects our intuitions such as:
            The larger the font size is, the more important the text must be.
            If an emphasized color is used, the text must be important.

        Technical Term Layer
            This layer selects terminologies from candidates based on method scores and styling scores.
            The order of the terminologies is the same as the appearance order in the PDF file.

    .. container:: column

        .. image:: static/architecture.png


Examples
==========================

Simplest example
----------------

Here is a zero-config example

.. code-block:: python

    from py_pdf_term import PyPDFTermSingleDomainExtractor, DomainPDFList

    def extract_terminologies_from_example_pdfs():
        # create an extractor instance with zero-config
        extractor = PyPDFTermSingleDomainExtractor()
    
        # define input: domain name and list of PDF paths
        domain = "example"
        pdf_path = "example/file1.pdf"
        domain_pdfs = DomainPDFList(
            "example",
            ["example/file1.pdf", "example/file2.pdf", "example/file3.pdf"],
        )

        # receive output: extracted terminologies
        terminologies = extractor.extract(pdf_path=pdf_path, domain_pdfs=domain_pdfs)

        return terminologies.to_dict()


Django Example
--------------

Here is an example with `Django <https://www.djangoproject.com>`_.'s FileField

.. code-block:: python

    from django.db import models
    from py_pdf_term import PyPDFTermSingleDomainExtractor, DomainPDFList


    class PDFFile(models.Model):
        id = models.AutoField(primary_key=True)
        file = models.FileField(upload_to=pdf_upload_to, max_length=200)


    def extract_terminologies_from_example_pdf():
        # define a function to open a PDF file on Django FileField
        def open_storage_binary_file(path: str, mode: str):
            try:
                pdf_file = PDFFile.objects.get(file=path)
            except PDFFile.DoesNotExist:
                raise RuntimeError()

            pdf_file.file.open(mode=mode)
            bytesio = BytesIO(pdf_file.file.read())
            pdf_file.file.close()
            return bytesio

        # define a name to find the function
        open_bin = "example.open_storage_binary_file"

        # registrate the function to the mapper
        bin_opener_mapper = BinaryOpenerMapper()
        bin_opener_mapper.add(open_bin, open_storage_binary_file)

        # create an extractor instance with following configs:
        #    - deactive the caches in all layers
        #    - costomize the function to open a PDF file
        #
        # see API reference to check all configs
        extractor = PyPDFTermSingleDomainExtractor(
            xml_config=XMLLayerConfig(
                open_bin=open_bin,
                cache="py_pdf_term.XMLLayerNoCache",
            ),
            candidate_config=CandidateLayerConfig(
                cache="py_pdf_term.CandidateLayerNoCache",
            ),
            method_config=MethodLayerConfig(
                ranking_cache="py_pdf_term.MethodLayerRankingNoCache",
                data_cache="py_pdf_term.MethodLayerDataNoCache",
            ),
            styling_config=StylingLayerConfig(
                cache="py_pdf_term.StylingLayerNoCache",
            ),
            bin_opener_mapper=bin_opener_mapper,
        )

        # define input: domain name and list of PDF paths
        domain = "example"
        pdf_path = "example/file1.pdf"
        domain_pdfs = DomainPDFList(
            "example",
            ["example/file1.pdf", "example/file2.pdf", "example/file3.pdf"],
        )

        # receive output: extracted terminologies
        terminologies = extractor.extract(pdf_path=pdf_path, domain_pdfs=domain_pdfs)

        return terminologies.to_dict()


API reference
==================

.. toctree::
    :maxdepth: 3

    api
