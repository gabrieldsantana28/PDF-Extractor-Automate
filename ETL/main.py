import os
from dotenv import load_dotenv
from readers.pdf_reader import PDFReader

load_dotenv()

FILE_NAME = os.getenv("FILE_NAME_2026T1")

PDF_PATH = os.path.abspath(
    f"ETL/{os.getenv('FILE_PATH')}{FILE_NAME}.pdf"
)


def main():

    reader = PDFReader(PDF_PATH)

    paginas = reader.locate_pages()

    print()
    print("Páginas iniciais encontradas:")
    print(paginas)

    reader.read_page(paginas[0])

if __name__ == "__main__":
    main()