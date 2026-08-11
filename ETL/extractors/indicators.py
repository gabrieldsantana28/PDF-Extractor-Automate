import re


class IndicatorsExtractor:

    CATEGORIAS = [
        "Consultas médicas (Amb+P.S)",
        "Consultas ambulatoriais",
        "Consultas em Pronto Socorro",
        "Outros Atendimentos Amb.",
        "Exames",
        "Terapias",
        "Internações"
    ]

    INDICADORES = [
        "Frequência média usuário/ano",
        "Taxa média de internação",
        "Custo médio do procedimento, em R$",
        "Despesa média do procedimento usuário/ano, em R$"
    ]

    def extract(self, texto):

        linhas = [
            linha.strip()
            for linha in texto.split("\n")
            if linha.strip()
        ]

        resultados = []

        dentro_bloco = False
        categoria_atual = None

        for linha in linhas:

            # ==========================================
            # INÍCIO DO BLOCO
            # ==========================================

            if linha.startswith("Comparativo dos Indicadores Assistenciais"):
                dentro_bloco = True
                continue

            # ==========================================
            # FIM DO BLOCO
            # ==========================================

            if dentro_bloco and linha.startswith("FONTE:"):
                break

            if not dentro_bloco:
                continue

            # ==========================================
            # IDENTIFICA CATEGORIA
            # ==========================================

            if linha in self.CATEGORIAS:
                categoria_atual = linha
                continue

            if categoria_atual is None:
                continue

            # ==========================================
            # IDENTIFICA INDICADOR
            # ==========================================

            indicador_encontrado = None

            for indicador in self.INDICADORES:

                if linha.startswith(indicador):
                    indicador_encontrado = indicador
                    break

            if indicador_encontrado is None:
                continue

            # ==========================================
            # REMOVE TEXTO DO INDICADOR
            # ==========================================

            restante = linha[len(indicador_encontrado):].strip()

            # ==========================================
            # EXTRAI VALORES
            # ==========================================

            valores = re.findall(
                r"-?\d[\d.]*,\d+%?|-?\d+%?",
                restante
            )

            if len(valores) < 5:
                continue

            resultados.append({
                "categoria": categoria_atual,
                "indicador": indicador_encontrado,
                "valor_unimed": valores[0],
                "valor_regiao": valores[1],
                "valor_media_porte": valores[2],
                "valor_media_nacional": valores[3],
                "variacao": valores[4]
            })

        return resultados