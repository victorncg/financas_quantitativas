# Instalação das bibliotecas

install.packages("BatchGetSymbols")
install.packages("quantmod")
install.packages("tidyquant")
install.packages("GetDFPData")

# Uma vez instaladas as bibliotecas
library(BatchGetSymbols)
library(quantmod)
library(tidyquant)
library(GetDFPData)
library(GetTDData)
library(Quandl)
library(ggplot2)
library(ggthemes)
library(reshape2)
library(plyr)
library(corrplot)

# =========================================================
# 1. Obtendo dados de ações e visualizando
# =========================================================
# BATCHGETSYMBOLS

?BatchGetSymbols

# Configurar os argumentos que vamos passar na função
acao = 'WEGE3.SA'

di = '2017-01-01'

# Aqui estou colocando a data de hoje
df = Sys.Date()

benchmark = '^BVSP'

dados_acao = BatchGetSymbols(tickers = acao, bench.ticker = benchmark,
                first.date = di, last.date = df)

dados_acao = dados_acao$df.tickers

p = ggplot(dados_acao, aes(ref.date, price.adjusted)) + geom_line(color = "blue")

p + labs(x = "", y = "Preço Ajustado de Fechamento de WEGE3",
         title = "Cotação da WEGE3 desde 2017",
         subtitle = "De 01/01/2017 a 19/10/20")

# ==============================
# SEÇÃO 03
# Vamos recuperar mais de uma ação de uma vez
# Aqui, a ideia é retornar todas as ações que compõem o IBOV

ibov = GetIbovStocks()

# Outra opção é usar o resultado da função GetIbovStocks() da própria
# BatchGetSymbols
# No comando a seguir, criamos uma nova coluna que vai conter o código das
# ações acrescido do texto ".SA", que é o formato padrão de busca no Yahoo Finance

ibov$tickersSA = paste(ibov$tickers,".SA", sep = "")

dados_ibov = BatchGetSymbols(tickers = ibov$tickersSA, bench.ticker = benchmark,
                      first.date = di, last.date = df)

dados_ibov2 = dados_ibov$df.tickers

# Aqui vamos realizar uma transformação para mudar o formato de dados
# Ao invés de um único data frame, vamos criar uma lista
# com todos os data frames de ações do Ibov dentro dela

dados_ibov3 = dlply(dados_ibov2, .(ticker), 
                    function(x) {rownames(x) = x$row; x$row = NULL;x})

# Queremos chegar num data frame onde cada linha é uma data
# e cada coluna uma ação

azul = dados_ibov3[[2]][,c(7,6)]

# Rotina para criar um só data frame com todos esses dados de todas as ações

acao = dados_ibov3[[1]][,c(7,6)]

colnames(acao) = c("Data", paste("Preço",dados_ibov3[[1]][1,8]))

for (i in 2:72){
  novaacao = dados_ibov3[[i]][,c(7,6)]
  colnames(novaacao) = c("Data", paste("Preço",dados_ibov3[[i]][1,8]))
  
  acao = merge(acao, novaacao, by = "Data")
  
}
# ===================================
# Como plotar mais de uma ação ao mesmo tempo?
# Três ações ao mesmo tempo

f = ggplot() + 
  geom_line(data = acao, aes(x = Data, y = acao$`Preço ITUB4.SA`, color = "ITUB4.SA")) +
  geom_line(data = acao, aes(x = Data, y = acao$`Preço BBDC3.SA`, color = "BBDC3.SA")) +
  geom_line(data = acao, aes(x = Data, y = acao$`Preço SANB11.SA`, color = "SANB11.SA")) +
  geom_line(data = acao, aes(x = Data, y = acao$`Preço BBAS3.SA`, color = "BBAS3.SA")) +
  
  xlab('Data') +
  ylab('Preço')

f$labels$colour = "Bancos"

print(f)

# ==================================
# SEÇÃO 04

# Normalizando os dados

# Vamos colocar várias ações num mesmo gráfico para compará-las

# Precisamos normalizar o preço dessas ações para que elas comecem no mesmo ponto

# Precisamos fazer com que o "preço" da ação seja 1 no primeiro dia

Adjcloses1 = acao[,-c(1)]

