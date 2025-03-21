# -*- coding: utf-8 -*-
"""Utilizando biblioteca brFinance.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bnC4Mfl5DQnBq3f6_8rJnxp3N8K4Gno4

# **Tutorial brfinance**

Confira aqui um tutorial de como utilizar a biblioteca brFinance, idealizada por Eudes Oliveira.

Documentação:
https://github.com/eudesrodrigo/brFinance

A instalação pode ser feita diretamente pelo comando !pip, uma vez que esta lib está no PyPi

#### Instalação e Importação
"""

!pip install brfinance

from brfinance import CVMAsyncBackend
import pandas as pd
from datetime import datetime, date

"""#### Conexão com a CVM

Quase tudo nesta lib gira em torno da classe CVMAsyncBackend. É através dela que conseguiremos gerar uma conexão com a plataforma Rad da CVM e realizar a extração dos dados.

Para entender melhor como esta classe é estruturada, verifique a documentação do backend:

https://github.com/eudesrodrigo/brFinance/blob/10e3f249a23916741c9537890bfda342a0f24b0d/brfinance/backend.py

Portanto, a primeira etapa é utilizar esta classe para criar um elemento de client que vai possibilitar a extração.
"""

cvm_httpclient = CVMAsyncBackend()

"""#### Extração de dados brutos

Feito isso, podemos começar a captura dos nossos dados.

Você pode utilizar as seguintes funções:

**get_cvm_codes:** Obtém os códigos cvm disponíveis para todas as empresas. Retorna um dicionário com o código CVM de chave e o nome da empresa.

**get_consulta_externa_cvm_categories:** Obtém os códigos para as categorias de busca disponíveis, dentre elas "DFP", "ITR", etc. Retorna um dicionário com o código da busca e a descrição.

**get_consulta_externa_cvm_results:** Obtém o resultado da busca para os dados informados. Retorna um dataframe com os resultados. *Parâmetros: cod_cvm, start_date, end_date, last_ref_date, report_type*

**get_report:** Utilizado para obter todos os demonstrativos de uma empresa na CVM. Retorna um dicionário com os nomes e os valores dos demonstrativos em um dataframe. *Parâmetros: numero_seq_documento, codigo_tipo_instituicao, reports_list, previous_results*

Vamos começar obtendo os códigos CVM para todas as empresas listadas
"""

cvm_codes = cvm_httpclient.get_cvm_codes()
print(cvm_codes)

# Realizando busca por Empresa
start_date = date(2019, 1, 1)
end_dt = date.today()
cvm_codes_list = ['5258'] # B3 DROGA RAIA
category = ["EST_4", "EST_3", "IPE_4_-1_-1"] # Códigos de categoria para DFP, ITR e fatos relevantes
last_ref_date = False # Se "True" retorna apenas o último report no intervalo de datas

# Realizando busca por Empresa SOMENTE DFP E ITR
start_date = date(2019, 1, 1)
end_dt = date.today()
cvm_codes_list = ['5258'] # B3 DROGA RAIA
category = ["EST_4", "EST_3"]
last_ref_date = False # Se "True" retorna apenas o último report no intervalo de datas

# Busca
search_result = cvm_httpclient.get_consulta_externa_cvm_results(
    cod_cvm=cvm_codes_list,
    start_date=start_date,
    end_date=end_dt,
    last_ref_date=last_ref_date,
    category=category
    )

"""Observe que vamos obter aqui vários demonstrativos - DFP e ITR"""

search_result

search_result['view_url'].loc[0]

"""Copie e cole esta URL no seu navegador para inspecionar o resultado!"""

search_result.columns

"""Verifique a trimestralidade dos demonstrativos"""

search_result['ref_date'].unique()

"""#### Obtenção de um report específico

E se quiséssemos apenas um demonstrativo específico?
"""

ativo = pd.DataFrame()

#Ativo
reports_list = None # Se None retorna todos os demonstrativos disponíveis.
# Outra opção é especificar o demonstrativo que você deseja:

reports_list = ['Balanço Patrimonial Ativo']


# Filtro search_result para ITR e DFP apenas
search_result = search_result[
    (search_result['categoria']=="DFP - Demonstrações Financeiras Padronizadas")]

search_result

search_result = search_result[pd.to_numeric(search_result['numero_seq_documento'], errors='coerce').notnull()]

search_result

"""Aqui, vamos buscar linha a linha pelos demonstrativos solicitados. Lembre-se de que os demonstrativos estão nas URLs apresentadas na coluna "view_url". 

O que estamos fazendo aqui é indo nos códigos dos demonstrativos, um a um, e colocando-os em um novo dataframe.
"""

for index, row in search_result.iterrows():
    empresa = f"{row['cod_cvm']} - {cvm_codes[row['cod_cvm']]} - {row['numero_seq_documento']} - {row['codigo_tipo_instituicao']}"
    print("*" * 20, empresa, "*" * 20)
    
    reports = cvm_httpclient.get_report(row["numero_seq_documento"], row["codigo_tipo_instituicao"],reports_list=reports_list)
    for report in reports:
        ativo = ativo.append(reports, ignore_index=True)

"""Para ficar mais fácil de entender, estamos usando aqui a função get_report isoladamente para obter o número de seq. documento 100794 como descrito pela CVM no dataframe acima, com o codigo_tipo_instituicao = 1. Confira o resultado.

"""

dict_example = cvm_httpclient.get_report(100794, 1,reports_list=reports_list)

dict_example.keys()

dict_example['Balanço Patrimonial Ativo']

"""Uma vez que entendemos isso, vamos ver como ficaria o **reports** completo, obtido a partir do loop definido acima."""

reports.keys()

reports['Balanço Patrimonial Ativo']

reports['Demonstração do Resultado']

