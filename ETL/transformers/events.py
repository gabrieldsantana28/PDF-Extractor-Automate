import re


class EventsTransformer:

    CATEGORIAS_EVENTOS = {
        "Consultas (Amb+PS)": "CONSULTAS_AMB_PS",
        "Outros Atend. Amb.": "OUTROS_ATEND_AMB",
        "Exames": "EXAMES",
        "Terapias": "TERAPIAS",
        "Internações": "INTERNACOES",
        "Total Eventos": "TOTAL_EVENTOS"
    }

    CATEGORIAS_DESPESAS = {
        "Consultas (Amb+PS)": "CONSULTAS_AMB_PS",
        "Outros Atend. Amb.": "OUTROS_ATEND_AMB",
        "Exames": "EXAMES",
        "Terapias": "TERAPIAS",
        "Internações": "INTERNACOES",
        "Demais Desp Amb e Hosp": "DEMAIS_DESP_AMB_HOSP",
        "Total Despesas Assistenciais R$": "TOTAL_DESPESAS_ASSISTENCIAIS"
    }

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])

        resultado = []

        # ==========================================
        # EVENTOS
        # ==========================================

        for evento in dados["eventos"]:

            categoria = self.CATEGORIAS_EVENTOS.get(
                evento["descricao"]
            )

            if categoria is None:
                continue

            valor = self._to_number(
                evento["valor_periodo_4"]
            )

            resultado.append({
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_categoria": evento["descricao"],
                "tp_medida": "EVENTOS",
                "valor": valor
            })

        # ==========================================
        # DESPESAS
        # ==========================================

        for despesa in dados["despesas"]:

            categoria = self.CATEGORIAS_DESPESAS.get(
                despesa["descricao"]
            )

            if categoria is None:
                continue

            valor = self._to_number(
                despesa["valor_periodo_4"]
            )

            resultado.append({
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_categoria": despesa["descricao"],
                "tp_medida": "DESPESA",
                "valor": valor
            })

        return resultado

    def _get_cd_periodo(self, periodo):

        match = re.search(
            r"(\d+)[º°] trimestre de (\d{4})",
            periodo.lower()
        )

        if not match:
            raise ValueError(
                f"Não foi possível identificar o período: {periodo}"
            )

        trimestre = match.group(1)
        ano = match.group(2)

        return f"{ano}T{trimestre}"

    def _to_number(self, valor):

        if valor is None:
            return None

        valor = str(valor).strip()

        # Remove separador de milhar
        valor = valor.replace(".", "")

        # Converte decimal brasileiro
        valor = valor.replace(",", ".")

        return float(valor)