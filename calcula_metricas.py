import yfinance as yf
import pandas as pd


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


def plota_razao_preco_media(stock, start, mm):

    #import yfinance as yf
    #import pandas as pd

    data = yf.download(stock, start = start)

    data['media'] = data.Close.rolling(mm).mean()


    #weg['ret_dia'] = weg.Close.pct_change().rolling(30).mean()

    #weg['vol'] = weg.Close.pct_change().rolling(30).std()

    #weg['razao_ret_vol'] = weg['ret_dia']/weg['vol']

    data['razao'] = data['Close']/data['media']

    return data['razao']