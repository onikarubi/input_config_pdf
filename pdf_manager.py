"""
- 必要なライブラリをインポートする
- 出力するpdf用のPDFWriterのインスタンスを作成する
- 追記したいファイルをpdf_readerで読み込む
- ストリームが格納されているキャンバスを作成する
- 追記したい内容の座標を指定する
- 指定された座標にテキストや図形をキャンバスに追記

- pdf_readerでストリームが格納されたキャンバスを読み込み、
  「追記を行なったキャンバスのデータと既存のpdfのデータを
  統合(マージ)させて、writerにページ情報を追記」という処理
  をマイページずつ処理する。

- 出力用のファイルにwriterのバイナリデータを保存
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io

class CanvasManager:
    FILE_NAME = './fonts/ArialUnicode.ttf'
    FONT = 'ヒラギノ角ゴシック Arial'
    FONT_SIZE_DEFAULT = 13

    def __init__(self, x: float, y: float, stream: str, page_size=A4, font: str = FONT, font_size: int = FONT_SIZE_DEFAULT, filename: str = FILE_NAME) -> None:
        self.x = x
        self.y = y
        self.cs = canvas.Canvas(stream)
        self.page_size = page_size
        self.font = font
        self.font_size = font_size
        self.filename = filename

        pdfmetrics.registerFont(TTFont(self.font, self.filename))
        self.cs.setFont(self.font, self.font_size)
        self.cs.setPageSize(A4)

    def change_page_size(self, size) -> None: self.cs.setPageSize(size)

    def change_font(self, font: str, size: int, file_name: str) -> None:
        pdfmetrics.registerFont(TTFont(font, file_name))
        self.cs.setFont(font, size)

    def draw_content_text(self, text: str):
        self.cs.drawString(self.x, self.y, text)
        self.cs.showPage()

    def pdf_save(self) -> None: self.cs.save()


class PDFManager:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.writer = PdfWriter()
        self.bs = io.BytesIO()
        self.stream_by_input = open(self.input_file, 'rb')
        self.reader = PdfReader(self.stream_by_input)
        self.reader_page_num: int = len(self.reader.pages)

    def _load_pdf_reader(self, bs_stream) -> PdfReader:
        return PdfReader(bs_stream)

    def draw_text(self, x: float, y: float, text: str):
        pdf_canvas = CanvasManager(x, y, self.bs, A4)

        for _ in range(self.reader_page_num):
            pdf_canvas.draw_content_text(text)

        pdf_canvas.pdf_save()

    def _pdf_merge(self, page_num: int) -> None:
        bs_reader = self._load_pdf_reader(self.bs)

        existing_pdf_page = self.reader.pages[page_num]
        bs_pdf_page = bs_reader.pages[page_num]

        existing_pdf_page.merge_page(bs_pdf_page)
        self.writer.add_page(existing_pdf_page)


    def write_to_pdf_output(self) -> None:
        for i in range(self.reader_page_num):
            self._pdf_merge(i)

        with open(self.output_file, 'wb') as f:
            self.writer.write(f)

        self.stream_by_input.close()

