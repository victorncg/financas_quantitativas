# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 09:28:39 2021

@author: USUARIO
"""

import pandas as pd
import numpy as np
import pandas_datareader as wb
import matplotlib.pyplot as plt
import seaborn as sns
import quandl 

with open('senha.txt') as f:
    read__data = f.read()

f = open("senha.txt","r")

token = f.read()


token

quandl.ApiConfig.api_key = token

# 3. Indicadores Macroeconômicos
# Inicialmente vamos verificar indicadores macroeconômicos que revelam o estado da economia no período. Ainda não vamos falar de indicadores que são usados como taxas de referência para investimentos

# 3.1. Endividamento do setor público brasileiro
# 4468 para governo federal
# 4478 para todo o setor público

endividamento = quandl.get("BCB/4478", trim_start = "2010-01-01", trim_end = "2019-12-31")
plt.figure(figsize=(9,7))
plt.plot(endividamento)

endividamento.rename(columns={"Value": "endividamento"}, inplace = True)
endividamento.head()



# 3.2. Taxa de desocupação da PNADC

pnadc = quandl.get("BCB/24369", trim_start = "2010-01-01", trim_end = "2019-12-31")
plt.figure(figsize=(9,7))
plt.plot(pnadc)

pnadc.rename(columns={"Value": "pnadc"}, inplace = True)
pnadc.head()


# 3.3. IGP-M

igpm = quandl.get("BCB/189", trim_start = "2010-01-01", trim_end = "2019-12-31")
plt.figure(figsize=(9,7))
plt.plot(igpm)

igpm.rename(columns={"Value": "igpm"}, inplace = True)
igpm.head()


# 3.4. Custo da cesta básica

CBAS = quandl.get("BCB/7493", trim_start = "2010-01-01", trim_end = "2019-12-31")
plt.figure(figsize=(9,7))
plt.plot(CBAS)

CBAS.rename(columns={"Value": "CBAS"}, inplace = True)
CBAS.head()


# 4. Indicadores de referência para investimentos
Continuando a análise de indicadores macroeconômicos, vamos agora retornar indicadores que são usados como referência para produtos de investimentos

# 4.1. Taxa Selic

selic = quandl.get("BCB/432", start_date="2010-01-01",end_date="2019-12-31")
plt.plot(selic)
plt.show()

selic.rename(columns={"Value": "Selic"}, inplace = True)
selic.head()

# Uma outra forma de obter o mesmo gráfico é com o código abaixo
selic.plot(figsize=(14, 4))

# 4.2. IPCA
ipca = quandl.get("BCB/13522", start_date="2010-01-01",end_date="2019-12-31")
plt.plot(ipca)
plt.show()

ipca.rename(columns={"Value": "IPCA"}, inplace = True)
ipca.head()

# 4.3. Dólar

dolar = quandl.get("BCB/10813", start_date="2010-01-01",end_date="2019-05-31")
plt.figure(figsize=(9,7))
plt.plot(dolar)

dolar.rename(columns={"Value": "dolar"}, inplace = True)
dolar.head()

# 4.4. Ouro
ourobr = quandl.get("BCB/4", start_date="2010-01-01",end_date="2019-12-31")
plt.figure(figsize=(9,7))
plt.plot(ourobr)

ourobr.rename(columns={"Value": "Ouro"}, inplace = True)
ourobr.head()



5. Gráficos
# Gráfico do Dolar e Ouro

fig, ax1 = plt.subplots(figsize=(9,7))

color = 'tab:red'
ax1.set_xlabel('Data')
ax1.set_ylabel('Dólar', color=color)
ax1.plot(dolar, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx() # Configurar um outro eixo vertical que compartilha o mesmo eixo X

color = 'tab:blue'
ax2.set_ylabel('Ouro', color=color) 
ax2.plot(ourobr, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.show()


#Vamos agora criar um data frame com todos esses indicadores

from functools import reduce

# Usar esse data frame na primeira análise, com todos os indicadores
data_frames = [endividamento, pnadc, igpm, CBAS, selic, ipca, dolar, ourobr]
​
# Num segundo momento, usar esse com apenas alguns para ficar mais fácil a visualização

data_frames = [CBAS, selic, ipca, dolar, ourobr]
​
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='inner'), data_frames)


# correlação de pearson 
sns.heatmap(df_merged.corr(), annot=True)





# 6. Normalizando o preço dos ativos
df_st = df_merged

(df_st / df_st.iloc[0] * 100).plot(figsize=(10, 8))

plt.ylabel('Preços Normalizados')

plt.xlabel('DATE')

plt.figure(figsize=(10,10))

# Caso queira criar um arquivo com o plot do gráfico:
plt.savefig('sample.png')


#mercadode ações


ativos = ['PETR4.SA', 'VALE3.SA','BRDT3.SA', 'CCRO3.SA', 'ECOR3.SA','MRFG3.SA', 'BEEF3.SA', 'RAPT4.SA','^BVSP']


df_ativos = pd.DataFrame()

for i in ativos:
    df_ativos[i] = wb.DataReader(i, data_source='yahoo', start='2018-03-15', end='2019-12-31')['Adj Close']
    
    
#retornos

df_retornos = df_ativos.pct_change()

#retornos acumulado
retorno_acm = (1+df_retornos).cumprod()

plt.figure(figsize=(20,10))
plt.plot(retorno_acm)
plt.legend(loc='lower right')
plt.show()


# Num segundo momento, usar esse com apenas alguns para ficar mais fácil a visualização

data_frames = [dolar, ourobr, df_ativos]
​
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='inner'), data_frames)


# 6. Normalizando o preço dos ativos
df_st = df_merged

(df_st / df_st.iloc[0] * 100).plot(figsize=(10, 8))

plt.ylabel('Preços Normalizados')

plt.xlabel('DATE')

plt.figure(figsize=(15,15))
