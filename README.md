## RECA — Automação de Extração de Dados de PDF

Este projeto nasceu de uma demanda real de trabalho na **Unimed**: transformar dados disponibilizados em relatórios PDF em informações estruturadas, confiáveis e prontas para análise.

Até então, parte desse processo dependia da transcrição manual dos dados para planilhas Excel e, posteriormente, de sua utilização em relatórios de Business Intelligence. Além de consumir tempo, esse fluxo aumenta o risco de erros de digitação, inconsistências e retrabalho.

O RECA representa também uma etapa importante do meu desenvolvimento profissional. Foi a primeira vez que precisei extrair dados estruturados de arquivos PDF — um formato criado principalmente para apresentação visual, e não para o consumo automatizado de dados. Ao longo do projeto, venho aprendendo a lidar com diferentes estruturas de página, tabelas, textos posicionados e gráficos, além de organizar uma aplicação de ETL de forma modular e preparada para evoluir.

## Objetivo

Automatizar a leitura, extração, transformação e disponibilização dos dados presentes nos PDFs do RECA, reduzindo o trabalho manual e criando uma base mais segura e escalável para análises.

Os principais objetivos são:

- reduzir a transcrição manual de informações;
- diminuir a possibilidade de erros humanos;
- padronizar os dados extraídos;
- facilitar validações e auditorias;
- acelerar a atualização dos relatórios;
- preparar o processo para integração futura com banco de dados e ferramentas de BI.

## Fluxo atual

Atualmente, o processo segue este fluxo:

```text
PDF do RECA
    ↓
Leitura e extração com Python
    ↓
Transformação e organização dos dados
    ↓
Validação
    ↓
Exportação para Excel
```

O arquivo Excel funciona como a saída estruturada da etapa atual do projeto e pode ser usado para conferência, análise e consumo por outras ferramentas.

## Evolução planejada

A evolução prevista amplia o fluxo para uma arquitetura de dados mais completa:

```text
PDF do RECA
    ↓
ETL em Python
    ↓
Oracle
    ↓
Transformações e modelagem com dbt
    ↓
Power BI
```

Nessa etapa, o Excel deixa de ser o destino principal e os dados passam a ser armazenados no Oracle. O dbt será responsável por parte das transformações e da modelagem analítica, enquanto o Power BI consumirá as estruturas preparadas para visualização e acompanhamento dos indicadores.

## Arquitetura do projeto

O código é organizado por responsabilidade, evitando concentrar toda a lógica em um único arquivo:

```text
ETL/
├── readers/
├── extractors/
├── transformers/
├── pipeline/
├── exporters/
└── utils/
```

### `readers`

Responsável por abrir o PDF, percorrer as páginas e disponibilizar seu conteúdo para as demais etapas.

### `extractors`

Contém as regras de extração de cada grupo de informações. Essa separação permite tratar individualmente os diferentes formatos encontrados no relatório.

### `transformers`

Normaliza e converte os valores extraídos, preparando tipos, textos e estruturas para armazenamento e análise.

### `pipeline`

Orquestra o fluxo de execução, conectando leitura, extração, transformação, validação e exportação.

### `exporters`

Gera as saídas estruturadas. Na versão atual, essa camada é responsável pela exportação para Excel.

### `utils`

Reúne recursos compartilhados, como configuração de caminhos e logging.

## Tecnologias utilizadas

- **Python** para implementar e orquestrar o processo de ETL;
- **pdfplumber** para ler páginas, textos, tabelas e informações de posicionamento no PDF;
- **pandas** para organizar, transformar e validar os dados tabulares;
- **openpyxl** para apoiar a geração dos arquivos Excel;
- **logging** para registrar o andamento da execução, avisos e erros relevantes.

## Extração de gráficos por coordenadas

Um dos maiores desafios do projeto está na extração de informações apresentadas graficamente. Em PDFs, elementos que parecem formar um gráfico para uma pessoa nem sempre existem como uma estrutura lógica pronta para ser lida pelo código. Muitas vezes, são apenas textos e objetos posicionados visualmente na página.

Por isso, parte da extração utiliza as coordenadas dos elementos. A posição horizontal e vertical ajuda a relacionar rótulos, categorias e valores, reconstruindo em formato tabular aquilo que aparece visualmente no relatório.

Essa abordagem exige atenção especial porque pequenas mudanças no layout do PDF podem afetar a interpretação das posições. As regras são, portanto, desenvolvidas e refinadas com base na estrutura observada nos documentos reais.

## Organização dos dados

Os dados extraídos são separados por seus diferentes contextos de negócio, incluindo estruturas relacionadas a:

- dados cadastrais;
- eventos e despesas;
- indicadores assistenciais;
- internações;
- despesas assistenciais;
- indicadores originalmente apresentados em gráficos.

Essas estruturas formam a base para a modelagem das principais tabelas e fatos do processo. A modelagem continuará evoluindo conforme o projeto avançar para o Oracle e para a camada analítica com dbt, sem antecipar definições que ainda dependem da validação do negócio.

## Validação e observabilidade

A validação é essencial porque o processo automatizado precisa produzir resultados tão confiáveis quanto — e, idealmente, mais confiáveis que — a transcrição manual.

Entre os controles considerados no projeto estão:

- conferência da presença das seções esperadas;
- validação de campos obrigatórios;
- verificação de tipos e formatos;
- comparação de quantidades extraídas;
- identificação de páginas sem texto ou de estruturas não reconhecidas;
- registro de avisos e erros para facilitar a investigação.

O projeto utiliza logging para acompanhar as principais etapas da execução. Os registros ajudam a identificar qual arquivo está sendo processado, quantas páginas ou entidades foram encontradas, quais conjuntos de dados foram gerados e em que ponto uma eventual falha ocorreu.

## Idempotência e identificação dos documentos

Uma evolução planejada é criar uma identificação única para cada documento processado, associada a um hash do arquivo. Essa estratégia deverá permitir:

- reconhecer PDFs já processados;
- evitar cargas duplicadas;
- rastrear a origem de cada registro;
- reprocessar documentos de maneira controlada;
- tornar as cargas futuras no Oracle idempotentes.

Essa funcionalidade ainda faz parte do planejamento e será definida em conjunto com a estratégia de persistência dos dados.

## Próximos passos

- ampliar e consolidar as regras de validação;
- melhorar o tratamento de exceções e os registros de execução;
- aumentar a cobertura dos diferentes cenários encontrados nos PDFs;
- criar testes para extração e transformação;
- implementar a identificação dos documentos por hash;
- garantir idempotência no processamento e nas cargas;
- substituir a saída principal em Excel pela persistência no Oracle;
- modelar os dados analíticos com dbt;
- disponibilizar os dados tratados no Power BI;
- documentar a instalação e a execução conforme o ambiente do projeto for consolidado.

## Aprendizados

Mais do que automatizar uma tarefa, este projeto tem sido uma oportunidade de aprender, na prática, sobre extração de dados semiestruturados, organização de pipelines, separação de responsabilidades, validação, observabilidade e modelagem de dados.

O desenvolvimento é incremental: primeiro, tornar a extração funcional; depois, melhorar a organização e a confiabilidade; por fim, evoluir para uma solução integrada ao ambiente de dados. Cada etapa aproxima o processo de uma rotina menos manual, mais rastreável e mais útil para o negócio.

## Status do projeto

O projeto está em desenvolvimento. O fluxo atual realiza a extração dos PDFs com Python e gera uma saída estruturada em Excel. As integrações com Oracle, dbt e Power BI, assim como os mecanismos de hash e idempotência, representam a evolução planejada da solução.
