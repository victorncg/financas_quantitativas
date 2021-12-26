library(ggplot2)
library(scales)
library(BatchGetSymbols)

bvsp = BatchGetSymbols('^BVSP', first.date = as.Date('2002-12-31'),
                       last.date = as.Date('2017-09-12'))

ggplot(bvsp$df.tickers, aes(x = ref.date, y = price.close))+
  geom_line()+
  scale_y_discrete(limits=c(10000, 20000, 30000, 40000, 50000, 60000,
                            70000))+
  scale_x_date(breaks = date_breaks("1 years"),
               labels = date_format("%Y"))+
  xlab('')+ylab('Pontos')+
  labs(title='Índice Bovespa',
       caption='Fonte: analisemacro.com.br com dados do Yahoo Finance.')


# ================================================================

bvsp = BatchGetSymbols('AMZN', first.date = as.Date('2002-12-31'),
                       last.date = as.Date('2017-09-12'))

ggplot(bvsp$df.tickers, aes(x = ref.date, y = price.close))+
  geom_line()+
  scale_y_discrete(limits=c(600, 700, 800, 900, 1000, 1100, 1200))+
  scale_x_date(breaks = date_breaks("1 years"),
               labels = date_format("%Y"))+
  xlab('')+ylab('Pontos')+
  labs(title='Índice Bovespa',
       caption='Fonte: analisemacro.com.br com dados do Yahoo Finance.')

# ================================================================

acn = BatchGetSymbols('ACN', first.date = as.Date('2002-12-31'),
                       last.date = as.Date('2019-09-12'))

ggplot(acn$df.tickers, aes(x = ref.date, y = price.close))+
  geom_line()+
  scale_y_discrete()+
  scale_x_date(breaks = date_breaks("1 years"),
               labels = date_format("%Y"))+
  xlab('')+ylab('Pontos')+
  labs(title='Índice Bovespa',
       caption='Fonte: analisemacro.com.br com dados do Yahoo Finance.')

# ================================================================

