# -- Project information ---------------------------------------------------------------

project = "py-pdf-term"
copyright = "2021, Yuya Suwa"
author = "Yuya Suwa"


# -- General configuration -------------------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.githubpages"]

add_module_names = True

autodoc_member_order = "bysource"

autodoc_preserve_defaults = True

templates_path = []

exclude_patterns = []


# -- Options for HTML output -----------------------------------------------------------

html_theme = "alabaster"

html_static_path = ["static"]

html_css_files = ["custom.css"]

html_theme_options = {
    "sidebar_width": "300px",
    "github_user": "kumachan-mis",
    "github_repo": "py-pdf-term",
    "github_button": False,
    "github_banner": True,
}
