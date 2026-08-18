import re


class HeaderExtractor:

    def extract(self, text):

        linhas = [l.strip() for l in text.split("\n") if l.strip()]

        dados = {
            "unimed": linhas[3],
            "periodo": linhas[4],
            "codigo_unimed": None,
            "codigo_ans": None,
            "municipio": None,
            "estado": None,
            "regiao": None,
            "tipo_cooperativa": None,
            "beneficiarios": None,
            "colaboradores": None,
            "medicos": None,
            "porte": None
        }

        # Linha 5
        m = re.search(
            r"MUNICÍPIO SEDE:\s*(.+)",
            linhas[5]
        )

        if m:
            dados["municipio"] = m.group(1).strip()

        # Linha 6
        m = re.search(
            r"ESTADO:\s*(.+)",
            linhas[6]
        )

        if m:
            dados["estado"] = m.group(1).strip()

        # Linha 7
        m = re.search(
            r"CÓDIGO UNIMED:\s*(\d+).*REGIÃO:\s*(.+)",
            linhas[7]
        )

        if m:
            dados["codigo_unimed"] = int(m.group(1))
            dados["regiao"] = m.group(2).strip()

        # Linha 8
        m = re.search(
            r"CÓDIGO ANS:\s*(\d+).*COLABORADORES:\s*([\d\.]+)",
            linhas[8]
        )

        if m:
            dados["codigo_ans"] = int(m.group(1))
            dados["colaboradores"] = int(
                m.group(2).replace(".", "")
            )

        # Linha 9
        m = re.search(
            r"TIPO COOPERATIVA:\s*(.+?)\s*Nº DE MÉDICOS COOPERADOS:\s*(\d+)",
            linhas[9]
        )

        if m:
            dados["tipo_cooperativa"] = m.group(1).strip()
            dados["medicos"] = int(m.group(2))

        # Linha 10
        m = re.search(
            r"TOTAL DE BENEFICIÁRIOS:\s*([\d\.]+)\s*PORTE:\s*(.+)",
            linhas[10]
        )

        if m:
            dados["beneficiarios"] = int(
                m.group(1).replace(".", "")
            )

            dados["porte"] = m.group(2).strip()

        return dados