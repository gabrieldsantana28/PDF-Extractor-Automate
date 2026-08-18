import re


class ExpensesExtractor:

    TIPOS_DESPESA = [
        "Despesas assistenciais pagamento por procedimento",
        "Despesas assistenciais pagamento por capitation",
        "Despesas assistenciais pagamento por orçamento global",
        "Despesas assistenciais pagamento por pacote",
        "Despesas assistenciais por rateio de custos de recursos próprios",
        "Despesas assistenciais pagamento prestados por rede indireta",
        "Despesas assistenciais pagamento por reembolso",
        "Despesas assistenciais no Sistema Único de Saúde - SUS",
        "Despesas assistenciais - Outras formas de pagamento"
    ]

    VALOR_E_PERCENTUAL = re.compile(
        r"^(?P<valor>-\s*(?:\d[\d.\s]*)?|\d[\d.\s]*?)"
        r"\s+(?P<percentual>\d+,\d+%)"
    )

    def extract(self, texto):

        linhas = [
            linha.strip()
            for linha in texto.split("\n")
            if linha.strip()
        ]

        despesas_assistenciais = []
        dentro_bloco = False

        for linha in linhas:

            if linha.startswith("Descrição por tipo de despesa"):
                dentro_bloco = True
                continue

            if linha.startswith(
                "Total de despesas assistenciais avisadas/conhecidas"
            ):
                break

            if not dentro_bloco:
                continue

            dados = self._extract_linha(linha)

            if dados:
                despesas_assistenciais.append(dados)

        return {
            "despesas_assistenciais": despesas_assistenciais
        }

    def _extract_linha(self, linha):

        tipo_despesa = next(
            (
                tipo
                for tipo in self.TIPOS_DESPESA
                if linha.startswith(tipo)
            ),
            None
        )

        if tipo_despesa is None:
            return None

        restante = linha[len(tipo_despesa):].strip()
        match = self.VALOR_E_PERCENTUAL.match(restante)

        if not match:
            raise ValueError(
                f"Não foi possível extrair o valor da despesa: {linha}"
            )

        return {
            "tipo_despesa": tipo_despesa,
            "valor": match.group("valor").strip()
        }
