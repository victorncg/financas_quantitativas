# Importando bibliotecas

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import seaborn as sns

ativos = ['ABEV3.SA', 'EQTL3.SA', 'LREN3.SA', 'CIEL3.SA', 'RADL3.SA', 'RENT3.SA', 'MDIA3.SA', 'WEGE3.SA', 'EZTC3.SA', 'FLRY3.SA']

df = pd.DataFrame()

for t in ativos:
  df[t] = wb.DataReader(t, data_source = 'yahoo', start = '2014-01-01', end = '2022-02-03')['Adj Close']


retorno_diario = df.pct_change()

retorno_diario = retorno_diario.iloc[1:]


retorno_anual = retorno_diario.mean()*250

cov_diario = retorno_diario.cov()

cov_anual = cov_diario*250

port_returns = []

port_volatility = []

stock_weights = []

num_assets = len(ativos)

num_portfolios = 200000

peso = np.random.random(num_assets)

peso /= np.sum(peso)

for single_portfolio in range(num_portfolios):
  weights = np.random.random(num_assets)
  weights /= np.sum(weights)
  returns = np.dot(weights, retorno_anual)
  volatility = np.sqrt(np.dot(weights.T, np.dot(cov_anual, weights)))
  port_returns.append(returns)
  port_volatility.append(volatility)
  stock_weights.append(weights)


portfolio = {'Retornos': port_returns, 'Volatilidade': port_volatility}

for counter,symbol in enumerate(ativos):
  portfolio[symbol+' peso'] = [weight[counter] for weight in stock_weights]

df = pd.DataFrame(portfolio)

retornos = df.sort_values(by = ['Retornos'], ascending = False)


retorno_max = retornos.iloc[:1]

retorno_max = retorno_max.drop(['Retornos', 'Volatilidade'], axis = 1)

pesos = np.array(retorno_max)

retorno_carteira = retorno_diario*pesos

retorno_carteira = retorno_carteira.sum(axis = 1)

returns_acm = (1 + retorno_carteira).cumprod()

ibov = wb.DataReader('^BVSP', data_source = 'yahoo', start = '2014-01-01', end = '2021-05-03')['Adj Close']

ibov_retornos = ibov.pct_change()

ibov_retornos_acm = (1 + ibov_retornos).cumprod()

novo_df = pd.merge(pd.DataFrame(ibov_retornos_acm), pd.DataFrame(returns_acm, columns = ['Minha Carteira']), how = 'inner', on = 'Date')

novo_df.rename(columns = {'Adj Close': 'IBOV'}, inplace = True)

#novo_df.plot()

novo_df['Date'] = novo_df.index

novo_df.plot(x = 'Date', y = ['IBOV', 'Minha Carteira'], kind = 'line', figsize= (10,10))

plt.text(0.8, 1, 'Trading com Dados', transform=ax.transAxes,
        fontsize=60, color='gray', alpha=0.2,
        ha='center', va='center', rotation='30')

plt.show()



