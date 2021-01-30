import re
from io import BufferedWriter, BytesIO
from dataclasses import dataclass
from typing import Any, Union, Optional, cast

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTPage, LTTextBox, LTTextLine, LTChar, LTAnno, LTText
from pdfminer.layout import LAParams
from pdfminer.utils import enc


@dataclass
class TextfulState:
    in_text_section: bool = False
    ncolor: str = ""
    size: float = 0.0
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
    ):
        PDFConverter.__init__(
            self, rsrcmgr, outfp, codec, pageno, laparams
        )  # pyright:reportUnknownMemberType=false
        self._stripcontrol = stripcontrol

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
            ncolor: str = item.graphicstate.ncolor
            size: float = item.size
            self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
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
            ncolor = cast(str, item.graphicstate.ncolor)
            size = cast(float, item.size)
            self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
            state.in_text_section = True
            state.ncolor = ncolor
            state.size = size
            state.text = self._get_text(item)

        def text_section_continues() -> bool:
            return (
                isinstance(item, LTChar)
                and state.ncolor == cast(str, item.graphicstate.ncolor)
                and abs(state.size - cast(float, item.size)) < 0.1
            )

        def exit_text_section():
            self._write_text(state.text)
            self._write("</text>\n")
            state.in_text_section = False
            state.ncolor = ""
            state.size = 0.0
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
            text = text.encode(
                cast(str, self.codec)
            )  # pyright:reportGeneralTypeIssues=false
        cast(Union[BufferedWriter, BytesIO], self.outfp).write(text)

    def _write_text(self, text: str):
        if self._stripcontrol:
            text = self.CONTROL.sub("", text)
        self._write(enc(text))  # pyright:reportUnknownArgumentType=false

    def _get_text(self, item: Union[LTText, LTChar]) -> str:
        text = cast(str, item.get_text())  # pyright: reportGeneralTypeIssues=false
        return text if self.ERROR_TEXT.match(text) is None else " "
