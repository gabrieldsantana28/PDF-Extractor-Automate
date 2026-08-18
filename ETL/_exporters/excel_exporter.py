import os
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

def export_to_excel(dados, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    dataframes = {
        nome_aba: pd.DataFrame(registros)
        for nome_aba, registros in dados.items()
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        for nome_aba, dataframe in dataframes.items():
            dataframe.to_excel(
                writer,
                sheet_name=nome_aba,
                index=False
            )

            worksheet = writer.sheets[nome_aba]
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            worksheet.sheet_view.showGridLines = False

            for cell in worksheet[1]:
                cell.fill = PatternFill(
                    fill_type="solid",
                    fgColor="006B64"
                )
                cell.font = Font(bold=True, color="FFFFFF")
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

            for indice_coluna, coluna in enumerate(
                worksheet.iter_cols(),
                start=1
            ):
                largura = min(
                    max(
                        len(str(celula.value))
                        if celula.value is not None
                        else 0
                        for celula in coluna
                    ) + 2,
                    45
                )

                worksheet.column_dimensions[
                    get_column_letter(indice_coluna)
                ].width = largura

    return dataframes