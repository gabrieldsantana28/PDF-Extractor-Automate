import pdfplumber


class PDFReader:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def locate_pages(self):

        paginas_unimed = []

        with pdfplumber.open(self.pdf_path) as pdf:

            print("=" * 30)
            print(f"Total de páginas: {len(pdf.pages)}")
            print("=" * 30)

            for indice, pagina in enumerate(pdf.pages):

                texto = pagina.extract_text()

                if texto is None:
                    continue

                if (
                    texto.startswith("RELATÓRIO DE EVENTOS")
                    or texto.startswith("RECA")
                ):
                    paginas_unimed.append(indice + 1)

                    print(
                        f"Página {indice + 1} encontrada."
                    )

        return paginas_unimed

    def get_page_text(self, page_index):

        with pdfplumber.open(self.pdf_path) as pdf:

            pagina = pdf.pages[page_index - 1]

            return pagina.extract_text()