# pyright:reportGeneralTypeIssues=false
# pyright:reportUnknownVariableType=false
# pyright:reportUnknownMemberType=false
# pyright:reportUnknownParameterType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportIncompatibleMethodOverride=false

import re
from io import BufferedWriter, BytesIO
from unicodedata import normalize
from dataclasses import dataclass
from typing import Any, Union, Optional

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTPage, LTTextBox, LTTextLine, LTChar, LTAnno, LTText
from pdfminer.layout import LAParams
from pdfminer.utils import bbox2str, enc


@dataclass
class TextfulState:
    in_text_section: bool = False
    size: float = 0.0
    ncolor: str = ""
    text: str = ""


class TextfulXMLConverter(PDFConverter):

    CONTROL = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
    ERROR_TEXT = re.compile(r"^(\(cid:\d+\))+$")

    # public
    def __init__(
        self,
        rsrcmgr: PDFResourceManager,
        outfp: Union[BufferedWriter, BytesIO],
        codec: str = "utf-8",
        pageno: int = 1,
        laparams: Optional[LAParams] = None,
        stripcontrol: bool = False,
        nfcnorm: bool = True,
    ):
        PDFConverter.__init__(self, rsrcmgr, outfp, codec, pageno, laparams)
        self._stripcontrol = stripcontrol
        self._nfcnorm = nfcnorm

    def write_header(self):
        if self.codec:
            codec: str = self.codec
            self._write('<?xml version="1.0" encoding="%s" ?>\n' % codec)
        else:
            self._write('<?xml version="1.0" ?>\n')
        self._write("<pages>\n")

    def receive_layout(self, ltpage: LTPage):
        self._render(ltpage)

    def write_footer(self):
        self._write("</pages>\n")

    # to ignore LTFigure
    def begin_figure(self, name, bbox, matrix):
        return

    # to ignore LTFigure
    def end_figure(self, name):
        return

    # to ignore LTImage
    def render_image(self, name, stream):
        return

    # to ignore LTLine, LTRect and LTCurve
    def paint_path(self, graphicstate, stroke, fill, evenodd, path):
        return

    # private
    def _render(self, item: Any):
        if isinstance(item, LTPage):
            pageid: str = item.pageid
            self._write('<page id="%s">\n' % pageid)
            for child in item:
                self._render(child)
            self._write("</page>\n")
        elif isinstance(item, LTTextBox):
            self._render_textlike_item(item)
        elif isinstance(item, LTTextLine):
            self._render_textlike_item(item)
        elif isinstance(item, LTChar):
            size: float = item.size
            ncolor: str = item.graphicstate.ncolor
            self._write(
                '<text size="%.3f" ncolour="%s" bbox="%s">'
                % (size, ncolor, bbox2str(item.bbox))
            )
            self._write_text(self._get_text(item))
            self._write("</text>\n")
        elif isinstance(item, LTText):
            self._write("<text>")
            self._write_text(self._get_text(item))
            self._write("</text>\n")

    def _render_textlike_item(self, item: Any):
        state = TextfulState()

        def rec_render_textlike_item(rec_item: Any):
            if isinstance(rec_item, LTTextBox):
                for child in rec_item:
                    rec_render_textlike_item(child)
            elif isinstance(rec_item, LTTextLine):
                for child in rec_item:
                    rec_render_textlike_item(child)
            else:
                self._render_charlike_item(rec_item, state)

        def finalize_textlike_item_rendering():
            if not state.in_text_section:
                return
            self._write_text(state.text)
            self._write("</text>\n")

        rec_render_textlike_item(item)
        finalize_textlike_item_rendering()

    def _render_charlike_item(self, item: Any, state: TextfulState):
        def enter_text_section():
            size: float = item.size
            ncolor: str = item.graphicstate.ncolor
            self._write(
                '<text size="%.3f" ncolor="%s" bbox="%s">'
                % (size, ncolor, bbox2str(item.bbox))
            )

            state.in_text_section = True
            state.size = size
            state.ncolor = ncolor
            state.text = self._get_text(item)

        def text_section_continues() -> bool:
            return (
                isinstance(item, LTChar)
                and state.ncolor == item.graphicstate.ncolor
                and abs(state.size - item.size) < 0.1
            )

        def exit_text_section():
            self._write_text(state.text)
            self._write("</text>\n")

            state.in_text_section = False
            state.size = 0.0
            state.ncolor = ""
            state.text = ""

        if state.in_text_section:
            if isinstance(item, LTChar):
                if text_section_continues():
                    state.text += self._get_text(item)
                else:
                    exit_text_section()
                    enter_text_section()
            elif not isinstance(item, LTAnno):
                exit_text_section()
        elif isinstance(item, LTChar):
            enter_text_section()

    def _write(self, text: str):
        if self.codec:
            text = text.encode(self.codec)
        self.outfp.write(text)

    def _write_text(self, text: str):
        if self._stripcontrol:
            text = self.CONTROL.sub("", text)
        if self._nfcnorm:
            text = normalize("NFC", text)
        self._write(enc(text))

    def _get_text(self, item: Union[LTText, LTChar]) -> str:
        text = item.get_text()
        return text if self.ERROR_TEXT.match(text) is None else " "