nova = data.frame(lapply(Adjcloses1,function(x) x/x[1]))

nova$Data = acao$Data

g = ggplot() + 
  geom_line(data = nova, aes(x = Data, y = Preço.EZTC3.SA, color = "EZTC3")) +
  geom_line(data = nova, aes(x = Data, y = Preço.MRVE3.SA, color = "MRVE3")) +
  geom_line(data = nova, aes(x = Data, y = Preço.CYRE3.SA, color = "CYRE3")) +
  
  xlab('Data') +
  ylab('Preço')

g$labels$colour = "Setor: Construção"

print(g)

# ==================================
# E se quiséssemos plotar todas as colunas?

# Primeiro precisamos mudar o formato dos dados

df = melt(nova ,  id.vars = 'Data', variable.name = 'series')

# Plotar no mesmo grid, mas em séries diferentes

ggplot(df, aes(Data,value)) + geom_line(aes(colour = series))

# E se quiséssemos fazer um filtro das 10 primeiras ações?

nova2 = nova[,c(1:10,74)]

df2 = melt(nova2 ,  id.vars = 'Data', variable.name = 'series')

# em plots diferentes
ggplot(df2, aes(Data,value)) + geom_line() + facet_grid(series ~ .)

# no mesmo plot
ggplot(df2, aes(Data,value)) + geom_line(aes(colour = series))


# =======================
# Inserir índices de referência para comparar com nossa carteira

IBOV = BatchGetSymbols(tickers = '^BVSP', bench.ticker = benchmark,
                             first.date = di, last.date = df)

SP500 = BatchGetSymbols(tickers = '^GSPC', bench.ticker = '^GSPC',
                       first.date = di, last.date = df)

# ===================================================================
# ===================================================================

# CÓDIGO CRIADO NO DIA 20/09/20

IBOV = IBOV$df.tickers

SP500 = SP500$df.tickers

colnames(IBOV)[6] = "IBOV"
colnames(IBOV)[7] = "Data"

colnames(SP500)[6] = "S&P500"
colnames(SP500)[7] = "Data"

IBOV = IBOV[,c(7,6)]

SP500 = SP500[,c(7,6)]

acoes_e_ibov = merge(acao,IBOV, by = "Data")

acoes_ibov_sp = merge(acoes_e_ibov,SP500, by = "Data")

# ==================================
# Normalizando os dados com o IBOV e S&P 500
# Precisamos fazer com que o "preço" da ação seja 1 no primeiro dia

Adjcloses_ibov_sp = acoes_ibov_sp[,-c(1)]

nova_ibov_sp = data.frame(lapply(Adjcloses_ibov_sp,function(x) x/x[1]))

nova_ibov_sp$Data = acoes_ibov_sp$Data

h = ggplot() + 
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$Preço.ITUB4.SA, color = "ITUB4.SA")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$Preço.BBDC3.SA, color = "BBDC3.SA")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$Preço.SANB11.SA, color = "SANB11.SA")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$Preço.BBAS3.SA, color = "BBAS3.SA")) +
  
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$IBOV, color = "IBOV")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$S.P500, color = "S&P500")) +
  
  xlab('Data') +
  ylab('Preço')

h$labels$colour = "Bancos"

print(h)


# ==================================
# Vamos obter a correlação dessas ações

# COmando Pipe - de uma forma bem mais direta, execute uma série de comandos
Adjcloses_ibov_sp %>%
  cor(use="complete.obs", method="spearman") %>%
  corrplot(type="lower", method="number", diag=FALSE,number.cex=0.70,number.font=1)

# Uma outra forma de obter as correlações é simplesmente criar um data frame
# com esses valores

correlacoes = cor(Adjcloses_ibov_sp,use="complete.obs", method="spearman")
corrplot(correlacoes,number.cex=0.001,number.font=5)

# É mais prático segmentar essa tabela em tabelas menores

tabela01 = Adjcloses_ibov_sp[,c(1:10,74,75)]

tabela01 %>%
  cor(use="complete.obs", method="spearman") %>%
  corrplot(type="lower", method="number", diag=FALSE,number.cex=0.70,number.font=1)

