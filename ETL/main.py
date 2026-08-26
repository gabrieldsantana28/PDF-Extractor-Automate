# BIBLIOTECAS
import os
import logging
import pandas as pd

from dotenv import load_dotenv

from _readers.pdf_reader import PDFReader
from _exporters.excel_exporter import export_to_excel
from _pipeline.extraction_pipeline import ExtractionPipeline
from _utils.paths import build_paths
from _utils.logging_config import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

def main():

    try:
        os.makedirs("ETL/logs", exist_ok=True)

        FILE_NAME, PDF_PATH, OUTPUT_PATH = build_paths(
            "FILE_NAME_2026T1_SC"
        )

        logger.info(f"Processando arquivo: {FILE_NAME}")

        reader = PDFReader(PDF_PATH)
        logger.info(f"Total de páginas no PDF: {reader.get_total_pages()}")

        paginas = reader.locate_pages()
        logger.info(f"Total de páginas localizadas: {len(paginas)}")

        pipeline = ExtractionPipeline(reader)
        logger.info("Iniciando extração de dados...")

        dados = pipeline.extract_all(paginas)
        logger.info("Extração de dados concluída.")

        dataframes = export_to_excel(dados, OUTPUT_PATH)
        logger.info("Exportando para Excel...")

        logger.info(f"Arquivo Excel gerado em: {OUTPUT_PATH}")

        for nome_aba, dataframe in dataframes.items():
            logger.info(f"{nome_aba}: {len(dataframe)} registros")

    except Exception as e:
        logger.exception(f"Erro durante a execução do ETL: {e}")
        raise

if __name__ == "__main__":
    main()
