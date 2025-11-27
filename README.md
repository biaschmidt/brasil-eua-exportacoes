# Exportações do Brasil para os Estados Unidos — Análise via API do ComexStat

Este repositório apresenta uma análise dos produtos mais exportados pelo Brasil para os Estados Unidos, utilizando dados obtidos diretamente da **API oficial do ComexStat**. O objetivo é demonstrar, de forma clara e aplicada, como acessar dados públicos de comércio exterior, tratá-los em Python e extrair insights relevantes sobre a pauta exportadora brasileira.

## Objetivo

Explorar a evolução das exportações brasileiras para os EUA por capítulo do Sistema Harmonizado (HS2), identificando os produtos mais relevantes ao longo do tempo e destacando mudanças estruturais na composição da pauta exportadora.

## Como os dados são obtidos

Os dados são baixados diretamente da API pública do ComexStat.  
O script `fetch_comex_br_us.py` realiza automaticamente:

1. Consulta ao endpoint de filtros para identificar o código correto dos Estados Unidos na API.  
2. Envio de requisição à API para obter valores FOB de exportações do Brasil → EUA, agregados por capítulo (HS2) e ano.  
3. Normalização da resposta em um DataFrame.  
4. Salvamento do dataset em CSV para análise posterior.

O uso da API garante dados atualizados, consistentes com a base oficial do governo brasileiro.

## Arquivos do repositório

- `fetch_comex_br_us.py` – Script em Python que consulta a API, trata os dados e gera o arquivo CSV.  
- `export_br_us_by_chapter.csv` – Arquivo gerado automaticamente com exportações agregadas por capítulo HS2 e ano.  
- `notebooks/analise.ipynb` – Notebook contendo a análise exploratória, gráficos e interpretação econômica dos resultados.

## Principais resultados

A análise dos dados evidencia que a pauta exportadora brasileira para os EUA apresenta maior participação de **produtos industriais**, incluindo máquinas, veículos, equipamentos elétricos e derivados de petróleo.  
Ao longo do período observado, nota-se:

- crescimento consistente de bens de maior intensidade tecnológica,  
- manutenção da relevância dos óleos combustíveis,  
- presença de produtos de maior valor agregado em comparação a outros parceiros comerciais do Brasil.

Esses padrões refletem características estruturais da relação comercial Brasil–EUA e ajudam a entender o papel dos EUA como destino relevante de bens industriais brasileiros.
