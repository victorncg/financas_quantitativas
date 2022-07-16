# Este script conterá todas as funções responsáveis pela criação e plotagem dos gráficos


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def razao_preco_media(stock, start, mm):
    
    #import yfinance as yf
    #import pandas as pd

    data = yf.download(stock, start = start)

    data['media'] = data.Close.rolling(mm).mean()
    

    #weg['ret_dia'] = weg.Close.pct_change().rolling(30).mean()

    #weg['vol'] = weg.Close.pct_change().rolling(30).std()

    #weg['razao_ret_vol'] = weg['ret_dia']/weg['vol']

    data['razao'] = data['Close']/data['media']

    return data['razao']



# GRÁFICO 02

def plota_razao_preco_media(stock, start, mm):

    #import yfinance as yf
    #import pandas as pd

    data = yf.download(stock, start = start, progress= False)

    data['media'] = data.Close.rolling(mm).mean()


    #weg['ret_dia'] = weg.Close.pct_change().rolling(30).mean()

    #weg['vol'] = weg.Close.pct_change().rolling(30).std()

    #weg['razao_ret_vol'] = weg['ret_dia']/weg['vol']

    data['razao'] = data['Close']/data['media']

    return data['razao'].plot();


# GRÁFICO 03
# Contém a média da razão calculada

def plota_razao_preco_media_marcado(stock, start, mm):

    #import yfinance as yf
    #import pandas as pd

    data = yf.download(stock, start = start, progress= False)

    data['media'] = data.Close.rolling(mm).mean()


    #weg['ret_dia'] = weg.Close.pct_change().rolling(30).mean()

    #weg['vol'] = weg.Close.pct_change().rolling(30).std()

    #weg['razao_ret_vol'] = weg['ret_dia']/weg['vol']

    data['razao'] = data['Close']/data['media']


    vol = data['razao']
    y = vol
    x = pd.to_datetime(vol.index)
    fig, ax = plt.subplots(figsize=(15,6))
    ax.plot(x,y)
    plt.axhline(y=np.mean(y), color='r', linestyle='-')

    plt.title(f'Razão Preço/Média de Preço nos últimos 30 dias')

    plt.show()