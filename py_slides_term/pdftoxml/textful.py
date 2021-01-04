import re
from io import BufferedWriter, BytesIO
from enum import Enum, auto
from typing import Any, Union, Optional, cast

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTPage, LTText, LTChar, LTTextLine, LTTextBox
from pdfminer.layout import LAParams
from pdfminer.utils import enc


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
            ncolor: str = item.graphicstate.ncolor
            size: float = item.size
            self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
            self._write_text(cast(str, item.get_text()))
            self._write("</text>\n")
        elif isinstance(item, LTText):
            self._write("<text>")
            self._write_text(cast(str, item.get_text()))
            self._write("</text>\n")

    def _render_children(self, item: Union[LTPage, LTTextLine, LTTextBox]):
        class State(Enum):
            CHAR = auto()
            NON_CHAR = auto()

        prev_state: State = State.NON_CHAR
        current_state: State = State.NON_CHAR
        ncolor: str = ""
        size: float = 0.0
        text: str = ""
        for child in item:
            current_state = State.CHAR if isinstance(child, LTChar) else State.NON_CHAR
            if prev_state == State.CHAR and current_state == State.CHAR:
                if (
                    ncolor == cast(str, child.graphicstate.ncolor)
                    and abs(size - cast(float, child.size)) < 0.1
                ):
                    text += self._get_text(child)
                else:
                    self._write_text(text)
                    self._write("</text>\n")
                    ncolor = cast(str, child.graphicstate.ncolor)
                    size = cast(float, child.size)
                    text = ""
                    self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
                    text += self._get_text(child)
            elif prev_state == State.CHAR and current_state == State.NON_CHAR:
                self._write_text(text)
                self._write("</text>\n")
                ncolor = ""
                size = 0.0
                text = ""
                self._render(child)
            elif prev_state == State.NON_CHAR and current_state == State.CHAR:
                ncolor = cast(str, child.graphicstate.ncolor)
                size = cast(float, child.size)
                self._write('<text ncolour="%s" size="%.3f">' % (ncolor, size))
                text += self._get_text(child)
            elif prev_state == State.NON_CHAR and current_state == State.NON_CHAR:
                ncolor = ""
                size = 0.0
                text = ""
                self._render(child)

            prev_state = current_state

        if prev_state == State.CHAR:
            self._write_text(text)
            self._write("</text>\n")

    def _get_text(
        self, item: Union[LTPage, LTTextLine, LTTextBox, LTText, LTChar]
    ) -> str:
        text = cast(str, item.get_text())  # pyright: reportGeneralTypeIssues=false
        return text if self.ERROR_TEXT.match(text) is None else " "

    def _write(self, text: str):
        if self.codec:
            text = text.encode(
                cast(str, self.codec)
            )  # pyright: reportGeneralTypeIssues=false
        cast(Union[BufferedWriter, BytesIO], self.outfp).write(text)

    def _write_text(self, text: str):
        if self._stripcontrol:
            text = self.CONTROL.sub("", text)
        self._write(enc(text))
