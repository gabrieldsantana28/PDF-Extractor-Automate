import os
import pandas as pd
from dotenv import load_dotenv
from readers.pdf_reader import PDFReader

load_dotenv()

FILE_NAME = os.getenv("FILE_NAME_2025T4")

PDF_PATH = os.path.abspath(
    f"ETL/{os.getenv('FILE_PATH')}{FILE_NAME}.pdf"
)


def main():

    reader = PDFReader(PDF_PATH)

    paginas = reader.locate_pages()

    dados_unimeds = []

    for pagina in paginas:

        dados = reader.read_page(pagina)

        dados_unimeds.append(dados)

    print()
    print("=" * 50)
    print(f"TOTAL DE UNIMEDS EXTRAÍDAS: {len(dados_unimeds)}")
    print("=" * 50)

    # Transformando os dados em DataFrame
    df = pd.DataFrame(dados_unimeds)

    print()

    output_path = os.path.abspath(
        f"ETL/files/output/{FILE_NAME}.xlsx"
    )

    df.to_excel(
        output_path,
        index=False
    )

    print()
    print("=" * 50)
    print("EXCEL GERADO COM SUCESSO")
    print("=" * 50)
    print(output_path)


if __name__ == "__main__":
    main()