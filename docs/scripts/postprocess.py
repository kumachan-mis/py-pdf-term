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

for html_filename in ["index.html", "api.html"]:
    with open(os.path.join(BUILD_DIR, html_filename), mode="r") as html_file:
        html_str = html_file.read()

    html_str = re.sub(PRIVATE_OBJECT_PATH_REGEX, r"\1", html_str)

    with open(os.path.join(BUILD_DIR, html_filename), mode="w") as html_file:
        html_file.write(html_str)
