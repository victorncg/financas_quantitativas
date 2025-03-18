def return_index(index:str):    

    import requests
    import pandas as pd

    conversion = {'ibov':'Qk9W',
                 'ibra':'QlJB',
                 'ifix': 'RklY',
                  'idiv': 'RElW'}

    hash_code = f'eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJ{conversion[index]}Iiwic2VnbWVudCI6IjEifQ=='

    full_url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/" + hash_code

    response = requests.get(full_url)
    data = pd.DataFrame(response.json()["results"])

    return data
