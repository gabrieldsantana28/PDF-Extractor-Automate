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

    def get_page_region_text(
        self,
        page_index,
        start_text,
        end_text=None,
        padding=2,
        right_margin=20
    ):

        with pdfplumber.open(self.pdf_path) as pdf:

            pagina = pdf.pages[page_index - 1]

            inicios = pagina.search(start_text, regex=False)

            if not inicios:
                raise ValueError(
                    f"Texto inicial não encontrado na página "
                    f"{page_index}: {start_text}"
                )

            inicio = min(
                inicios,
                key=lambda ocorrencia: ocorrencia["top"]
            )

            x0 = max(inicio["x0"] - padding, 0)
            top = max(inicio["top"] - padding, 0)
            x1 = pagina.width - right_margin

            if end_text:

                finais = [
                    ocorrencia
                    for ocorrencia in pagina.search(end_text, regex=False)
                    if ocorrencia["top"] > inicio["top"]
                ]

                if not finais:
                    raise ValueError(
                        f"Texto final não encontrado na página "
                        f"{page_index}: {end_text}"
                    )

                fim = min(
                    finais,
                    key=lambda ocorrencia: ocorrencia["top"]
                )

                bottom = min(fim["bottom"] + padding, pagina.height)

            else:
                bottom = pagina.height

            regiao = pagina.crop((x0, top, x1, bottom))

            return regiao.extract_text(
                x_tolerance=2,
                y_tolerance=3
            )
