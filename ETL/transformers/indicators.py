import re


class IndicatorsTransformer:

    CATEGORIAS = {
        "Consultas médicas (Amb+P.S)": "CONSULTAS_MEDICAS_AMB_PS",
        "Consultas ambulatoriais": "CONSULTAS_AMBULATORIAIS",
        "Consultas em Pronto Socorro": "CONSULTAS_PRONTO_SOCORRO",
        "Outros Atendimentos Amb.": "OUTROS_ATENDIMENTOS_AMB",
        "Exames": "EXAMES",
        "Terapias": "TERAPIAS",
        "Internações": "INTERNACOES"
    }

    INDICADORES = {
        "Frequência média usuário/ano": "FREQUENCIA_MEDIA_USUARIO_ANO",
        "Taxa média de internação": "TAXA_MEDIA_INTERNACAO",
        "Custo médio do procedimento, em R$": "CUSTO_MEDIO_PROCEDIMENTO",
        "Despesa média do procedimento usuário/ano, em R$": (
            "DESPESA_MEDIA_PROCEDIMENTO_USUARIO_ANO"
        )
    }

    ENTIDADES = (
        ("UNIMED", "valor_unimed"),
        ("PORTE_REGIAO", "valor_regiao"),
        ("PORTE_NACIONAL", "valor_media_porte"),
        ("MEDIA_NACIONAL_GERAL", "valor_media_nacional")
    )

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])
        descricoes_entidades = self._get_descricoes_entidades(header)

        resultado = []

        for registro in dados:

            cd_categoria = self.CATEGORIAS.get(registro["categoria"])
            cd_indicador = self.INDICADORES.get(registro["indicador"])

            if cd_categoria is None or cd_indicador is None:
                continue

            for tp_entidade, campo_valor in self.ENTIDADES:

                resultado.append({
                    "cd_unimed": header["codigo_unimed"],
                    "cd_periodo": cd_periodo,
                    "cd_categoria": cd_categoria,
                    "cd_indicador": cd_indicador,
                    "tp_entidade": tp_entidade,
                    "ds_entidade": descricoes_entidades[tp_entidade],
                    "valor": self._to_number(registro[campo_valor]),
                    "variacao": (
                        self._to_number(registro["variacao"])
                        if tp_entidade == "UNIMED"
                        else None
                    )
                })

        return resultado

    def _get_descricoes_entidades(self, header):

        porte = header["porte"].split("-")[0].strip().title()
        regiao = header["regiao"].upper()

        return {
            "UNIMED": header["unimed"],
            "PORTE_REGIAO": f"Unimeds {porte} Porte - Região {regiao}",
            "PORTE_NACIONAL": f"Unimeds {porte} Porte - Média Nacional",
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

        trimestre = match.group(1)
        ano = match.group(2)

        return f"{ano}T{trimestre}"

    def _to_number(self, valor):

        if valor is None:
            return None

        valor = str(valor).strip()

        if valor in {"-", "#VALOR!", ""}:
            return None

        percentual = valor.endswith("%")

        valor = valor.removesuffix("%")
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

        numero = float(valor)

        if percentual:
            numero /= 100

        return numero
