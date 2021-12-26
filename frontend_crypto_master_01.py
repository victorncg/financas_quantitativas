import streamlit as st
import pandas as pd
import bitfinex
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


header = st.beta_container()
ranking = st.beta_container()

@st.cache
def analisa_retornos(number, timeframe, periods):
    # Create api instance of the v2 API
    api_v2 = bitfinex.bitfinex_v2.api_v2()

    import requests

    url = "https://api.bitfinex.com/v1/symbols"

    response = requests.request("GET", url)

    # Fazendo split das criptos
    lines = [i.strip().split(';') for i in response.text.split(',')]

    # Transformando cada palavra em um novo item da lista
    flat_list = [item for sublist in lines for item in sublist]

    # Removendo caracteres indesejados
    new_list = [s.replace(' " ', "") for s in flat_list]

    new_list = [s.replace("'", "") for s in new_list]

    new_list = [s.replace('"', "") for s in new_list]

    new_list = [s.replace('[', "") for s in new_list]

    new_list = [s.replace(']', "") for s in new_list]

    res = [i for i in new_list if 'usd' in i]

    # Trazendo as 50 criptos mais importanes
    number_coins = int(number)

    importantes = res[0:8]

    #importantes = importantes[0:number_coins]

    completo = pd.DataFrame([], columns =['Open', 'Close', 'High', 'Low', 'PAR'])

    negocios_close = pd.DataFrame()

    for i in importantes:

        # Define the start date
        t_start = datetime.datetime(2021, 1, 1, 0, 0)
        t_start = time.mktime(t_start.timetuple()) * 1000

        # Define the end date
        t_stop = datetime.datetime(2021, 8, 3, 0, 0)
        t_stop = time.mktime(t_stop.timetuple()) * 1000

        # Download OHCL data from API
        result = api_v2.candles(symbol=i, interval=timeframe, limit=int(periods), start=t_start, end=t_stop)

        # Convert list of data to pandas dataframe
        names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
        df = pd.DataFrame(result, columns=names)
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        df.index = df.Date

        negocios_close[i] = df['Close']

    ativos_retornos_1h = negocios_close.pct_change()

    ativos_retornos_1h = ativos_retornos_1h.dropna()

    returns_acm = (1 + ativos_retornos_1h).cumprod()

    returns_acm['Date'] = returns_acm.index.strftime("%d/%m/%y")

    returns_acm.index = returns_acm['Date'] 

    returns_acm.drop(['Date'], axis = 1, inplace = True)


    return returns_acm


@st.cache
def retorna_grafico(moeda, timeframe, periods):
    # Create api instance of the v2 API
    api_v2 = bitfinex.bitfinex_v2.api_v2()

    import requests

    url = "https://api.bitfinex.com/v1/symbols"

    response = requests.request("GET", url)

    pair = str(moeda)

    TIMEFRAME = timeframe

    # Define the start date
    t_start = datetime.datetime(2020, 9, 1, 0, 0)
    t_start = time.mktime(t_start.timetuple()) * 1000

    # Define the end date
    t_stop = datetime.datetime(2021, 8, 3, 0, 0)
    t_stop = time.mktime(t_stop.timetuple()) * 1000

    # Download OHCL data from API
    result = api_v2.candles(symbol=pair, interval=TIMEFRAME, limit=int(periods), start=t_start, end=t_stop)

    # Convert list of data to pandas dataframe
    names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
    df = pd.DataFrame(result, columns=names)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')

    negocios = df.copy()

    negocios = negocios.iloc[::-1]
    negocios.index = negocios.Date

    return negocios

