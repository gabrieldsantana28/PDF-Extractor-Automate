import logging
from dotenv import load_dotenv

from _readers.pdf_reader import PDFReader
from _exporters.excel_exporter import export_to_excel
from _pipeline.extraction_pipeline import ExtractionPipeline
from _utils.paths import build_paths
from _utils.logging_config import setup_logging

load_dotenv()
LOG_FILE = setup_logging()

logger = logging.getLogger(__name__)


def main():

    try:
        FILE_NAME, PDF_PATH, OUTPUT_PATH = build_paths(
            "FILE_NAME_2026T1_SC"
        )

        logger.info(
            "ETL iniciado | arquivo=%s | log=%s",
            FILE_NAME,
            LOG_FILE
        )

        reader = PDFReader(PDF_PATH)
        paginas = reader.locate_pages()

        pipeline = ExtractionPipeline(reader)
        dados = pipeline.extract_all(paginas)

        logger.info("Exportação para Excel iniciada")
        dataframes = export_to_excel(dados, OUTPUT_PATH)

        for nome_aba, dataframe in dataframes.items():
            logger.info(
                "Conjunto processado | nome=%s | registros=%d",
                nome_aba,
                len(dataframe)
            )

        logger.info(
            "ETL concluído com sucesso | arquivo_saida=%s",
            OUTPUT_PATH
        )

    except Exception:
        logger.exception("ETL finalizado com erro")
        raise

if __name__ == "__main__":
    main()
