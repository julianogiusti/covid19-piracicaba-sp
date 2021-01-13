import os
import subprocess
from datetime import datetime

import pandas as pd


def list_stats():
    # downalod data
    covid_url = 'https://www.dropbox.com/s/tp52yb4oda456ub/Historico_covid19_Piracicaba_SP.xlsx?dl=0'
    covid_data_sheet = 'covid19_piracicaba_sp.xlsx'

    # check if there is need to download
    if not os.path.exists(covid_data_sheet):
        subprocess.call(f'wget -c {covid_url} -O {covid_data_sheet}', shell=True)
        covid_data = pd.read_excel(covid_data_sheet)
    else:
        covid_data = pd.read_excel(covid_data_sheet)
        last_update = covid_data['data'].iloc[-1]
        today = datetime.now()
        if today.hour >= 18 and today.date() > last_update.date():
            subprocess.call(f'wget -c {covid_url} -O {covid_data_sheet}', shell=True)
            covid_data = pd.read_excel(covid_data_sheet)

    covid_data['data'] = covid_data['data'].dt.strftime("%d/%m/%Y")

    media_movel = 7
    covid_data['media_movel_casos'] = covid_data['casos_novos'].rolling(window=media_movel).mean()
    covid_data['media_movel_obitos'] = covid_data['obitos_novos'].rolling(window=media_movel).mean()

    sample = [
          ['Month', 'Bolivia', 'Ecuador', 'Madagascar', 'Papua New Guinea', 'Rwanda', 'Average'],
          ['2004/05',  165,      938,         522,             998,           450,      614.6],
          ['2005/06',  135,      1120,        599,             1268,          288,      682],
          ['2006/07',  157,      1167,        587,             807,           397,      623],
          ['2007/08',  139,      1110,        615,             968,           215,      609.4],
          ['2008/09',  136,      691,         629,             1026,          366,      569.6]
        ]

    covid_data['media_movel_casos'].fillna(0, inplace=True)
    daily_cases = covid_data[['data', 'casos_novos', 'media_movel_casos']].to_numpy().tolist()
    daily_cases.insert(0, ['Data', 'Casos', f'Média nos últimos {media_movel} dias'])

    covid_data['media_movel_obitos'].fillna(0, inplace=True)
    daily_deaths = covid_data[['data', 'obitos_novos', 'media_movel_obitos']].to_numpy().tolist()
    daily_deaths.insert(0, ['Data', 'Óbitos', f'Média nos últimos {media_movel} dias'])

    stats = {
        'dia': covid_data["data"].iloc[-1],
        'casos_24h': covid_data["casos_novos"].iloc[-1],
        'casos_total': covid_data["casos"].iloc[-1],
        'obitos_24h': covid_data["obitos_novos"].iloc[-1],
        'obitos_total': covid_data["obitos"].iloc[-1],
        'tratamento_total': covid_data["em_tratamento"].iloc[-1].astype('int'),
        'suspeitos_total': covid_data["suspeitos"].iloc[-1].astype('int'),
        'recuperados_total': covid_data["recuperados"].iloc[-1].astype('int'),
        'descartados_total': covid_data["descartados"].iloc[-1].astype('int'),
        'grafico_casos_diarios': daily_cases,
        'grafico_obitos_diarios': daily_deaths
    }

    return stats
