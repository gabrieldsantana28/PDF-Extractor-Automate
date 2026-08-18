import re


class EventsExtractor:

    CATEGORIAS_EVENTOS = [
        "Consultas (Amb+PS)",
        "Outros Atend. Amb.",
        "Exames",
        "Terapias",
        "Internações",
        "Total Eventos"
    ]

    CATEGORIAS_DESPESAS = [
        "Consultas (Amb+PS)",
        "Outros Atend. Amb.",
        "Exames",
        "Terapias",
        "Internações",
        "Demais Desp Amb e Hosp",
        "Total Despesas Assistenciais R$"
    ]

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

            # INÍCIO DA TABELA DE EVENTOS
            if linha.startswith("Tipo de evento"):
                modo = "eventos"
                continue

            # INÍCIO DA TABELA DE DESPESAS
            if linha.startswith("Tipo da despesa"):
                modo = "despesas"
                continue

            # FIM DAS TABELAS
            if linha.startswith("Comparativo dos Indicadores"):
                modo = None
                continue

            if modo is None:
                continue

            # IGNORA FONTE
            if linha.startswith("FONTE:"):
                continue

            # EXTRAI EVENTOS
            if modo == "eventos":

                dados = self._extract_linha(
                    linha,
                    self.CATEGORIAS_EVENTOS
                )

                if dados:
                    eventos.append(dados)

            # EXTRAI DESPESAS
            elif modo == "despesas":

                dados = self._extract_linha(
                    linha,
                    self.CATEGORIAS_DESPESAS
                )

                if dados:
                    despesas.append(dados)

        return {
            "eventos": eventos,
            "despesas": despesas
        }

    def _extract_linha(self, linha, categorias):

        categoria = None
        restante = None

        for nome_categoria in categorias:

            if linha.startswith(nome_categoria):

                categoria = nome_categoria

                restante = linha[len(nome_categoria):].strip()

                break

        if categoria is None:
            return None



        numeros = re.findall(
            r"\d[\d.]*,\d+|\d[\d.]*",
            restante
        )

        # Precisamos de:
        #
        # período 1
        # período 2
        # período 3
        # período 4
        # total
        # percentual
        #
        # Os números posteriores pertencem
        # aos gráficos e serão ignorados.

        if len(numeros) < 6:
            return None

        valores = numeros[:6]

        return {
            "descricao": categoria,
            "valor_periodo_1": valores[0],
            "valor_periodo_2": valores[1],
            "valor_periodo_3": valores[2],
            "valor_periodo_4": valores[3],
            "valor_total": valores[4],
            "percentual": valores[5]
        }