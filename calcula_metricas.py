import yfinance as yf


def razao_preco_media(stock, start, mm):
    weg = yf.download('WEGE3.SA', start = '2019-01-01')