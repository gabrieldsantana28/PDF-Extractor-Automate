import re


class HospitalizationsTransformer:

    TIPOS_INTERNACAO = {
        "Internações Clínicas": "Internações Clínicas",
        "Internações Cirúrgicas": "Internações Cirúrgicas",
        "Obstétrica": "Obstétrica",
        "Internações Pediatricas": "Internações Pediátricas",
        "Psquiatria": "Psiquiatria"
    }

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])
        resultado = []

        for registro in dados:

            valor = registro["valores_por_periodo"].get(cd_periodo)

            if valor is None:
                raise ValueError(
                    f"Período {cd_periodo} não encontrado para "
                    f"{registro['tipo_internacao']}."
                )

            resultado.append({
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_tipo_internacao": self.TIPOS_INTERNACAO.get(
                    registro["tipo_internacao"],
                    registro["tipo_internacao"]
                ),
                "qtd_internacoes": self._to_number(valor)
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

        return int(str(valor).replace(".", ""))
