import yfinance as yf

# Função para buscar os dados
def get_stock_data(ticker, start_date='2025-03-10'):
    data = yf.download('WEGE3.SA', start = '2025-03-10', progress=False)
    
    return print(data.iloc[0])

get_stock_data('WEGE3.SA')