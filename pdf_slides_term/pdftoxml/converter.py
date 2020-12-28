# type: ignore

import re
from enum import Enum, auto
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTPage, LTText, LTChar, LTTextLine, LTTextBox
from pdfminer.utils import enc


class TextfulXMLConverter(PDFConverter):

    CONTROL = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
    ERROR_TEXT = re.compile(r"^(\(cid:\d+\))+$")

    # public
    def __init__(
        self,
        rsrcmgr,
        outfp,
        codec="utf-8",
        pageno=1,
        laparams=None,
        imagewriter=None,
        stripcontrol=False,
    ):
        PDFConverter.__init__(
            self, rsrcmgr, outfp, codec=codec, pageno=pageno, laparams=laparams
        )
        self.imagewriter = imagewriter
        self.stripcontrol = stripcontrol
        self._write_header()

    def receive_layout(self, ltpage):
        self._render(ltpage)

    def close(self):
        self._write_footer()

    # private
    def _write_header(self):
        if self.codec:
            self._write('<?xml version="1.0" encoding="%s" ?>\n' % self.codec)
        else:
            self._write('<?xml version="1.0" ?>\n')
        self._write("<pages>\n")

    def _write_footer(self):
        self._write("</pages>\n")

    def _render(self, item):
        if isinstance(item, LTPage):
            self._write('<page id="%s">\n' % (item.pageid))
            self._render_children(item)
            self._write("</page>\n")
        elif isinstance(item, LTTextLine):
            self._write("<textline>\n")
            self._render_children(item)
            self._write("</textline>\n")
        elif isinstance(item, LTTextBox):
            self._write('<textbox id="%d">\n' % (item.index))
            self._render_children(item)
            self._write("</textbox>\n")
        elif isinstance(item, LTChar):
            ncolor, size = item.graphicstate.ncolor, item.size
            self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
            self._write_text(item.get_text())
            self._write("</text>\n")
        elif isinstance(item, LTText):
            self._write("<text>")
            self._write_text(item.get_text())
            self._write("</text>\n")

    def _render_children(self, item):
        class State(Enum):
            CHAR = auto()
            NON_CHAR = auto()

        prev_state, current_state = State.NON_CHAR, None
        ncolor, size, text = None, None, ""
        for child in item:
            current_state = State.CHAR if isinstance(child, LTChar) else State.NON_CHAR
            if prev_state == State.CHAR and current_state == State.CHAR:
                if (
                    ncolor == child.graphicstate.ncolor
                    and -0.1 < size - child.size < 0.1
                ):
                    text += self._get_text(child)
                else:
                    self._write_text(text)
                    self._write("</text>\n")
                    ncolor, size = child.graphicstate.ncolor, child.size
                    text = ""
                    self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
                    text += self._get_text(child)
            elif prev_state == State.CHAR and current_state == State.NON_CHAR:
                self._write_text(text)
                self._write("</text>\n")
                ncolor, size = None, None
                text = ""
                self._render(child)
            elif prev_state == State.NON_CHAR and current_state == State.CHAR:
                ncolor, size = child.graphicstate.ncolor, child.size
                self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
                text += self._get_text(child)
            elif prev_state == State.NON_CHAR and current_state == State.NON_CHAR:
                ncolor, size = None, None
                text = ""
                self._render(child)

            prev_state = current_state

        if prev_state == State.CHAR:
            self._write_text(text)
            self._write("</text>\n")

    def _get_text(self, item):
        text = item.get_text()
        return text if self.ERROR_TEXT.match(text) is None else " "

    def _write(self, text):
        if self.codec:
            text = text.encode(self.codec)
        self.outfp.write(text)

    def _write_text(self, text):
        if self.stripcontrol:
            text = self.CONTROL.sub("", text)
        self._write(enc(text))


class PDFtoXMLConverter:
    # public
    def pdf_to_xml(self, pdf_path: str, xml_path: str):
        manager = PDFResourceManager()
        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            converter = TextfulXMLConverter(manager, xml_file, stripcontrol=True)
            page_interpreter = PDFPageInterpreter(manager, converter)

            for page in PDFPage.get_pages(pdf_file, check_extractable=False):
                page_interpreter.process_page(page)

            converter.close()
