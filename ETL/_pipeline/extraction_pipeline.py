import logging

# EXTRACTORS
from _extractors.charts import ChartsExtractor
from _extractors.events import EventsExtractor
from _extractors.expenses import ExpensesExtractor
from _extractors.header import HeaderExtractor
from _extractors.hospitalizations import HospitalizationsExtractor
from _extractors.indicators import IndicatorsExtractor
from _extractors.ticket_cost import TicketCostExtractor

# TRANSFORMERS
from _transformers.charts import ChartsTransformer
from _transformers.events import EventsTransformer
from _transformers.expenses import ExpensesTransformer
from _transformers.hospitalizations import HospitalizationsTransformer
from _transformers.indicators import IndicatorsTransformer
from _transformers.ticket_cost import TicketCostTransformer


logger = logging.getLogger(__name__)


class ExtractionPipeline:

    def __init__(self, reader):
        self.reader = reader

        self.header_extractor = HeaderExtractor()
        self.events_extractor = EventsExtractor()
        self.charts_extractor = ChartsExtractor()
        self.expenses_extractor = ExpensesExtractor()
        self.indicators_extractor = IndicatorsExtractor()
        self.hospitalizations_extractor = HospitalizationsExtractor()
        self.ticket_cost_extractor = TicketCostExtractor()

        self.events_transformer = EventsTransformer()
        self.charts_transformer = ChartsTransformer()
        self.expenses_transformer = ExpensesTransformer()
        self.indicators_transformer = IndicatorsTransformer()
        self.hospitalizations_transformer = HospitalizationsTransformer()
        self.ticket_cost_transformer = TicketCostTransformer()

    def extract_all(self, paginas):

        logger.info(
            "Pipeline de extração iniciado | blocos_unimed=%d",
            len(paginas)
        )

        dados_cadastrais = []
        eventos_despesas = []
        indicadores_assistenciais = []
        internacoes = []
        despesas_assistenciais = []
        indicadores_graficos = []

        for indice, pagina in enumerate(paginas, start=1):

            logger.info(
                "Processando bloco de Unimed | bloco=%d/%d | "
                "pagina_inicial=%d",
                indice,
                len(paginas),
                pagina
            )

            texto = self.reader.get_page_text(pagina)

            header = self.header_extractor.extract(texto)

            logger.info(
                "Unimed identificada | codigo=%s | nome=%s | periodo=%s",
                header["codigo_unimed"],
                header["unimed"],
                header["periodo"]
            )

            dados_eventos = self.events_extractor.extract(texto)
            dados_indicadores = self.indicators_extractor.extract(texto)

            texto_pagina_3 = self.reader.get_page_text(
                pagina + 2
            )

            dados_despesas = self.expenses_extractor.extract(
                texto_pagina_3
            )

            texto_internacoes = self.reader.get_page_region_text(
                page_index=pagina + 2,
                start_text="Número de Internações",
                end_text="Total Internações"
            )

            dados_internacoes = (
                self.hospitalizations_extractor.extract(
                    texto_internacoes
                )
            )

            regioes_graficos = {
                "consultas": self.reader.get_page_region_words(
                    page_index=pagina + 1,
                    start_text="Consultas Médicas Totais",
                    end_text="Exames Médicos"
                ),
                "exames": self.reader.get_page_region_words(
                    page_index=pagina + 1,
                    start_text="Exames Médicos",
                    end_text="Terapias e Outros Atendimentos"
                ),
                "terapias": self.reader.get_page_region_words(
                    page_index=pagina + 1,
                    start_text="Terapias e Outros Atendimentos"
                )
            }

            dados_graficos = self.charts_extractor.extract(
                regioes_graficos
            )

            regiao_tiquete_custo = self.reader.get_page_region_words(
                page_index=pagina + 2,
                start_text="Tíquete Médio e Custo Per Capita",
                end_text="Comparativo Despesas Assistenciais"
            )

            dados_tiquete_custo = self.ticket_cost_extractor.extract(
                regiao_tiquete_custo
            )

            dados_cadastrais.append(header)

            eventos_despesas.extend(
                self.events_transformer.transform(
                    dados_eventos,
                    header
                )
            )

            indicadores_assistenciais.extend(
                self.indicators_transformer.transform(
                    dados_indicadores,
                    header
                )
            )

            internacoes.extend(
                self.hospitalizations_transformer.transform(
                    dados_internacoes,
                    header
                )
            )

            despesas_assistenciais.extend(
                self.expenses_transformer.transform(
                    dados_despesas,
                    header
                )
            )

            indicadores_graficos.extend(
                self.charts_transformer.transform(
                    dados_graficos,
                    header
                )
            )

            indicadores_graficos.extend(
                self.ticket_cost_transformer.transform(
                    dados_tiquete_custo,
                    header
                )
            )

            logger.info(
                "Bloco de Unimed concluído | codigo=%s | "
                "pagina_inicial=%d",
                header["codigo_unimed"],
                pagina
            )

        resultado = {
            "dados_cadastrais": dados_cadastrais,
            "eventos_despesas": eventos_despesas,
            "indicadores_assistenciais": indicadores_assistenciais,
            "internacoes": internacoes,
            "despesas_assistenciais": despesas_assistenciais,
            "indicadores_graficos": indicadores_graficos
        }

        logger.info(
            "Pipeline de extração concluído | blocos_processados=%d | "
            "total_registros=%d",
            len(dados_cadastrais),
            sum(len(registros) for registros in resultado.values())
        )

        return resultado