# ==================================
# vamos criar nossa carteira?
# Que ações você tem na carteira?
# Carteira fictícia:
# 40% WEGE3, 30% EZTC3, 20% IRBR3, 5% ITUB4, 5% ABEV

nova_ibov_sp$carteira = 0.4*nova_ibov_sp$Preço.ITUB4.SA +
  0.3*nova_ibov_sp$Preço.CIEL3.SA +
  0.2*nova_ibov_sp$Preço.CVCB3.SA +
  0.05*nova_ibov_sp$Preço.WEGE3.SA +
  0.05*nova_ibov_sp$Preço.ABEV3.SA


i = ggplot() + 
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$carteira, color = "Minha Carteira")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$IBOV, color = "IBOV")) +
  geom_line(data = nova_ibov_sp, aes(x = Data, y = nova_ibov_sp$S.P500, color = "S&P500")) +
  
  xlab('Data') +
  ylab('Preço')

i$labels$colour = "Comparativo"

print(i)

# Para calcular a correlação na nossa carteira
carteira_df = data.frame(nova_ibov_sp$Preço.ITUB4.SA,
                         nova_ibov_sp$Preço.CIEL3.SA,
                         nova_ibov_sp$Preço.CVCB3.SA,
                         nova_ibov_sp$Preço.WEGE3.SA,
                         nova_ibov_sp$Preço.ABEV3.SA,
                         nova_ibov_sp$carteira,
                         nova_ibov_sp$IBOV,
                         nova_ibov_sp$S.P500)

colnames(carteira_df) = c("ITUB4", "CIEL3", "CVCB3", "WEGE3", 
                          "ABEV3", "Carteira","IBOV", "S&P500")

carteira_df %>%
  cor(use="complete.obs", method="spearman") %>%
  corrplot(type="lower", method="number", diag=FALSE,number.cex=0.70,number.font=1)


# ===================================================================
# ===================================================================

# QUANTMOD
library(quantmod)

?getSymbols


getSymbols(Symbols = "AAPL", from = '2020-01-01', src ='yahoo')

getSymbols(Symbols = "PETR4.SA", from = '2020-01-01', src ='yahoo')
chart_Series(PETR4.SA)

dados_acao_apple = getSymbols(Symbols = "AAPL", from = '2020-01-01', src ='yahoo', auto.assign = FALSE)

# Plotando os dados da ação da Petrobras num formato simples
ggplot(PETR4.SA, aes(index(PETR4.SA), PETR4.SA[,6])) + 
  geom_line(color = "darkblue") + ggtitle("Cotação da PETR4 desde 2020")

# Outra forma de obter o mesmo gráfico
p = ggplot(PETR4.SA, aes(index(PETR4.SA), PETR4.SA[,6])) + 
  geom_line(color = "darkblue") 

p + labs(x = "", y = "Preço Ajustado de Fechamento de PETR4",
         title = "Cotação da PETR4 desde 2020")

PETR4.SAfiltrado = subset(PETR4.SA, index(PETR4.SA)>= '2020-04-01')

# Vamos tentar criar duas médias móveis: 10 períodos e 30 períods
MM_PETR_10 = rollmean(PETR4.SAfiltrado[,6], 10, fill = list(NA, NULL, NA), align = 'right')
MM_PETR_30 = rollmean(PETR4.SAfiltrado[,6], 30, fill = list(NA, NULL, NA), align = 'right')

PETR4.SAfiltrado$MM_PETR_10 = coredata(MM_PETR_10)
PETR4.SAfiltrado$MM_PETR_30 = coredata(MM_PETR_30)

ggplot(PETR4.SAfiltrado, aes(index(PETR4.SAfiltrado))) +
  geom_line(aes(y =PETR4.SAfiltrado[,6], color = "PETR4.SA"))+
  geom_line(aes(y=PETR4.SAfiltrado$MM_PETR_10, color = "MM10"))+
  geom_line(aes(y=PETR4.SAfiltrado$MM_PETR_30, color = "MM30"))

