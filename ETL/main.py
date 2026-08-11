import os
import pandas as pd

from dotenv import load_dotenv

from readers.pdf_reader import PDFReader
from extractors.header import HeaderExtractor
from extractors.events import EventsExtractor
from transformers.events import EventsTransformer


load_dotenv()

FILE_NAME = os.getenv("FILE_NAME_2025T4")

PDF_PATH = os.path.abspath(
    f"ETL/{os.getenv('FILE_PATH')}{FILE_NAME}.pdf"
)


def main():

    
    # # ==========================================
    # # PDF READER
    # # ==========================================

    reader = PDFReader(PDF_PATH)

    paginas = reader.locate_pages()

    texto_pagina_2 = reader.get_page_text(
        paginas[0]
    )

    print(texto_pagina_2)

    # print()
    # print("=" * 50)
    # print("PÁGINAS ENCONTRADAS")
    # print("=" * 50)
    # print(paginas)


    # # ==========================================
    # # TEXTO DA PÁGINA
    # # ==========================================

    # texto = reader.get_page_text(paginas[0])


    # # ==========================================
    # # HEADER
    # # ==========================================

    # header_extractor = HeaderExtractor()

    # header = header_extractor.extract(texto)

    # print()
    # print("=" * 50)
    # print("HEADER")
    # print("=" * 50)
    # print(header)


    # # ==========================================
    # # EVENTS EXTRACTOR
    # # ==========================================

    # events_extractor = EventsExtractor()

    # dados_eventos = events_extractor.extract(texto)

    # print()
    # print("=" * 50)
    # print("DADOS EXTRAÍDOS")
    # print("=" * 50)

    # print(dados_eventos)


    # # ==========================================
    # # EVENTS TRANSFORMER
    # # ==========================================

    # events_transformer = EventsTransformer()

    # dados_tf_eventos = events_transformer.transform(
    #     dados_eventos,
    #     header
    # )

    # print()
    # print("=" * 50)
    # print("DADOS TRANSFORMADOS")
    # print("=" * 50)

    # for linha in dados_tf_eventos:
    #     print(linha)


if __name__ == "__main__":
    main()