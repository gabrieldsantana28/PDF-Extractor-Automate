import os
import pandas as pd

from dotenv import load_dotenv

from readers.pdf_reader import PDFReader

from extractors.header import HeaderExtractor
from extractors.events import EventsExtractor
from extractors.indicators import IndicatorsExtractor

from transformers.events import EventsTransformer
from transformers.indicators import IndicatorsTransformer


load_dotenv()

FILE_NAME = os.getenv("FILE_NAME_2025T4")

PDF_PATH = os.path.abspath(
    f"ETL/{os.getenv('FILE_PATH')}{FILE_NAME}.pdf"
)


def main():

    reader = PDFReader(PDF_PATH)

    paginas = reader.locate_pages()

    # ==========================================
    # PDF READER
    # ==========================================

    print()
    print("=" * 50)
    print("PÁGINAS ENCONTRADAS")
    print("=" * 50)
    print(paginas)


    # ==========================================
    # TEXTO DA PÁGINA
    # ==========================================

    texto = reader.get_page_text(paginas[0])


    # ==========================================
    # HEADER
    # ==========================================

    header_extractor = HeaderExtractor()

    header = header_extractor.extract(texto)

    print()
    print("=" * 50)
    print("HEADER")
    print("=" * 50)
    print(header)


    # ==========================================
    # EVENTS EXTRACTOR
    # ==========================================

    events_extractor = EventsExtractor()

    dados_eventos = events_extractor.extract(texto)

    print()
    print("=" * 50)
    print("DADOS EXTRAÍDOS")
    print("=" * 50)

    print(dados_eventos)

    # ==========================================
    # INDICATORS EXTRACTOR
    # ==========================================

    indicators_extractor = IndicatorsExtractor()

    dados_indicadores = indicators_extractor.extract(texto)

    print()
    print("=" * 50)
    print("INDICADORES ASSISTENCIAIS")
    print("=" * 50)

    for indicador in dados_indicadores:
        print(indicador)

    # ==========================================
    # INDICATORS TRANSFORMER
    # ==========================================

    indicators_transformer = IndicatorsTransformer()

    dados_tf_indicadores = indicators_transformer.transform(
        dados_indicadores,
        header
    )

    print()
    print("=" * 50)
    print("INDICADORES TRANSFORMADOS")
    print("=" * 50)

    for linha in dados_tf_indicadores:
        print(linha)

    print(f"Total de indicadores transformados: {len(dados_tf_indicadores)}")

    # ==========================================
    # EVENTS TRANSFORMER
    # ==========================================

    events_transformer = EventsTransformer()

    dados_tf_eventos = events_transformer.transform(
        dados_eventos,
        header
    )

    print()
    print("=" * 50)
    print("DADOS TRANSFORMADOS")
    print("=" * 50)

    for linha in dados_tf_eventos:
        print(linha)


if __name__ == "__main__":
    main()
