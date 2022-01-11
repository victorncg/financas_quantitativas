install.packages("BatchGetSymbols")
install.packages("quantmod")
install.packages("GetDFPData")

library(BatchGetSymbols)
library(quantmod)
library(GetDFPData)
library(ggplot2)
library(ggthemes)
library(reshape2)
library(plyr)

# Início do nosso código
# SEÇÃO 01
?BatchGetSymbols

acao = 'MGLU3.SA'

di = '2016-01-01'

df = Sys.Date()

benchmark = '^BVSP'

dados_acao = BatchGetSymbols(
  tickers = acao,
  first.date = di,
  last.date = df,
  bench.ticker = benchmark,
)

dados_acao = dados_acao$df.tickers

p = ggplot(dados_acao, aes(ref.date, price.adjusted)) + geom_line(color = 'blue')

p + labs(x = "Data", y = "Preço Ajustado", title = "Variação do Preço da Ação", subtitle = "De 01/01/2016 a 19/10/2020")

# SEÇÃO 02
# Dados de várias ações de uma vez

ibov = GetIbovStocks()

ibov$tickersSA = paste(ibov$tickers, ".SA", sep = '')

dados_ibov = BatchGetSymbols(
  tickers = ibov$tickersSA,
  first.date = di,
  last.date = df,
  bench.ticker = benchmark,
)


dados_ibov = dados_ibov$df.tickers

dados_ibov2 = dlply(dados_ibov, .(ticker), function(x) {rownames(x) = x$row; x$row = NULL;x})

acao = dados_ibov2[[1]][,c(7,6)]

colnames(acao) = c("Data", paste("Preços",dados_ibov2[[1]][1,8]))

for (i in 2:69) {
  
  novaacao = dados_ibov2[[i]][,c(7,6)]
  
  colnames(novaacao) = c("Data", paste("Preços",dados_ibov2[[i]][1,8]))
  
  acao = merge(acao, novaacao, by = "Data")
  
}

# Gerando gráfico com várias ações
# Ações do setor bancário

f = ggplot() +
  geom_line(data = acao, aes(x = Data , y = acao$`Preços BBAS3.SA` , color = "Banco do Brasil"))+
  geom_line(data = acao, aes(x = Data , y = acao$`Preços BBDC4.SA` , color = "Bradesco"))+
  geom_line(data = acao, aes(x = Data , y = acao$`Preços ITUB4.SA` , color = "Itaú Unibanco"))+
  geom_line(data = acao, aes(x = Data , y = acao$`Preços SANB11.SA` , color = "Santander"))+
  
  xlab("Data")+
  ylab("Preço")

f$labels$colour = "Bancos"

print(f)

# SEÇÃO 03 - Normalizando o preço das ações

# Utilizar índices de referência no mercado financeiro

IBOV = BatchGetSymbols(
  tickers = '^BVSP',
  first.date = di,
  last.date = df,
  bench.ticker = benchmark,
)
  
IBOV = IBOV$df.tickers

colnames(IBOV)[6] = "IBOV"
colnames(IBOV)[7] = "Data"

IBOV = IBOV[,c(7,6)]
SP500 = SP500[,c(7,6)]

SP500 = BatchGetSymbols(
  tickers = '^GSPC',
  first.date = di,
  last.date = df,
  bench.ticker = '^GSPC',
)

SP500 = SP500$df.tickers

colnames(SP500)[6] = "SP500"
colnames(SP500)[7] = "Data"

ibov_sp500 = merge(IBOV, SP500, by = "Data")

total = merge (ibov_sp500, acao, by = "Data")

normalizado = total[,-c(1)]

novo_total = data.frame(lapply(normalizado, function(x) x/x[1]))

novo_total$Data = total$Data

g = ggplot() +
  geom_line(data = novo_total, aes(x = Data , y = novo_total$Preços.EZTC3.SA , color = "EZTEC"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$Preços.MRVE3.SA , color = "MRV"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$Preços.CYRE3.SA , color = "Cyrela"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$IBOV , color = "IBOV"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$SP500 , color = "S&P 500"))+
  
  xlab("Data")+
  ylab("Preço")

g$labels$colour = "Construção"

print(g)


# E se quiséssemos plotar todas as colunas?

df = melt(novo_total, id.vars = 'Data', variable.name = 'series')

ggplot(df, aes(Data, value)) + geom_line(aes(colour = series))

novo_total2 = novo_total[,c(1:4,72)]

df = melt(novo_total2, id.vars = 'Data', variable.name = 'series')

ggplot(df, aes(Data, value)) + geom_line(aes(colour = series))

# Para visualizar em plots separados

ggplot(df, aes(Data, value)) + geom_line() + facet_grid(series ~.)

# SEÇÃO 04 - Calculando correlação e construindo nosso próprio portfólio
library(corrplot)

