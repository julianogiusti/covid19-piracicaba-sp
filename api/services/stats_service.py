import os
import subprocess
from datetime import datetime

import pandas as pd


def list_stats():
    covid_data_csv = 'https://raw.githubusercontent.com/julianogiusti/covid19-piracicaba-sp/master/covid19_piracicaba_sp.csv'

    covid_data = pd.read_csv(covid_data_csv, sep=';')
    covid_data['data'] = pd.to_datetime(covid_data['data'])

    covid_data['data'] = covid_data['data'].dt.strftime("%d/%m/%Y")

    media_movel = 7
    covid_data['media_movel_casos'] = covid_data['casos_novos'].rolling(window=media_movel).mean()
    covid_data['media_movel_obitos'] = covid_data['obitos_novos'].rolling(window=media_movel).mean()

    covid_data['media_movel_casos'].fillna(0, inplace=True)
    daily_cases = covid_data[['data', 'casos_novos', 'media_movel_casos']].to_numpy().tolist()
    daily_cases.insert(0, ['Data', 'Casos', f'Média nos últimos {media_movel} dias'])

    covid_data['media_movel_obitos'].fillna(0, inplace=True)
    daily_deaths = covid_data[['data', 'obitos_novos', 'media_movel_obitos']].to_numpy().tolist()
    daily_deaths.insert(0, ['Data', 'Óbitos', f'Média nos últimos {media_movel} dias'])

    covid_data[['dia', 'mes', 'ano']] = covid_data['data'].str.split('/', expand=True)
    covid_data['ano_mes'] = covid_data['ano'] + "-" + covid_data['mes']
    monthly_cases = covid_data.groupby(by='ano_mes').sum()['casos_novos']
    monthly_cases.sort_index()
    monthly_cases = monthly_cases.reset_index()
    monthly_cases = monthly_cases.to_numpy().tolist()
    monthly_cases.insert(0, ['Ano-mês', 'Casos'])

    covid_data[['dia', 'mes', 'ano']] = covid_data['data'].str.split('/', expand=True)
    covid_data['ano_mes'] = covid_data['ano'] + "-" + covid_data['mes']
    monthly_deaths = covid_data.groupby(by='ano_mes').sum()['obitos_novos']
    monthly_deaths.sort_index()
    monthly_deaths = monthly_deaths.reset_index()
    monthly_deaths = monthly_deaths.to_numpy().tolist()
    monthly_deaths.insert(0, ['Ano-mês', 'Óbitos'])

    stats = {
        'dia': covid_data["data"].iloc[-1],
        'casos_24h': covid_data["casos_novos"].iloc[-1],
        'casos_total': covid_data["casos"].iloc[-1],
        'obitos_24h': covid_data["obitos_novos"].iloc[-1],
        'obitos_total': covid_data["obitos"].iloc[-1],
        'tratamento_total': int(covid_data["em_tratamento"].iloc[-1]),
        'suspeitos_total': int(covid_data["suspeitos"].iloc[-1]),
        'recuperados_total': int(covid_data["recuperados"].iloc[-1]),
        'descartados_total': int(covid_data["descartados"].iloc[-1]),
        'ocupacao_uti': int(covid_data["ocupacao_uti_%"].iloc[-1]),
        'ocupacao_enfermaria': int(covid_data["ocupacao_enfermaria_%"].iloc[-1]),
        'grafico_casos_diarios': daily_cases,
        'grafico_obitos_diarios': daily_deaths,
        'grafico_casos_mensal': monthly_cases,
        'grafico_obitos_mensal': monthly_deaths,
        'ultima_atualizacao': covid_data["fonte"].iloc[-1]
    }

    return stats
