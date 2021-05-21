# pyright:reportGeneralTypeIssues=false
# pyright:reportUnknownVariableType=false
# pyright:reportUnknownMemberType=false
# pyright:reportUnknownParameterType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportIncompatibleMethodOverride=false

from io import BufferedWriter, BytesIO
from dataclasses import dataclass
from typing import Any, Union, Optional

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTPage, LTTextBox, LTTextLine, LTChar, LTText, LTAnno
from pdfminer.layout import LAParams
from pdfminer.utils import bbox2str, enc

from .utils import clean_content_text


@dataclass
class TextfulState:
    in_text_section: bool = False
    size: float = 0.0
    ncolor: str = ""
    bbox: str = ""
    text: str = ""


class TextfulXMLConverter(PDFConverter):
    # public
    def __init__(
        self,
        rsrcmgr: PDFResourceManager,
        outfp: Union[BufferedWriter, BytesIO],
        codec: str = "utf-8",
        pageno: int = 1,
        laparams: Optional[LAParams] = None,
        nfc_norm: bool = True,
        include_pattern: Optional[str] = None,
        exclude_parrern: Optional[str] = None,
    ):
        PDFConverter.__init__(self, rsrcmgr, outfp, codec, pageno, laparams)

        def _clean_content_text(text: str) -> str:
            return clean_content_text(text, nfc_norm, include_pattern, exclude_parrern)

        self._clean_content_text = _clean_content_text

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
            self._render_styled_text_item(item)
        elif isinstance(item, LTTextLine):
            self._render_styled_text_item(item)
        elif isinstance(item, LTChar):
            self._render_styled_text_item(item)
        elif isinstance(item, LTText):
            text = self._clean_content_text(item.get_text())
            if text:
                self._write("<text>")
                self._write(enc(text))
                self._write("</text>\n")

    def _render_styled_text_item(self, item: Any):
        state = TextfulState()

        def rec_render_styled_text_item(rec_item: Any):
            if isinstance(rec_item, LTTextBox) or isinstance(rec_item, LTTextLine):
                for child in rec_item:
                    rec_render_styled_text_item(child)
            else:
                self._render_styled_char_item(rec_item, state)

        def finalize_styled_text_item_rendering():
            if not state.in_text_section:
                return

            text = self._clean_content_text(state.text)
            if text:
                self._write(
                    '<text size="%.3f" ncolor="%s" bbox="%s">'
                    % (state.size, state.ncolor, state.bbox)
                )
                self._write(enc(text))
                self._write("</text>\n")

        rec_render_styled_text_item(item)
        finalize_styled_text_item_rendering()

    def _render_styled_char_item(self, item: Any, state: TextfulState):
        def enter_text_section():
            state.in_text_section = True
            state.size = item.size
            state.ncolor = item.graphicstate.ncolor
            state.bbox = bbox2str(item.bbox)
            state.text = item.get_text()

        def text_section_continues() -> bool:
            return (
                isinstance(item, LTChar)
                and state.ncolor == item.graphicstate.ncolor
                and abs(state.size - item.size) < 0.1
            )

        def exit_text_section():
            text = self._clean_content_text(state.text)
            if text:
                self._write(
                    '<text size="%.3f" ncolor="%s" bbox="%s">'
                    % (state.size, state.ncolor, state.bbox)
                )
                self._write(enc(text))
                self._write("</text>\n")

            state.in_text_section = False
            state.size = 0.0
            state.ncolor = ""
            state.bbox = ""
            state.text = ""

        if state.in_text_section:
            if isinstance(item, LTChar):
                if text_section_continues():
                    state.text += item.get_text()
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