correlacoes = cor(normalizado, use = "complete.obs", method = 'spearman')
corrplot(correlacoes, number.cex = 0.001, number.font = 5)

tabela01 = normalizado[,c(1,2,15:25)]

correlacoes = cor(tabela01, use = "complete.obs", method = 'spearman')
corrplot(correlacoes, number.cex = 1, number.font = 1, method = "number", type = "lower")


tabela02 = normalizado[,colnames(normalizado) %in% c("Preços MGLU3.SA","Preços WEGE3.SA","Preços ITUB4.SA","Preços MGLU3.SA","Preços ABEV3.SA","Preços B3SA3.SA" )]

correlacoes = cor(tabela02, use = "complete.obs", method = 'spearman')
corrplot(correlacoes, number.cex = 1, number.font = 1, method = "number", type = "lower")


# Construção do portfólio

novo_total$Preços.MGLU3.SA = (novo_total$Preços.MGLU3.SA)*(-1)

novo_total$carteira = 0.2*novo_total$Preços.ABEV3.SA +
  0.15*novo_total$Preços.B3SA3.SA +
  0.15*novo_total$Preços.EZTC3.SA+
  0.3*novo_total$Preços.WEGE3.SA+
  0.2*novo_total$Preços.MGLU3.SA

h = ggplot() +
  geom_line(data = novo_total, aes(x = Data , y = novo_total$carteira , color = "Meu portfólio"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$Preços.WEGE3.SA , color = "Weg"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$Preços.ABEV3.SA , color = "Ambev"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$IBOV , color = "IBOV"))+
  geom_line(data = novo_total, aes(x = Data , y = novo_total$SP500 , color = "S&P 500"))+
  
  xlab("Data")+
  ylab("Preço")

h$labels$colour = "Ativos vs. Portfólio"

print(h)



tabela03 = novo_total[,colnames(novo_total) %in% c("IBOV","Preços.WEGE3.SA","Preços.ITUB4.SA","Preços.MGLU3.SA","Preços.ABEV3.SA","Preços.B3SA3.SA","carteira","SP500" )]

correlacoes = cor(tabela03, use = "complete.obs", method = 'spearman')
corrplot(correlacoes, number.cex = 1, number.font = 1, method = "number", type = "lower")

# SEÇÃO 05 - Utilizando a biblioteca quantmod
library(quantmod)

?getSymbols

dados_apple = getSymbols(Symbols = "AAPL", from = '2020-01-01', src = 'yahoo', auto.assign = FALSE)

chart_Series(dados_apple)

dados_weg = getSymbols(Symbols = "WEGE3.SA", from = '2020-01-01', src = 'yahoo', auto.assign = FALSE)

chart_Series(dados_weg)

ggplot(dados_weg, aes(index(dados_weg), dados_weg[,6])) + geom_line(color = "darkblue") +
  ggtitle("Cotação de Weg desde 01 de Janeiro de 2020")


# Construção das médias móveis
dados_weg_filtrado = subset(dados_weg, index(dados_weg)>= '2020-02-20')

MMWEG_10 = rollmean(dados_weg_filtrado[,6], 10, fill = list(NA, NULL, NA), align = 'right')
MMWEG_30 = rollmean(dados_weg_filtrado[,6], 30, fill = list(NA, NULL, NA), align = 'right')

dados_weg_filtrado$MMWEG_10 = MMWEG_10
dados_weg_filtrado$MMWEG_30 = MMWEG_30


ggplot(dados_weg_filtrado, aes(index(dados_weg_filtrado)))+
  geom_line(aes(y = dados_weg_filtrado[,6], color = "Preço de WEGE3")) +
  geom_line(aes(y = dados_weg_filtrado$MMWEG_10, color = "Média Móvel de 10 Períodos")) +
  geom_line(aes(y = dados_weg_filtrado$MMWEG_30, color = "Média Móvel de 30 Períodos"))+
  xlab("Data") + ylab("Preço")


dailyReturn(dados_weg_filtrado)

weeklyReturn(dados_weg_filtrado)

monthlyReturn(dados_weg_filtrado)

yearlyReturn(dados_weg_filtrado)

sd(na.omit(dados_weg_filtrado$WEGE3.SA.Adjusted))


# SEÇÃO 06 - Trabalhando com dados fundamentalistas
empresas = gdfpd.get.info.companies()

company = "RUMO MALHA PAULISTA S.A."

di = '2019-01-01'
df = '2020-01-01'
type.export = "xlsx"

Dados_Fund_RAIL3 = gdfpd.GetDFPData(name.companies = company,
                 first.date = di,
                 last.date = df)

fluxodecaixa = Dados_Fund_RAIL3[[17]]
fluxodecaixa = data.frame(fluxodecaixa[[1]])
