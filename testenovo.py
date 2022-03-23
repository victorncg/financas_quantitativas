import yfinance as yf
import pandas as pd
import numpy as np

ativos = ['PETR4.SA','VALE3.SA', 'WEGE3.SA', 
          'RADL3.SA', 'OIBR3.SA','KNRI11.SA','FLMA11.SA','BOVA11.SA',
          'SMAL11.SA','AAPL34.SA','IVVB11.SA','ETH-USD','USDBRL=X']

inicio = '2020-05-01'
fim = '2021-10-11'

weg = yf.download('WEGE3.SA', start = inicio, end = fim)

precos = pd.DataFrame()

for i in ativos:
  precos[i] = yf.download(i, start = inicio, end = fim)['Adj Close']

precos['ETH-BRL'] = precos['ETH-USD']*precos['USDBRL=X']

precos = precos.drop(columns = ['ETH-USD', 'USDBRL=X'])

compras = {'PETR4.SA': 1000, 'VALE3.SA': 700, 'WEGE3.SA': 1500, 
           'RADL3.SA': 700, 'OIBR3.SA': 200, 'KNRI11.SA': 700, 'FLMA11.SA': 700, 'BOVA11.SA':1500,
           'SMAL11.SA': 1500, 'AAPL34.SA': 2000, 'IVVB11.SA': 1500, 
           'ETH-BRL': 200}
           
compras_df = pd.Series(data=compras, index=list(compras.keys()))

primeiros = precos.iloc[0]

qtd_acoes = compras_df/primeiros

PL = precos*qtd_acoes

PL['PL Total'] = PL.iloc[:].sum(axis = 1)

PL['PL Total'].plot();
