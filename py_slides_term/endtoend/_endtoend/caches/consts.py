import os

DEFAULT_CACHE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "__py_slides_term_cache__",
    )
)
