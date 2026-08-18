import re


class HospitalizationsExtractor:

    TIPOS_INTERNACAO = [
        "Internações Clínicas",
        "Internações Cirúrgicas",
        "Obstétrica",
        "Internações Pediatricas",
        "Psquiatria"
    ]

    def extract(self, texto):

        linhas = [
            linha.strip()
            for linha in texto.splitlines()
            if linha.strip()
        ]

        periodos = self._extract_periodos(linhas)
        resultados = []

        for linha in linhas:

            tipo_encontrado = next(
                (
                    tipo
                    for tipo in self.TIPOS_INTERNACAO
                    if linha.startswith(tipo)
                ),
                None
            )

            if tipo_encontrado is None:
                continue

            restante = linha[len(tipo_encontrado):].strip()
            valores = re.findall(r"\d[\d.]*", restante)

            if len(valores) < len(periodos):
                continue

            resultados.append({
                "tipo_internacao": tipo_encontrado,
                "valores_por_periodo": dict(
                    zip(periodos, valores[:len(periodos)])
                )
            })

        return resultados

    def _extract_periodos(self, linhas):

        linha_periodos = next(
            (
                linha
                for linha in linhas
                if linha.startswith("Tipo de Internações")
            ),
            None
        )

        if linha_periodos is None:
            raise ValueError(
                "Cabeçalho dos períodos de internação não encontrado."
            )

        periodos_encontrados = re.findall(
            r"(\d+)[º°]\s*TRIM\s*(\d{2,4})",
            linha_periodos,
            flags=re.IGNORECASE
        )

        if not periodos_encontrados:
            raise ValueError(
                "Nenhum período foi encontrado na tabela de internações."
            )

        return [
            f"{self._normalize_ano(ano)}T{trimestre}"
            for trimestre, ano in periodos_encontrados
        ]

    def _normalize_ano(self, ano):

        if len(ano) == 2:
            return f"20{ano}"

        return ano
