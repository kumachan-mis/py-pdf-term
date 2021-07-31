import os
import re


BUILD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "build")

PRIVATE_OBJECT_PATH_REGEX = "".join(
    [
        "py_pdf_term.",
        r"(?:[A-Za-z0-9_]+\.)*",
        r"(?:_[A-Za-z0-9_]*\.)",
        r"(?:[A-Za-z0-9_]+\.)*",
        r"([A-Za-z0-9_]+)",
    ]
)

with open(os.path.join(BUILD_DIR, "api.html"), mode="r") as api_html_file:
    api_html = api_html_file.read()

api_html = re.sub(PRIVATE_OBJECT_PATH_REGEX, r"\1", api_html)

with open(os.path.join(BUILD_DIR, "api.html"), mode="w") as api_html_file:
    api_html_file.write(api_html)