# Código retirado do original da aula
ggplot(PETR4.SA, aes(x = index(PETR4.SA))) + geom_line(aes(y = PETR4.SA[,6], color = "PETR4.SA")) + 
  ggtitle("Série de preços da Petrobrás") +
  geom_line(aes(y = PETR4.SA$MM_PETR_10, color = "MM10")) +
  geom_line(aes(y = PETR4.SA$MM_PETR_30, color = "MM30")) +
  xlab("Data") + ylab("Preço ($)") +
  theme(plot.title = element_text(hjust = 0.5), panel.border = element_blank()) +
  scale_x_date(date_labels = "%b %y", date_breaks = "3 months") +
  scale_colour_manual("Séries", values=c("PETR4.SA"="gray40", "MM10"="firebrick4", "MM30"="darkcyan"))


# Funções que ajudam a calcular o retorno
dailyReturn(PETR4.SAfiltrado)

weeklyReturn(PETR4.SAfiltrado)

monthlyReturn(PETR4.SAfiltrado)

yearlyReturn(PETR4.SAfiltrado)

sd(na.omit(PETR4.SAfiltrado$PETR4.SA.Adjusted))


# ===================================================================
# ===================================================================

# ===================================================================
# DADOS FUNDAMENTALISTAS
# GetDFPData - autoria do prof. Marcelo Perlin

# Como procurar as razões sociais das empresas
empresas = gdfpd.get.info.companies()

my.companies = c("RUMO MALHA NORTE S.A.")

di = "2019-01-01"
df = "2020-01-01"
type.export = "xlsx"

DadosFund_EDP = gdfpd.GetDFPData(name.companies = my.companies,
                                 first.date = di,
                                 last.date = df)

quadrosocial = DadosFund_EDP[[11]]
quadrosocial = data.frame(quadrosocial[[1]])

fluxodecaixa = data.frame(DadosFund_EDP$fr.cashflow)

# ===================================================================
# DADOS MACROECONÔMICOS E COMMODITIES
# Biblioteca Quandl

install.packages("Quandl")
library(Quandl)

install.packages("devtools")
library(devtools)
install_github("quandl/quandl-r")

library(Quandl)

Quandl.api_key("77TfLxTY9XzxycV_uzSe")


?Quandl

# Vamos começar com petróleo WTI
petroleo = Quandl('EIA/PET_RWTC_D', start_date= '2019-01-01')

ggplot(petroleo, aes(x = petroleo$Date, y = petroleo$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série de preços do Petróleo WTI") + xlab("Data") + ylab("Retorno") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")



# =============================
# PIB EUA
pib_eua = Quandl('FRED/GDP', start_date= '1979-01-01')

ggplot(pib_eua, aes(x = pib_eua$Date, y = pib_eua$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série de PIB dos EUA") + xlab("Data") + ylab("PIB") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")

# =============================
# Vamos analisar dados do Brasil
selic = Quandl('BCB/432', start_date= '2000-01-01')

ggplot(selic, aes(x = selic$Date, y = selic$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série da SELIC") + xlab("Data") + ylab("SELIC") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")
# =============================
# IBOV
ibov = Quandl('BCB/7845', start_date= '2000-01-01')

ggplot(ibov, aes(x = ibov$Date, y = ibov$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série") + xlab("Data") + ylab("Valor") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")

# =============================
# Contrato de Ouro
ouro = Quandl('BCB/4', start_date= '2000-01-01')

ggplot(ouro, aes(x = ouro$Date, y = ouro$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série") + xlab("Data") + ylab("Valor") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")

# =============================
# IPCA
ipca = Quandl('BCB/13522', start_date= '1990-01-01')

ggplot(ipca, aes(x = ipca$Date, y = ipca$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Série IPCA") + xlab("Data") + ylab("IPCA") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")

# =============================
# Real vs. Dólar
dolar = Quandl('BCB/10813', start_date= '2000-01-01')

ggplot(dolar, aes(x = dolar$Date, y = dolar$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("Cotação do dólar vs. Real") + xlab("Data") + ylab("Preço Dólar") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")

# =============================
# PIB BRasileiro
pib = Quandl('ODA/BRA_NGDPD', start_date= '1970-01-01')

ggplot(pib, aes(x = pib$Date, y = pib$Value)) + geom_line(color = "deepskyblue4") +
  ggtitle("PIB do Brasil") + xlab("Data") + ylab("PIB") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "1 months")
