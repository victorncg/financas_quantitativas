#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/victorncg/financas_quantitativas/blob/main/20210504_Live_Fronteira_Eficiente.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Importando bibliotecas

# In[ ]:


import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Selecionar ativos da carteira


# In[ ]:


ativos = ['ABEV3.SA', 'EQTL3.SA', 'LREN3.SA', 'CIEL3.SA', 'RADL3.SA', 'RENT3.SA', 'MDIA3.SA', 'WEGE3.SA', 'EZTC3.SA', 'FLRY3.SA']


# In[ ]:


# Criar um dataframe que vai conter as cotações diárias dessas ações


# In[ ]:


df = pd.DataFrame()

for t in ativos:
  df[t] = wb.DataReader(t, data_source = 'yahoo', start = '2014-01-01', end = '2021-05-03')['Adj Close']


# In[ ]:


# Visualizando os preços


# In[ ]:


df.plot(figsize = (10,10))


# In[ ]:


df.head()


# In[ ]:


# Calculando retorno diário dos papéis


# In[ ]:


retorno_diario = df.pct_change()


# In[ ]:


retorno_diario.head()


# In[ ]:


retorno_diario = retorno_diario.iloc[1:]


# In[ ]:


retorno_diario.head()


# In[ ]:


retorno_anual = retorno_diario.mean()*250


# In[ ]:


cov_diario = retorno_diario.cov()


# In[ ]:


cov_diario


# In[ ]:


cov_anual = cov_diario*250


# # Iniciando Simulação de Monte Carlo

# In[ ]:


# Aqui vamos criar 200 mil portfólios fictícios com esses papéis


# In[ ]:


port_returns = []

port_volatility = []

stock_weights = []


# In[ ]:


# Vamos passar os parâmetros de simulação


# In[ ]:


num_assets = len(ativos)

num_portfolios = 200000


# In[ ]:


# Vamos usar a função random para criar 10 pesos aleatórios


# In[ ]:


peso = np.random.random(num_assets)


# In[ ]:


peso /= np.sum(peso)


# In[ ]:


peso


# In[ ]:


np.sum(peso)


# In[ ]:


for single_portfolio in range(num_portfolios):
  weights = np.random.random(num_assets)
  weights /= np.sum(weights)
  returns = np.dot(weights, retorno_anual)
  volatility = np.sqrt(np.dot(weights.T, np.dot(cov_anual, weights)))
  port_returns.append(returns)
  port_volatility.append(volatility)
  stock_weights.append(weights)


# In[ ]:


portfolio = {'Retornos': port_returns, 'Volatilidade': port_volatility}


# In[ ]:


for counter,symbol in enumerate(ativos):
  portfolio[symbol+' peso'] = [weight[counter] for weight in stock_weights]

df = pd.DataFrame(portfolio)


# In[ ]:


df.head()


# In[ ]:


retornos = df.sort_values(by = ['Retornos'], ascending = False)


# In[ ]:


retornos.head()


# In[ ]:


plt.style.use('seaborn')

df.plot.scatter(x = 'Volatilidade', y = 'Retornos', figsize = (10,10), grid = True)

plt.xlabel('Volatilidade')

plt.ylabel('Retornos Esperados')

plt.title('Fronteira Eficiente')

plt.show()


# In[ ]:


retorno_max = retornos.iloc[:1]


# In[ ]:


retorno_max = retorno_max.drop(['Retornos', 'Volatilidade'], axis = 1)


# In[ ]:


retorno_max


# In[ ]:


ativos


# In[ ]:


pesos = np.array(retorno_max)


# In[ ]:


pesos


# In[ ]:


retorno_carteira = retorno_diario*pesos


# In[ ]:


retorno_carteira = retorno_carteira.sum(axis = 1)


# In[ ]:


retorno_carteira.plot()


# In[ ]:


# Retorno acumulado


# In[ ]:


returns_acm = (1 + retorno_carteira).cumprod()


# In[ ]:


returns_acm.plot()


# In[ ]:


# Importando dados do IBOV para Benchmark


# In[ ]:


ibov = wb.DataReader('^BVSP', data_source = 'yahoo', start = '2014-01-01', end = '2021-05-03')['Adj Close']


# In[ ]:


type(ibov)


# In[ ]:


ibov_retornos = ibov.pct_change()


# In[ ]:


ibov_retornos_acm = (1 + ibov_retornos).cumprod()


# In[ ]:


pd.DataFrame(ibov_retornos_acm)


# In[ ]:


novo_df = pd.merge(pd.DataFrame(ibov_retornos_acm), pd.DataFrame(returns_acm, columns = ['Minha Carteira']), how = 'inner', on = 'Date')


# In[ ]:


novo_df.rename(columns = {'Adj Close': 'IBOV'}, inplace = True)


# In[ ]:


novo_df.head()


# In[ ]:


novo_df.plot()


# In[ ]:




