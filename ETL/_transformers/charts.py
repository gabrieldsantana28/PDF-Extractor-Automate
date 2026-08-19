import re


class ChartsTransformer:

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])
        descricoes_entidades = self._get_descricoes_entidades(header)

        return [
            {
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_grafico": registro["cd_grafico"],
                "cd_indicador": registro["cd_indicador"],
                "tp_entidade": registro["tp_entidade"],
                "ds_entidade": descricoes_entidades[
                    registro["tp_entidade"]
                ],
                "valor": self._to_number(registro["valor"])
            }
            for registro in dados
        ]

    def _get_descricoes_entidades(self, header):

        porte = header["porte"].split("-")[0].strip().title()
        regiao = header["regiao"].upper()

        return {
            "UNIMED": header["unimed"],
            "PORTE_REGIAO": (
                f"Unimeds {porte} Porte - Região {regiao}"
            ),
            "PORTE_NACIONAL": (
                f"Unimeds {porte} Porte - Média Nacional"
            ),
            "MEDIA_NACIONAL_GERAL": "Média Nacional Geral"
        }

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

        return int(str(valor).replace(".", ""))
