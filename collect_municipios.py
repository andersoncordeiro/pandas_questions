import pandas as pd
import numpy as np
import unicodedata


URL = 'https://raw.githubusercontent.com/andersoncordeiro/datasets/main/arq_municipios_fronteiricos.csv'


def converte_object_decimais(valor):
    return int(valor.replace(" ", "").replace(".",""))

def remove_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def normaliza_coluna(coluna):
    nova_coluna = coluna.replace(' (R$)', '').replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').lower()
    nova_coluna = remove_acentos(nova_coluna)
    return nova_coluna

def get_nome_municipio(texto):
    return texto.replace('–', '-').split('-')[-1].strip()


df_original                        = pd.read_csv(URL, thousands=".", decimal=",")
df_original['PIB (IBGE/2005']      = df_original['PIB (IBGE/2005'].apply(converte_object_decimais)
df_original['PIB per capita (R$)'] = df_original['PIB per capita (R$)'].apply(converte_object_decimais)
df_original['IDH/2000']            = df_original['IDH/2000'].replace('ni', '0.621')
# FONTE: CLAUDIO PCICKASFIDKJSDAFIS

df_original['IDH/2000'] = df_original['IDH/2000'].str.replace(',','.').astype(float)
novas_colunas           = [normaliza_coluna(column) for column in df_original.columns]
df_original.columns     = novas_colunas

df_original['nome_municipio'] = df_original['municipio'].apply(get_nome_municipio)

df_original = df_original[[
    'nome_municipio', 'estado', 'area_territorial', 'populacao_ibge_2007',
    'densidade_demografica_hab_km2', 'pib_ibge_2005', 'pib_per_capita', 'idh_2000'
]]

df_original.to_csv('municipios_cleaned.csv')