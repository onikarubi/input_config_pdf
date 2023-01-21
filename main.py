from PyPDF2 import PdfReader

if __name__ == '__main__':
    input_file = './pdf_file/isouhi_edit(墨消し).pdf'

    with open(input_file, 'rb') as f:
        reader = PdfReader(f)

        fields = reader.get_fields()

        for key, value in fields.items():
            print(key, value['/V'])

# Declaration

