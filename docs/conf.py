# -- Project information ---------------------------------------------------------------

project = "py-pdf-term"
copyright = "2021, Yuya Suwa"
author = "Yuya Suwa"


# -- General configuration -------------------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

add_module_names = False

autodoc_member_order = "bysource"

autodoc_preserve_defaults = True

templates_path = []

exclude_patterns = []


# -- Options for HTML output -----------------------------------------------------------

html_theme = "alabaster"

html_static_path = ["static"]

html_css_files = ["custom.css"]
