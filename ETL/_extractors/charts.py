import re


class ChartsExtractor:

    ENTIDADES = (
        "UNIMED",
        "PORTE_REGIAO",
        "PORTE_NACIONAL",
        "MEDIA_NACIONAL_GERAL"
    )

    CONFIGURACOES = {
        "consultas": {
            "cd_grafico": "CONSULTAS_POR_MIL_BENEFICIARIOS",
            "indicadores": (
                "CONSULTAS_MEDICAS_AMB_PS",
                "CONSULTAS_AMBULATORIAIS",
                "CONSULTAS_PRONTO_SOCORRO"
            ),
            "centros_x": (
                0.116, 0.164, 0.212,
                0.331, 0.379, 0.427,
                0.546, 0.594, 0.642,
                0.761, 0.809, 0.857
            ),
            "ordem": "entidade_indicador"
        },
        "exames": {
            "cd_grafico": "EXAMES_POR_MIL_BENEFICIARIOS",
            "indicadores": (
                "RESSONANCIA_MAGNETICA",
                "TOMOGRAFIA_COMPUTADORIZADA",
                "HEMOGLOBINA_GLICADA"
            ),
            "centros_x": (
                0.126, 0.178, 0.230, 0.282,
                0.413, 0.465, 0.517, 0.569,
                0.700, 0.752, 0.804, 0.856
            ),
            "ordem": "indicador_entidade"
        },
        "terapias": {
            "cd_grafico": (
                "TERAPIAS_OUTROS_ATENDIMENTOS_"
                "POR_MIL_BENEFICIARIOS"
            ),
            "indicadores": (
                "TERAPIAS",
                "OUTROS_ATENDIMENTOS"
            ),
            "centros_x": (
                0.153, 0.232, 0.311, 0.390,
                0.584, 0.663, 0.742, 0.821
            ),
            "ordem": "indicador_entidade"
        }
    }

    NUMERO = re.compile(r"^\d[\d.]*$")
    TOLERANCIA_X = 0.022

    def extract(self, regioes):

        resultados = []

        for nome_grafico, configuracao in self.CONFIGURACOES.items():

            regiao = regioes[nome_grafico]

            resultados.extend(
                self._extract_grafico(
                    regiao,
                    configuracao
                )
            )

        if len(resultados) != 32:
            raise ValueError(
                "Quantidade inesperada de valores nos gráficos: "
                f"esperado 32, encontrado {len(resultados)}"
            )

        return resultados

    def _extract_grafico(self, regiao, configuracao):

        page_width = regiao["page_width"]
        centros = configuracao["centros_x"]
        valores_por_posicao = {}

        for palavra in regiao["words"]:

            texto = palavra["text"]

            if not self.NUMERO.fullmatch(texto):
                continue

            centro_x = (
                palavra["x0"] + palavra["x1"]
            ) / 2 / page_width

            indice = min(
                range(len(centros)),
                key=lambda posicao: abs(
                    centro_x - centros[posicao]
                )
            )

            distancia = abs(centro_x - centros[indice])

            if distancia > self.TOLERANCIA_X:
                continue

            if indice in valores_por_posicao:
                raise ValueError(
                    "Mais de um valor associado à mesma coluna do "
                    f"gráfico {configuracao['cd_grafico']}"
                )

            valores_por_posicao[indice] = texto

        if len(valores_por_posicao) != len(centros):
            faltantes = sorted(
                set(range(len(centros)))
                - set(valores_por_posicao)
            )

            raise ValueError(
                "Não foi possível mapear todas as colunas do gráfico "
                f"{configuracao['cd_grafico']}. "
                f"Posições ausentes: {faltantes}"
            )

        resultados = []

        for indice in range(len(centros)):

            indicador, entidade = self._get_dimensoes(
                indice,
                configuracao
            )

            resultados.append({
                "cd_grafico": configuracao["cd_grafico"],
                "cd_indicador": indicador,
                "tp_entidade": entidade,
                "valor": valores_por_posicao[indice]
            })

        return resultados

    def _get_dimensoes(self, indice, configuracao):

        if configuracao["ordem"] == "entidade_indicador":
            entidade = self.ENTIDADES[
                indice // len(configuracao["indicadores"])
            ]
            indicador = configuracao["indicadores"][
                indice % len(configuracao["indicadores"])
            ]

        else:
            indicador = configuracao["indicadores"][
                indice // len(self.ENTIDADES)
            ]
            entidade = self.ENTIDADES[
                indice % len(self.ENTIDADES)
            ]

        return indicador, entidade