petr4 = BatchGetSymbols('PETR4.SA', first.date = as.Date('2002-12-31'),
                      last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")

ggplot(petr4$df.tickers, aes(x = ref.date, y = price.close))+
  geom_line()+
  scale_y_discrete()+
  scale_x_date(breaks = date_breaks("1 years"),
               labels = date_format("%Y"))+
  xlab('')+ylab('Pontos')+
  labs(title='Petrobrás',
       caption='Fonte: analisemacro.com.br com dados do Yahoo Finance.')

petr4df = petr4$df.tickers

Adjcloses1 = petr4df[,-c(7:10)]

nova = data.frame(lapply(Adjcloses1,function(x) x/x[1]))

nova$data = petr4df$ref.date

plot(nova$price.adjusted, type = "l")








ggplot(nova, aes(x = data, y = price.adjusted))+
  geom_line()+
  scale_y_discrete()+
  scale_x_date(breaks = date_breaks("1 years"),
               labels = date_format("%Y"))+
  xlab('')+ylab('Pontos')+
  labs(title='Petrobrás',
       caption='RETORNOS PETR4')






d <- ggplot() + 
  geom_line(data = aa, aes(x = Date1, y = aa$SAPR4, color = "SAPR4"),size=0.72) +
  geom_line(data = aa, aes(x = Date1, y = aa$SBSP3, color = "SBSP3"),size=0.72) +
  geom_line(data = aa, aes(x = Date1, y = aa$CGAS3, color = "CGAS3"),size=0.72) +
  
  xlab('Data') +
  ylab('Pre?o Normalizado')

d$labels$colour <- "Servi?os P?blicos"

print(d)







# WEGE3 - Retornando informações da ação
wege = BatchGetSymbols('WEGE3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
wege.df = wege$df.tickers
wege.nova = data.frame(lapply(wege.df[,-c(7:10)],function(x) x/x[1]))
wege.nova$data = wege.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
wege.nova.merge = data.frame(data = wege.nova$data, WEGE3 = wege.nova$price.adjusted)


# VALE3 - Retornando informações da ação
vale = BatchGetSymbols('VALE3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
vale.df = vale$df.tickers
vale.nova = data.frame(lapply(vale.df[,-c(7:10)],function(x) x/x[1]))
vale.nova$data = vale.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
vale.nova.merge = data.frame(data = vale.nova$data, VALE3 = vale.nova$price.adjusted)


# MGLU3 - Retornando informações da ação
mglu = BatchGetSymbols('MGLU3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
mglu.df = mglu$df.tickers
mglu.nova = data.frame(lapply(mglu.df[,-c(7:10)],function(x) x/x[1]))
mglu.nova$data = mglu.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
mglu.nova.merge = data.frame(data = mglu.nova$data, MGLU3 = mglu.nova$price.adjusted)


# EQTL3 - Retornando informações da ação
eqtl = BatchGetSymbols('EQTL3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
eqtl.df = eqtl$df.tickers
eqtl.nova = data.frame(lapply(eqtl.df[,-c(7:10)],function(x) x/x[1]))
eqtl.nova$data = eqtl.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
eqtl.nova.merge = data.frame(data = eqtl.nova$data, EQTL3 = eqtl.nova$price.adjusted)
plot(eqtl.nova$price.adjusted, type = "l")


# LREN3 - Retornando informações da ação
lren = BatchGetSymbols('LREN3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
lren.df = lren$df.tickers
lren.nova = data.frame(lapply(lren.df[,-c(7:10)],function(x) x/x[1]))
lren.nova$data = lren.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
lren.nova.merge = data.frame(data = lren.nova$data, LREN3 = lren.nova$price.adjusted)
plot(lren.nova$price.adjusted, type = "l")


# EZTC3 - Retornando informações da ação
eztc = BatchGetSymbols('EZTC3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
eztc.df = eztc$df.tickers
eztc.nova = data.frame(lapply(eztc.df[,-c(7:10)],function(x) x/x[1]))
eztc.nova$data = eztc.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
eztc.nova.merge = data.frame(data = eztc.nova$data, EZTC3 = eztc.nova$price.adjusted)
plot(eztc.nova$price.adjusted, type = "l")


# PETR4 - Retornando informações da ação
petr = BatchGetSymbols('PETR4.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
petr.df = petr$df.tickers
petr.nova = data.frame(lapply(petr.df[,-c(7:10)],function(x) x/x[1]))
petr.nova$data = petr.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
petr.nova.merge = data.frame(data = petr.nova$data, PETR4 = petr.nova$price.adjusted)
plot(petr.nova$price.adjusted, type = "l")




# LAME4 - Retornando informações da ação
lame = BatchGetSymbols('LAME4.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
lame.df = lame$df.tickers
lame.nova = data.frame(lapply(lame.df[,-c(7:10)],function(x) x/x[1]))
lame.nova$data = lame.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
lame.nova.merge = data.frame(data = lame.nova$data, LAME4 = lame.nova$price.adjusted)


# BBDC4 - Retornando informações da ação
bbdc = BatchGetSymbols('BBDC4.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
bbdc.df = bbdc$df.tickers
bbdc.nova = data.frame(lapply(bbdc.df[,-c(7:10)],function(x) x/x[1]))
bbdc.nova$data = bbdc.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
bbdc.nova.merge = data.frame(data = bbdc.nova$data, BBDC4 = bbdc.nova$price.adjusted)


# ITUB4 - Retornando informações da ação
itub = BatchGetSymbols('ITUB4.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
itub.df = itub$df.tickers
itub.nova = data.frame(lapply(itub.df[,-c(7:10)],function(x) x/x[1]))
itub.nova$data = itub.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
itub.nova.merge = data.frame(data = itub.nova$data, ITUB4 = itub.nova$price.adjusted)


# USIM5 - Retornando informações da ação
usim = BatchGetSymbols('USIM5.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
usim.df = usim$df.tickers
usim.nova = data.frame(lapply(usim.df[,-c(7:10)],function(x) x/x[1]))
usim.nova$data = usim.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
usim.nova.merge = data.frame(data = usim.nova$data, USIM5 = usim.nova$price.adjusted)



# HGTX3 - Retornando informações da ação
hgtx = BatchGetSymbols('HGTX3.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
hgtx.df = hgtx$df.tickers
hgtx.nova = data.frame(lapply(hgtx.df[,-c(7:10)],function(x) x/x[1]))
hgtx.nova$data = hgtx.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
hgtx.nova.merge = data.frame(data = hgtx.nova$data, HGTX3 = hgtx.nova$price.adjusted)


# CMIG4 - Retornando informações da ação
cmig = BatchGetSymbols('CMIG4.SA',first.date = as.Date('2010-12-31'),last.date = as.Date('2019-09-12'),bench.ticker = "^BVSP")
cmig.df = cmig$df.tickers
cmig.nova = data.frame(lapply(cmig.df[,-c(7:10)],function(x) x/x[1]))
cmig.nova$data = cmig.df$ref.date

# Fazendo modificação de forma a conter apenas data e o preço ajustado
cmig.nova.merge = data.frame(data = cmig.nova$data, CMIG4 = cmig.nova$price.adjusted)



total.merge = merge(wege.nova.merge,vale.nova.merge, by = "data")
total.merge = merge(total.merge, mglu.nova.merge , by = "data")
total.merge = merge(total.merge, eqtl.nova.merge , by = "data")
total.merge = merge(total.merge, lren.nova.merge , by = "data")
total.merge = merge(total.merge, eztc.nova.merge , by = "data")
total.merge = merge(total.merge, petr.nova.merge , by = "data")

total.merge = merge(total.merge, lame.nova.merge , by = "data")
total.merge = merge(total.merge, bbdc.nova.merge , by = "data")
total.merge = merge(total.merge, itub.nova.merge , by = "data")
total.merge = merge(total.merge, usim.nova.merge , by = "data")
total.merge = merge(total.merge, hgtx.nova.merge , by = "data")
total.merge = merge(total.merge, cmig.nova.merge , by = "data")



# COmeçando o processo de normalizar os dados e calcular médias e desvio-padrão

replaced = replaceNaWithLatest(total.merge)

replaced2 = na.locf(replaced, fromLast = TRUE)

Adjcloses_new = data.frame(sapply(replaced2, function(x) as.numeric(x)))

Adjcloses1 = Adjcloses_new[,-1]

# Normalizando dados    
nova = data.frame(lapply(Adjcloses1,function(x) x/x[1]))

nova = na.omit(nova)

# Daily returns  
daily = sapply(nova,function(x) (diff(x)/x[-length(x)]))

# Vamos remover outliers que podem ter sido gerados quando calculamos os retornos
daily <- data.frame(daily)

daily <- rm.outlier(daily)

# =========================================================================================
# Returns/Volatility index
retvol <- data.frame(apply(daily,2,function (x) (mean(x)/sd(x))))

retvol2 <- data.frame(retvol[order(retvol$apply.daily..2..function.x...mean.x..sd.x...), drop = FALSE,])

meant <- apply(daily,2,function (x) mean(x))

sdev <- apply(daily,2,function (x) sd(x))

# daily3 <- apply(daily,2,function (x) remove_outliers(x))

tovar <- rbind (meant,sdev)

tovar <- data.frame(t(tovar))

ggplot(tovar, aes(x= sdev, y= meant, colour="green")) +geom_text(aes(label=rownames(tovar),
                                                                     colour=sdev,size=meant),hjust=0, vjust=0,check_overlap = F)+ scale_radius(range = c(4,6))+  
  xlab('Desvio-Padrão') + ylab('Média dos Retornos') + theme(text = element_text(size=10)) + coord_cartesian(xlim = c(0.015, 0.045), ylim = c(0, 0.003))