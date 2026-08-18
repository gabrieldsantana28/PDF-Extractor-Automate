# EXTRACTORS
from ETL._extractors.events import EventsExtractor
from ETL._extractors.expenses import ExpensesExtractor
from ETL._extractors.header import HeaderExtractor
from ETL._extractors.hospitalizations import HospitalizationsExtractor
from ETL._extractors.indicators import IndicatorsExtractor

# TRANSFORMERS
from ETL._transformers.events import EventsTransformer
from ETL._transformers.expenses import ExpensesTransformer
from ETL._transformers.hospitalizations import HospitalizationsTransformer
from ETL._transformers.indicators import IndicatorsTransformer

class ExtractionPipeline:

    def __init__(self, reader):
        self.reader = reader

        self.header_extractor = HeaderExtractor()
        self.events_extractor = EventsExtractor()
        self.expenses_extractor = ExpensesExtractor()
        self.indicators_extractor = IndicatorsExtractor()
        self.hospitalizations_extractor = HospitalizationsExtractor()

        self.events_transformer = EventsTransformer()
        self.expenses_transformer = ExpensesTransformer()
        self.indicators_transformer = IndicatorsTransformer()
        self.hospitalizations_transformer = HospitalizationsTransformer()

    def extract_all(self, paginas):

        dados_cadastrais = []
        eventos_despesas = []
        indicadores_assistenciais = []
        internacoes = []
        despesas_assistenciais = []

        for pagina in paginas:

            texto = self.reader.get_page_text(pagina)

            header = self.header_extractor.extract(texto)

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

        return {
            "dados_cadastrais": dados_cadastrais,
            "eventos_despesas": eventos_despesas,
            "indicadores_assistenciais": indicadores_assistenciais,
            "internacoes": internacoes,
            "despesas_assistenciais": despesas_assistenciais
        }