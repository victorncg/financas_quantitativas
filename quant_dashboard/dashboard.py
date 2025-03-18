import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt

# Função para buscar os dados
def get_stock_data(ticker, start_date):
    data = yf.download(ticker, start=start_date, progress=False, auto_adjust=False)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]  # Ajusta nomes das colunas
    return data

# Função para calcular métricas quantitativas
def calculate_metrics(data):
    data2 = data.copy()
    data2['Returns'] = data2['Adj Close'].pct_change()
    data2['Cumulative Return'] = (1 + data2['Returns']).cumprod()
    data2['Drawdown'] = (data2['Cumulative Return'] / data2['Cumulative Return'].cummax()) - 1
    max_drawdown = data2['Drawdown'].min()
    
    mean_return = data2['Returns'].mean()
    volatility = data2['Returns'].std()
    sharpe_ratio = mean_return / volatility * np.sqrt(252)  # Ajustado para dias úteis
    VaR_95 = np.percentile(data2['Returns'].dropna(), 5)  # VaR a 95%
    cvar_95 = data2['Returns'][data2['Returns'] <= VaR_95].mean()  # CVaR (Expected Shortfall)
    
    metrics = {
        'Retorno Médio Diário': round(mean_return, 2),
        'Volatilidade': round(volatility, 2),
        'Sharpe Ratio': round(sharpe_ratio, 2),
        'VaR (95%)': round(VaR_95, 2),
        'CVaR (95%)': round(cvar_95, 2),
        'Max Drawdown': round(max_drawdown, 2)
    }
    
    return data2, metrics

# Configuração do Streamlit
st.title("📈 Dashboard Quantitativo de Ações")
st.write("Digite o ticker de uma ação e a data de início para obter um relatório quantitativo.")

ticker = st.text_input("Ticker da ação (ex: PETR4.SA, AAPL, TSLA)", value="PETR4.SA")
benchmark = st.text_input("Ticker do benchmark (ex: ^BVSP, ^GSPC)", value="^BVSP")
start_date = st.date_input("Selecione a data de início", pd.to_datetime("2025-03-10"))

if ticker and start_date:
    st.subheader(f"📊 Dados para {ticker}")
    
    data = get_stock_data(ticker, start_date.strftime('%Y-%m-%d'))
    benchmark_data = get_stock_data(benchmark, start_date.strftime('%Y-%m-%d'))
    
    if not data.empty and not benchmark_data.empty:
        st.success("✅ Dados capturados com sucesso!")
        
        # Exibir dados brutos antes de qualquer modificação
        st.write("### 📊 Amostra dos Dados Brutos")
        st.dataframe(data.tail(10))
        
        # Configurar limites do eixo Y para evitar que ele comece do zero
        y_min = data['Adj Close'].min() * 0.95
        y_max = data['Adj Close'].max() * 1.05
        
        # Gráfico do preço de fechamento sem modificações
        st.write("### 📈 Gráfico de Preço de Fechamento (Dados Brutos)")
        chart = alt.Chart(data.reset_index()).mark_line().encode(
            x='Date:T', y=alt.Y('Adj Close:Q', scale=alt.Scale(domain=[y_min, y_max])), 
            tooltip=['Date', 'Adj Close']
        ).properties(title=f'Preço de Fechamento - {ticker}')
        st.altair_chart(chart, use_container_width=True)
        
        # Gerar métricas apenas após exibição dos dados brutos
        data2, metrics = calculate_metrics(data)
        benchmark_data2, _ = calculate_metrics(benchmark_data)
        
        # Normalizando apenas 'Adj Close' com a média dos primeiros 5 dias
        norm_data = data2[['Adj Close']].copy()
        norm_data['Normalized'] = norm_data['Adj Close'] / norm_data['Adj Close'].iloc[:5].mean()
        norm_data = norm_data.reset_index()
        
        benchmark_norm = benchmark_data2[['Adj Close']].copy()
        benchmark_norm['Normalized'] = benchmark_norm['Adj Close'] / benchmark_norm['Adj Close'].iloc[:5].mean()
        benchmark_norm = benchmark_norm.reset_index()
        
        # Ajuste do eixo Y para valores normalizados
        y_min_norm = min(norm_data['Normalized'].min(), benchmark_norm['Normalized'].min()) * 0.98
        y_max_norm = max(norm_data['Normalized'].max(), benchmark_norm['Normalized'].max()) * 1.02
        
        st.success("✅ Análise concluída com sucesso!")
              
        st.write("### 📊 Retorno Acumulado Comparado com Benchmark")
        chart2 = alt.Chart(norm_data).mark_line().encode(
            x='Date:T', y=alt.Y('Normalized:Q', scale=alt.Scale(domain=[y_min_norm, y_max_norm])), 
            color=alt.value('blue'), tooltip=['Date', 'Normalized']
        ).properties(title=f'Retorno Acumulado - {ticker}')
        
        chart_benchmark = alt.Chart(benchmark_norm).mark_line().encode(
            x='Date:T', y=alt.Y('Normalized:Q', scale=alt.Scale(domain=[y_min_norm, y_max_norm])), 
            color=alt.value('red'), tooltip=['Date', 'Normalized']
        ).properties(title=f'Retorno Acumulado - {benchmark}')
        
        st.altair_chart(chart2 + chart_benchmark, use_container_width=True)
        
        st.write("### 📉 Gráfico de Drawdown")
        chart3 = alt.Chart(data2.reset_index()).mark_area().encode(
            x='Date:T', y='Drawdown:Q', tooltip=['Date', 'Drawdown']
        ).properties(title=f'Drawdown - {ticker}')
        st.altair_chart(chart3, use_container_width=True)
        
        st.write("### 📌 Métricas Quantitativas")
        st.json(metrics)
    else:
        st.error("⚠️ Não foi possível obter os dados. Verifique os tickers e tente novamente.")
