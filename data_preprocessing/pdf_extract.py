from PyPDF2 import PdfReader


def pdf_extract(path: str) -> list[str]:
    with open(path, 'rb') as f:

        reader = PdfReader(f)

        text = []

        for page_num in range(6, len(reader.pages)):
            page = reader.pages[page_num]
            text.append(page.extract_text().replace('\uf0b7', '').replace('\n', ''))

    return text

