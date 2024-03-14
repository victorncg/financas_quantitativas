import time
import pandas as pd
import datetime

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


@_logging_error
def create_interval(start_date: object, end_date: object):

    """
    This function is responsible for receiving user input for start and end dates for data extraction and transforming it into YYYYMM format.
    
    :start_date: str
    :end_date: str
    """
    
    b = list()
    end = str(datetime.datetime.strptime(end_date, '%Y-%m-%d').year) + '{:02d}'.format(datetime.datetime.strptime(end_date, '%Y-%m-%d').month +1)

    for year in range(int(datetime.datetime.strptime(start_date, '%Y-%m-%d').year), int(datetime.datetime.strptime(end_date, '%Y-%m-%d').year)+1):

        for month in range(1,13):
            a = '{:02d}{:02d}'.format(year, month)
            if a == end:
                break
            b.append(a)

        if a == end:
            break

        year = year +1

    return b



@_logging_error
def extract_fund_data(dates_list: list, verbose: bool = False):
    start_time = time.time()

    # Initialize an empty list to store individual DataFrames
    dataframes = []
    # Iterate through the files in the folder
    for i in dates_list:

        url_pre = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{i}.zip'
        df_loc = pd.read_csv(url_pre, sep=';', compression='zip')
        s = datetime.datetime.strptime(i, "%Y%m")
        date = s.strftime('%B %Y')
        
        if verbose == True:
            print("Extraction of month",date,"finished")

        # Append the DataFrame to the list
        dataframes.append(df_loc)

    # Combine all DataFrames in the list into one large DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    if verbose == True:
        print("Process took %s seconds" % (time.time() - start_time))

    return combined_df


@_logging_error
def get_fund_data(start: object, end: object, cnpj:object = None, verbose: bool = False):

    """
    This function receives the raw data from function extract_fund_data and filters by date and CNPJ. If user doesn't specify CNPJ, it returns all funds.
  
    :start: str
    :end: str
    :cnpj: str
    :verbose: bool
    """
    interval = create_interval(start, end)
    data_fund = extract_fund_data(interval, verbose)
    data_fund['DT_COMPTC'] = pd.to_datetime(data_fund['DT_COMPTC'])
    mask = (data_fund['DT_COMPTC'] >= start) & (data_fund['DT_COMPTC'] <= end)
    data_fund = data_fund.loc[mask]

    if cnpj != None:
        data_fund = data_fund[data_fund['CNPJ_FUNDO'] == cnpj]

    else:
        data_fund = data_fund

    return data_fund.reset_index(drop=True)