@st.cache
def ultimos_retornos(timeframe):
    # Create api instance of the v2 API
    api_v2 = bitfinex.bitfinex_v2.api_v2()

    import requests

    url = "https://api.bitfinex.com/v1/symbols"

    response = requests.request("GET", url)

    # Fazendo split das criptos
    lines = [i.strip().split(';') for i in response.text.split(',')]

    # Transformando cada palavra em um novo item da lista
    flat_list = [item for sublist in lines for item in sublist]

    # Removendo caracteres indesejados
    new_list = [s.replace(' " ', "") for s in flat_list]

    new_list = [s.replace("'", "") for s in new_list]

    new_list = [s.replace('"', "") for s in new_list]

    new_list = [s.replace('[', "") for s in new_list]

    new_list = [s.replace(']', "") for s in new_list]

    res = [i for i in new_list if 'usd' in i]

    # Trazendo as 50 criptos mais importanes
    importantes = res[0:21]

    #number_coins = int(number)

    #importantes = importantes[0:number_coins]

    completo = pd.DataFrame([], columns =['Open', 'Close', 'High', 'Low', 'PAR'])

    TIMEFRAME = timeframe

    for j in importantes:

        # Define the start date
        t_start = datetime.datetime(2021, 1, 1, 0, 0)
        t_start = time.mktime(t_start.timetuple()) * 1000

        # Define the end date
        t_stop = datetime.datetime(2021, 8, 3, 0, 0)
        t_stop = time.mktime(t_stop.timetuple()) * 1000

        # Download OHCL data from API
        #print(f"Baixando dados da moeda {j} ")
        result = api_v2.candles(symbol=j, interval=TIMEFRAME, limit=50, start=t_start, end=t_stop)

        # Convert list of data to pandas dataframe
        names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
        df = pd.DataFrame(result, columns=names)
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        negocios_1h = df.copy()

        negocios_1h = negocios_1h.iloc[::-1]
        negocios_1h.index = negocios_1h.Date
        negocios_1h.drop(['Date','Volume'], axis = 1, inplace = True)

        ativos_retornos_1h = negocios_1h.pct_change()

        ativos_retornos_1h = ativos_retornos_1h.dropna()

        last_line_coin = pd.DataFrame(ativos_retornos_1h.iloc[-1]).transpose()

        last_line_coin['PAR'] = str(j).upper()

        completo = pd.concat([completo, last_line_coin])
        #print(f"Anexação dos dados da moeda {j} concluída \n")


    #print("O tempo de execução desse programa foi de %s segundos ---" % (time.time() - start_time))

    # O data frame 'completo' que a função solta vai conter o último resultado de todas as criptos para um dado timeframe
    completo.index = completo.PAR
    completo.drop(['PAR'], axis = 1, inplace = True)
    completo = completo.sort_values(by='Close', ascending=False)

    return completo



with header:
    st.title('Painel Easy Crypto')
    st.text('Painel de exibição do desempenho de criptomoedas em exchanges ao redor do mundo')  
  
with ranking:
# PARTE 01 - VISÃO GERAL ========================================================================================
    sel_col, disp_col = st.beta_columns([1,3])
    sel_col.header("Visão Geral")
    
    # Exibição do gráfico
    disp_col.subheader('Visualização de desempenho')

    exchange = sel_col.selectbox('Qual exchange você deseja?', options = ['Binance', 'Bitfinex', 'Poloniex'], index = 0)
    n_coins = sel_col.slider('Quantas moedas deseja incluir na análise do ranking?', min_value = 1, max_value = 100, value = 50, step = 5)
    timeframe = sel_col.selectbox('Qual timeframe você deseja?', options = ['1 hora', '1 dia', '1 semana'], index = 0)
    exibicao = sel_col.slider('Quantas moedas deseja visualizar no gráfico ao lado?', min_value = 1, max_value = 10, value = 5, step = 1)
    periodos = sel_col.slider('Quantos perídos deseja trazer?', min_value = 1, max_value = 400, value = 200, step = 5)

    if timeframe == '1 hora':
        TF = '1h'
    elif timeframe == '1 dia':
        TF = '1D'
    else:
        TF = '1W'
    
    interval = int(periodos)

    number_coins = 0
    df_retornos = analisa_retornos(number_coins, TF, interval)
    numero_exib = int(exibicao)
    plotable = df_retornos.iloc[:, 0:numero_exib] 
    
    pd.options.plotting.backend = "plotly"
    figax = plotable.plot()

    disp_col.write(figax)

