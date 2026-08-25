import re


class TicketCostExtractor:

    NUMERO_DECIMAL = re.compile(r"^\d[\d.]*,\d+$")
    TRIMESTRE = re.compile(r"^(\d+)")
    ANO = re.compile(r"^(\d{2}|\d{4})$")

    def extract(self, regiao):

        palavras = sorted(
            regiao["words"],
            key=lambda palavra: (palavra["top"], palavra["x0"])
        )

        periodos = self._extract_periodos(palavras)
        valores = [
            palavra
            for palavra in palavras
            if self.NUMERO_DECIMAL.fullmatch(palavra["text"])
        ]

        if len(periodos) != 4:
            raise ValueError(
                "Quantidade inesperada de períodos no gráfico de "
                f"tíquete médio: esperado 4, encontrado {len(periodos)}"
            )

        if len(valores) != 8:
            raise ValueError(
                "Quantidade inesperada de valores no gráfico de "
                f"tíquete médio: esperado 8, encontrado {len(valores)}"
            )

        resultados = []

        for periodo in periodos:
            valores_periodo = sorted(
                valores,
                key=lambda palavra: abs(
                    self._centro_x(palavra) - periodo["centro_x"]
                )
            )[:2]
            valores_periodo.sort(key=self._centro_x)

            resultados.extend([
                {
                    "cd_periodo": periodo["cd_periodo"],
                    "cd_indicador": "TIQUETE_MEDIO",
                    "valor": valores_periodo[0]["text"]
                },
                {
                    "cd_periodo": periodo["cd_periodo"],
                    "cd_indicador": "CUSTO_PER_CAPITA",
                    "valor": valores_periodo[1]["text"]
                }
            ])

        return resultados

    def _extract_periodos(self, palavras):

        periodos = []

        for indice, palavra in enumerate(palavras):
            if palavra["text"].upper() != "TRIM":
                continue

            if indice == 0 or indice + 1 >= len(palavras):
                continue

            palavra_trimestre = palavras[indice - 1]
            palavra_ano = palavras[indice + 1]
            trimestre = self.TRIMESTRE.match(
                palavra_trimestre["text"]
            )
            ano = self.ANO.match(palavra_ano["text"])

            if not trimestre or not ano:
                continue

            ano_normalizado = ano.group(1)
            if len(ano_normalizado) == 2:
                ano_normalizado = f"20{ano_normalizado}"

            periodos.append({
                "cd_periodo": (
                    f"{ano_normalizado}T{trimestre.group(1)}"
                ),
                "centro_x": (
                    palavra_trimestre["x0"] + palavra_ano["x1"]
                ) / 2
            })

        return periodos

    def _centro_x(self, palavra):

        return (palavra["x0"] + palavra["x1"]) / 2
