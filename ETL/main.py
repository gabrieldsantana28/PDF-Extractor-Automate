# BIBLIOTECAS
import os
import pandas as pd
from dotenv import load_dotenv

from _readers.pdf_reader import PDFReader
from _exporters.excel_exporter import export_to_excel
from _pipeline.extraction_pipeline import ExtractionPipeline
from _utils.paths import build_paths

load_dotenv()

def main():

    FILE_NAME, PDF_PATH, OUTPUT_PATH = build_paths(
        "FILE_NAME_2026T1_SC"
    )

    reader = PDFReader(PDF_PATH)
    paginas = reader.locate_pages()

    pipeline = ExtractionPipeline(reader)

    dados = pipeline.extract_all(paginas)

    dataframes = export_to_excel(dados, OUTPUT_PATH)

    print()
    print("=" * 50)
    print("EXCEL GERADO")
    print("=" * 50)
    print(OUTPUT_PATH)

    for nome_aba, dataframe in dataframes.items():
        print(f"{nome_aba}: {len(dataframe)} registros")

if __name__ == "__main__":
    main()
