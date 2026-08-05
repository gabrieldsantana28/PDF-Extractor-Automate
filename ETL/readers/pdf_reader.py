import pdfplumber

from extractors.header import HeaderExtractor

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

            extractor = HeaderExtractor()

            dados = extractor.extract(texto)

            return dados

    def extract_header(self, pagina):
        text = pagina.extract_text()

        dados = {
            "unimed": None,
            "codigo_unimed": None,
            "codigo_ans": None,
            "municipio": None,
            "estado": None,
            "regiao": None,
            "tipo_cooperativa": None,
            "beneficiarios": None,
            "colaboradores": None,
            "medicos": None,
            "porte": None
        }

        for linha in text.split("\n"):

            linha = linha.strip()

            if linha.startswith("UNIMED"):
                dados["unimed"] = linha

            elif "CÓDIGO UNIMED:" in linha:
                dados["codigo_unimed"] = linha.split("CÓDIGO UNIMED:")[1].split()[0]

            elif "CÓDIGO ANS:" in linha:
                dados["codigo_ans"] = linha.split("CÓDIGO ANS:")[1].split()[0]

            elif "MUNICÍPIO SEDE:" in linha:
                dados["municipio"] = linha.split("MUNICÍPIO SEDE:")[1].strip()

            elif "ESTADO:" in linha:
                dados["estado"] = linha.split("ESTADO:")[1].strip()

            elif "REGIÃO:" in linha:
                dados["regiao"] = linha.split("REGIÃO:")[1].strip()

            elif "TIPO COOPERATIVA:" in linha:
                dados["tipo_cooperativa"] = linha.split("TIPO COOPERATIVA:")[1].split("Nº")[0].strip()

            elif "TOTAL DE BENEFICIÁRIOS:" in linha:
                dados["beneficiarios"] = linha.split("TOTAL DE BENEFICIÁRIOS:")[1].split("PORTE")[0].strip()

            elif "Nº DE COLABORADORES:" in linha:
                dados["colaboradores"] = linha.split("Nº DE COLABORADORES:")[1].strip()

            elif "Nº DE MÉDICOS COOPERADOS:" in linha:
                dados["medicos"] = linha.split("Nº DE MÉDICOS COOPERADOS:")[1].strip()

            elif "PORTE:" in linha:
                dados["porte"] = linha.split("PORTE:")[1].strip()

        return dados

    # def extract_doc_info(self):

    # def extract_ud_info(self, page_index):

    