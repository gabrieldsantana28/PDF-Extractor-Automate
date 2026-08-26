import logging
import os

import pdfplumber


logger = logging.getLogger(__name__)


class PDFReader:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

        logger.debug(
            "Leitor de PDF criado | arquivo=%s",
            os.path.basename(pdf_path)
        )

    def get_total_pages(self):

        with pdfplumber.open(self.pdf_path) as pdf:
            return len(pdf.pages)

    def locate_pages(self):

        paginas_unimed = []

        logger.info(
            "Localização de páginas iniciada | arquivo=%s",
            os.path.basename(self.pdf_path)
        )

        with pdfplumber.open(self.pdf_path) as pdf:
            logger.info("PDF aberto | total_paginas=%d", len(pdf.pages))

            for indice, pagina in enumerate(pdf.pages):

                texto = pagina.extract_text()

                if texto is None:
                    logger.warning(
                        "Página sem texto ignorada | pagina=%d",
                        indice + 1
                    )
                    continue

                if (
                    texto.startswith("RELATÓRIO DE EVENTOS")
                    or texto.startswith("RECA")
                ):
                    paginas_unimed.append(indice + 1)
                    logger.debug(
                        "Página inicial de Unimed localizada | pagina=%d",
                        indice + 1
                    )

        logger.info(
            "Localização de páginas concluída | blocos_unimed=%d",
            len(paginas_unimed)
        )

        return paginas_unimed

    def get_page_text(self, page_index):

        logger.debug("Extraindo texto integral | pagina=%d", page_index)

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

        logger.debug(
            "Extraindo região de texto | pagina=%d | inicio=%s | fim=%s",
            page_index,
            start_text,
            end_text
        )

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

    def get_page_region_words(
        self,
        page_index,
        start_text,
        end_text=None,
        top_padding=2,
        bottom_padding=2
    ):

        logger.debug(
            "Extraindo palavras por região | pagina=%d | inicio=%s | fim=%s",
            page_index,
            start_text,
            end_text
        )

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

            top = min(
                inicio["bottom"] + top_padding,
                pagina.height
            )

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

                bottom = max(
                    fim["top"] - bottom_padding,
                    top
                )

            else:
                bottom = pagina.height

            regiao = pagina.crop(
                (0, top, pagina.width, bottom)
            )

            return {
                "page_width": pagina.width,
                "top": top,
                "bottom": bottom,
                "words": regiao.extract_words(
                    x_tolerance=1,
                    y_tolerance=2
                )
            }
