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

                if texto.startswith("RECA"):
                    paginas_unimed.append(indice+1)
                    print(f"Página {indice + 1} encontrada.")

        return paginas_unimed

    def read_page(self, page_index):
        with pdfplumber.open(self.pdf_path) as pdf:
            pagina = pdf.pages[page_index - 1]
            texto = pagina.extract_text()

            dados = self.extract_header(texto)

            print(dados)

            print("\n" + "=" * 30)
            print(f"Conteúdo da página {page_index}:")
            print("=" * 30)
            print(texto)

    def extract_header(self, text):
        dados = {}

        linhas = text.split("\n")

        dados["unimed"] = linhas[3]

        return dados

    # def extract_doc_info(self):

    # def extract_ud_info(self, page_index):

    