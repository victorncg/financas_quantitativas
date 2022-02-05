# Importando bibliotecas

# Rotina para criação da Fronteira Eficiente usando a simulação de Monte Carlo

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

ativos = ['ABEV3.SA', 'EQTL3.SA', 'LREN3.SA', 'CIEL3.SA', 'RADL3.SA', 'RENT3.SA', 'MDIA3.SA', 'WEGE3.SA', 'EZTC3.SA', 'FLRY3.SA']

df = pd.DataFrame()

df= yf.download(ativos, start = '2019-01-01', end = '2022-02-03')['Adj Close']

retorno_diario = df.pct_change()

retorno_diario = retorno_diario.iloc[1:]


retorno_anual = retorno_diario.mean()*250

cov_diario = retorno_diario.cov()

cov_anual = cov_diario*250

port_returns = []

port_volatility = []

stock_weights = []

num_assets = len(ativos)

num_portfolios = 1000

peso = np.random.random(num_assets)

peso /= np.sum(peso)

# Preenchimento das listas com os parâmetros

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

ibov = yf.download('^BVSP', start = '2019-01-01', end = '2022-02-03')

ibov.rename(columns = {'Adj Close': 'IBOV'}, inplace = True)

ibov_retornos_acm = ibov/ibov.iloc[0]

novo_df = pd.merge(pd.DataFrame(ibov_retornos_acm), pd.DataFrame(returns_acm, columns = ['Minha Carteira']), how = 'inner', on = 'Date')

novo_df['Date'] = novo_df.index

novo_df.plot(x = 'Date', y = ['IBOV', 'Minha Carteira'], kind = 'line', figsize= (10,10))

plt.show()



