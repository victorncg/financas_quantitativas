# MODULE FOR OBTAINING ALTERNATIVE DATA

# SOME OF THE ALTERNATIVE DATA WE CAN OBTAIN FROM THIS MODULE
# IBOV Composition
# Google Trends
# CVM
# B3
# S&P 500


# Criar uma função prévia que obtém os dados do IBOV, antes de processá-lo

import pandas as pd

import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def _logging_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


# Função para extrair os dados do IBOV
@_logging_error
def _parse_ibov():
    
    try:
        
        url = 'https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv'
        df = pd.read_csv(url, encoding='latin-1', sep='delimiter', header=None, engine='python')
        df = pd.DataFrame(df[0].str.split(';').tolist())
        
        return df
        
    except:
        
        print("An error occurred while parsing data from IBOV.")



@_logging_error
def _standardize_ibov():
    
    try:
        
        url = 'https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv'
        df = pd.read_csv(url, encoding='latin-1', sep='delimiter', header=None, engine='python')
        df = pd.DataFrame(df[0].str.split(';').tolist())
        df.columns = list(df.iloc[1])
        df[2:][['Código','Ação',	'Tipo',	'Qtde. Teórica','Part. (%)']]
        df.reset_index(drop=True, inplace=True)
        
        return df
        
    except:
        
        print("An error occurred while parsing data from IBOV.")


def _standardize_sp500():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]

  return df


@_logging_error
def index_composition(index = 'ibov', ativos = 'all', mode = 'df', reduction = True):

  '''
  This function captures the latest composition of IBOV. It is updated every 4 months.

  Parameters
    ----------
  ativos : you can pass a list with the desired tickets. Default = 'all'.
  mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
  reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True.

  '''
  
  if index = 'ibov':
      df = _standardize_ibov()
      
      if reduction == False:
        df = df[:-2]
    
      if ativos != 'all':
        df = df[df['Código'].isin(ativos)]    
    
      if mode == 'list':
        df = list(df.Código)
    
  if index = 'sp500':
      df = _standardize_sp500()
    


  return df



