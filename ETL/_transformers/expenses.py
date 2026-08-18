import re


class ExpensesTransformer:

    def transform(self, dados, header):

        cd_periodo = self._get_cd_periodo(header["periodo"])
        resultado = []

        for despesa in dados["despesas_assistenciais"]:

            resultado.append({
                "cd_unimed": header["codigo_unimed"],
                "cd_periodo": cd_periodo,
                "cd_tipo_despesa": despesa["tipo_despesa"],
                "valor": self._to_number(despesa["valor"])
            })

        return resultado

    def _get_cd_periodo(self, periodo):

        match = re.search(
            r"(\d+)[º°] trimestre(?: de)?\s*(\d{4})",
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

        valor = str(valor).strip()
        negativo = valor.startswith("-")
        digitos = re.sub(r"\D", "", valor)

        if not digitos:
            return 0

        numero = int(digitos)

        if negativo:
            numero *= -1

        return numero
