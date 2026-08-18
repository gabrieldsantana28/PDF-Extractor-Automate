import os


def build_paths(file_env_key):

    file_name = os.getenv(file_env_key)

    file_path = os.getenv("FILE_PATH")

    pdf_path = os.path.abspath(
        f"ETL/{file_path}{file_name}.pdf"
    )

    output_dir = os.path.abspath("ETL/output")

    output_path = os.path.join(
        output_dir,
        f"{file_name}_extraido.xlsx"
    )

    return file_name, pdf_path, output_path