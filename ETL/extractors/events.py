import re


class EventsExtractor:

    def extract(self, texto):

        linhas = [
            linha.strip()
            for linha in texto.split("\n")
            if linha.strip()
        ]

        eventos = []
        despesas = []

        modo = None

        for linha in linhas:

            # ==============================
            # INÍCIO DA TABELA DE EVENTOS
            # ==============================
            if linha.startswith("Tipo de evento"):
                modo = "eventos"
                continue

            # ==============================
            # INÍCIO DA TABELA DE DESPESAS
            # ==============================
            if linha.startswith("Tipo da despesa"):
                modo = "despesas"
                continue

            # ==============================
            # FIM DAS TABELAS
            # ==============================
            if linha.startswith("Comparativo dos Indicadores"):
                modo = None
                continue

            if linha.startswith("FONTE:"):
                continue

            # ==============================
            # IGNORA LINHAS QUE NÃO SÃO DADOS
            # ==============================
            if modo is None:
                continue

            # Ignora percentuais isolados dos gráficos
            if re.fullmatch(r"[\d,]+%", linha):
                continue

            # ==============================
            # EXTRAI LINHA
            # ==============================
            dados = self._extract_linha(linha)

            if dados is None:
                continue

            if modo == "eventos":
                eventos.append(dados)

            elif modo == "despesas":
                despesas.append(dados)

        return {
            "eventos": eventos,
            "despesas": despesas
        }

    def _extract_linha(self, linha):

        # Procura todos os números da linha
        numeros = re.findall(
            r"\d[\d.]*,\d+|\d[\d.]*",
            linha
        )

        if len(numeros) < 6:
            return None

        # Os últimos 6 valores são:
        # período 1
        # período 2
        # período 3
        # período 4
        # total
        # percentual

        valores = numeros[-6:]

        descricao = linha[:linha.find(valores[0])].strip()

        if not descricao:
            return None

        return {
            "descricao": descricao,
            "valor_periodo_1": valores[0],
            "valor_periodo_2": valores[1],
            "valor_periodo_3": valores[2],
            "valor_periodo_4": valores[3],
            "valor_total": valores[4],
            "percentual": valores[5]
        }