# PARTE 02 - RANKING ========================================================================================
    sel_col, disp_col = st.beta_columns([1,3])
    sel_col.header("Parâmetros")
    #exchange = sel_col.selectbox('Qual exchange você deseja?', options = ['Binance', 'Bitfinex', 'Poloniex'], index = 0)
    #n_coins = sel_col.slider('Quantas moedas deseja incluir na análise do ranking?', min_value = 1, max_value = 100, value = 5, step = 1)
    #exibicao = sel_col.slider('Quantas moedas deseja visualizar no gráfico ao lado?', min_value = 1, max_value = 10, value = 5, step = 1)
    #timeframe = sel_col.selectbox('Qual timeframe você deseja?', options = ['1 hora', '1 dia', '1 semana'], index = 0
    #user_coin = sel_col.text_input('Deseja analisar uma moeda específica? Digite', 'BTCUSD')

    completo = ultimos_retornos(TF)

    top10 = completo.head(10)
    bottom10 = completo.tail(10)

    # Exibição do gráfico
    disp_col.subheader('Ranking das criptomoedas ganhadoras e perdedoras em retorno')

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    def SetColor(y):
        if(y >= 0):
            return "green"
        elif(y < 0):
            return "red"
    
    y=top10["Close"]

    z=bottom10["Close"]
    fig = make_subplots(rows=1, cols=2,  subplot_titles=("Ganhadores","Perdedores"))

    fig.add_trace(
        go.Bar(x=top10.index, y=top10["Close"], marker=dict(color = list(map(SetColor, y))),name="Retorno positivo"),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=bottom10.index, y = bottom10["Close"], marker=dict(color = list(map(SetColor, z))),name="Retorno negativo"),
        row=1, col=2
    )

    fig.update_layout(height=500, width=1000)
    
    # Apresenta o gráfico
    disp_col.write(fig)

# PARTE 03 - ANÁLISE TÉCNICA ========================================================================================
    sel_col, disp_col = st.beta_columns([1,3])
    sel_col.header("Análise Técnica")
    
    # Exibição do gráfico
    disp_col.subheader('Visualização do indicador')

    coin_choice = sel_col.selectbox('Escolha a criptomoeda', options = ['Bitcoin', 'Ethereum', 'Litecoin'], index = 0)
    figura = sel_col.selectbox('Escolha a figura de análise técnica', options = ['Média Móvel Simples', 'Média Móvel Exponencial', 'Índice de Força Relativa', 'Bandas de Bollinger'], index = 0)
    #timeframe_at = sel_col.selectbox('Qual timeframe você deseja?', options = ['1 hora', '1 dia', '1 semana'], index = 0)
    
    if coin_choice == 'Bitcoin':
        moeda = 'btcusd'
    elif coin_choice == 'Ethereum':
        moeda = 'ethusd'
    else:
        moeda = 'ltcusd'

    if figura == 'Média Móvel Simples':
        plot_option = 'MMS'
    elif figura == 'Média Móvel Exponencial':
        plot_option = 'MME'
    elif figura == 'Índice de Força Relativa':
        plot_option = 'IFR'
    elif figura == 'Bandas de Bollinger':
        plot_option = 'BB'
    else:
        plot_option = 'BB'


    negocios = retorna_grafico(moeda, TF, interval)
    pd.options.plotting.backend = "plotly"

    negocios['mm20'] = negocios.Close.rolling(window=20).mean()
    negocios['mm100'] = negocios.Close.rolling(window=100).mean()

    figat = negocios[['Close','mm20','mm100']].plot()

    disp_col.write(figat)