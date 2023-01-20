from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

class BlankPDF(object):
    OUTPUT_FILE = 'blank_pdf.pdf'

    def __init__(self, output_file = OUTPUT_FILE, page_size=A4) -> None:
        self.output_file = output_file
        self.page_size = page_size
        self.bt_stream = io.BytesIO()
        self.cs = canvas.Canvas(self.bt_stream)
        self.writer = PdfWriter()
        self._initialize_make_blank_page(canvas=self.cs, page_size=self.page_size)


    def _initialize_make_blank_page(self, canvas: canvas.Canvas, page_size: tuple[float, float]):
        canvas.setPageSize(page_size)
        canvas.showPage()
        canvas.save()

        blank_pdf_reader = PdfReader(self.bt_stream)
        self.writer.add_page(blank_pdf_reader.pages[0])


    def write(self):
        with open(self.output_file, 'wb') as f:
            self.writer.write(f)

if __name__ == '__main__':
    blank_pdf = BlankPDF()
    blank_pdf.write()

