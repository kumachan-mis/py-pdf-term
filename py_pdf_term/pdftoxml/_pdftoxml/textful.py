from dataclasses import dataclass
from typing import BinaryIO, Sequence

from pdfminer.converter import PDFConverter
from pdfminer.layout import (
    LAParams,
    LTAnno,
    LTChar,
    LTComponent,
    LTPage,
    LTTextBox,
    LTTextLine,
)
from pdfminer.pdfinterp import PDFGraphicState, PDFResourceManager
from pdfminer.pdftypes import PDFStream
from pdfminer.utils import Matrix, PathSegment, Rect, bbox2str, enc

from .utils import clean_content_text

type NColor = float | tuple[float, float, float] | tuple[float, float, float, float]


@dataclass
class TextboxState:
    within_section: bool
    size: float
    ncolor: NColor | None
    bbox: str
    text: str


class TextfulXMLConverter(PDFConverter[BinaryIO]):
    """A PDFConverter subclass that outputs textful XML format.

    Args
    ----
        rsrcmgr:
            PDFResourceManager object from pdfminer.
        outfp:
            File-like object to output XML.
        codec:
            Codec name to encode XML.
        pageno:
            Page number to start.
        laparams:
            LAParams object from pdfminer.
        nfc_norm:
            If True, normalize text to NFC, otherwise keep original.
        include_pattern:
            Regular expression pattern of text to include in the output.
        exclude_pattern:
            Regular expression pattern of text to exclude from the output (overrides
            include_pattern).
    """

    def __init__(
        self,
        rsrcmgr: PDFResourceManager,
        outfp: BinaryIO,
        codec: str = "utf-8",
        pageno: int = 1,
        laparams: LAParams | None = None,
        nfc_norm: bool = True,
        include_pattern: str | None = None,
        exclude_pattern: str | None = None,
    ) -> None:
        super().__init__(rsrcmgr, outfp, codec, pageno, laparams)

        def _clean_content_text(text: str) -> str:
            return clean_content_text(text, nfc_norm, include_pattern, exclude_pattern)

        self._clean_content_text = _clean_content_text

    def write_header(self) -> None:
        self._write('<?xml version="1.0" encoding="%s" ?>\n' % self.codec)
        self._write("<pages>\n")

    def receive_layout(self, ltpage: LTPage) -> None:
        self._render(ltpage)

    def write_footer(self) -> None:
        self._write("</pages>\n")

    # override to ignore LTFigure
    def begin_figure(self, name: str, bbox: Rect, matrix: Matrix) -> None:
        pass

    # override to ignore LTFigure
    def end_figure(self, _: str) -> None:
        pass

    # override to ignore LTImage
    def render_image(self, name: str, stream: PDFStream) -> None:
        pass

    # override to ignore LTLine, LTRect and LTCurve
    def paint_path(
        self,
        gstate: PDFGraphicState,
        stroke: bool,
        fill: bool,
        evenodd: bool,
        path: Sequence[PathSegment],
    ) -> None:
        pass

    def _render(self, item: LTComponent) -> None:
        match item:
            case LTPage():
                self._render_page(item)
            case LTTextBox():
                self._render_textbox(item)
            case _:
                pass

    def _render_page(self, ltpage: LTPage) -> None:
        self._write('<page id="%s">\n' % ltpage.pageid)
        for child in ltpage:
            self._render(child)
        self._write("</page>\n")

    def _render_textbox(self, lttextbox: LTTextBox) -> None:
        state = TextboxState(False, 0.0, None, "", "")

        def render_textbox_child(child: LTTextLine | LTChar | LTAnno) -> None:
            match child:
                case LTTextLine():
                    render_textline(child)
                case LTChar():
                    render_char(child)
                case LTAnno():
                    render_anno(child)

        def render_textline(lttextline: LTTextLine) -> None:
            for child in lttextline:
                render_textbox_child(child)

        def render_char(ltchar: LTChar) -> None:
            if not state.within_section:
                enter_text_section(ltchar)
                state.text += ltchar.get_text()
            elif text_section_continues(ltchar):
                state.text += ltchar.get_text()
            else:
                exit_text_section()
                enter_text_section(ltchar)
                state.text += ltchar.get_text()

        def render_anno(ltanno: LTAnno) -> None:
            if not state.within_section:
                pass
            elif text_section_continues(ltanno):
                state.text += ltanno.get_text()
            else:
                exit_text_section()

        def enter_text_section(item: LTChar) -> None:
            state.within_section = True
            state.size = item.size
            state.ncolor = item.graphicstate.ncolor
            state.bbox = bbox2str(item.bbox)
            state.text = ""

        def text_section_continues(item: LTChar | LTAnno) -> bool:
            if isinstance(item, LTAnno):
                return True
            return (
                state.ncolor == item.graphicstate.ncolor
                and abs(state.size - item.size) < 0.1
            )

        def exit_text_section() -> None:
            if not state.within_section:
                return

            text = self._clean_content_text(state.text)
            if text:
                self._write(
                    '<text size="%.3f" ncolor="%s" bbox="%s">'
                    % (state.size, state.ncolor, state.bbox)
                )
                self._write(enc(text))
                self._write("</text>\n")

            state.within_section = False
            state.size = 0.0
            state.ncolor = None
            state.bbox = ""
            state.text = ""

        for child in lttextbox:
            render_textbox_child(child)

        exit_text_section()

    def _write(self, text: str) -> None:
        text_bytes = text.encode(self.codec)
        self.outfp.write(text_bytes)
