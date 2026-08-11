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

    dados = reader.read_page(paginas[0])

    print()
    print("=" * 50)
    print("HEADER")
    print("=" * 50)

    print(dados["header"])

    print()
    print("=" * 50)
    print("EVENTOS")
    print("=" * 50)

    for evento in dados["eventos"]:
        print(evento)

    print()
    print("=" * 50)
    print("DESPESAS")
    print("=" * 50)

    for despesa in dados["despesas"]:
        print(despesa)

    # output_path = os.path.abspath(
    #     f"ETL/files/output/{FILE_NAME}.xlsx"
    # )

    # df.to_excel(
    #     output_path,
    #     index=False
    # )

    # print()
    # print("=" * 50)
    # print("EXCEL GERADO COM SUCESSO")
    # print("=" * 50)
    # print(output_path)


if __name__ == "__main__":
    main()