import re


class TicketCostTransformer:

    CD_GRAFICO = "TIQUETE_MEDIO_CUSTO_PER_CAPITA_DIOPS"

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])
        registros_periodo = [
            registro
            for registro in dados
            if registro["cd_periodo"] == cd_periodo
        ]

        if len(registros_periodo) != 2:
            raise ValueError(
                f"Período {cd_periodo} não encontrado por completo "
                "no gráfico de tíquete médio e custo per capita."
            )

        return [
            {
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_grafico": self.CD_GRAFICO,
                "cd_indicador": registro["cd_indicador"],
                "tp_entidade": "UNIMED",
                "ds_entidade": header["unimed"],
                "valor": self._to_number(registro["valor"])
            }
            for registro in registros_periodo
        ]

    def _get_cd_periodo(self, periodo):

        match = re.search(
            r"(\d+)[º°] trimestre de (\d{4})",
            periodo.lower()
        )

        if not match:
            raise ValueError(
                f"Não foi possível identificar o período: {periodo}"
            )

        return f"{match.group(2)}T{match.group(1)}"

    def _to_number(self, valor):

        return float(
            str(valor).replace(".", "").replace(",", ".")
        )
