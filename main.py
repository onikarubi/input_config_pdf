from pdf_manager import PDFManager

if __name__ == '__main__':
    pdf_manager = PDFManager('./pdf_file/sample.pdf', output_file='output.pdf')
    pdf_manager.draw_text(x=300, y=200, text='竹内')
    pdf_manager.write_to_pdf_output()


