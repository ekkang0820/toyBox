import requests
import pandas as pd

API_KEY = 'O6EP7N8HL3GPS0HE'


def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        latest_time = sorted(data['Time Series (1min)'].keys())[0]
        price = float(data['Time Series (1min)'][latest_time]['4. close'])
        return price
    else:
        return None


def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
    else:
        return None


def get_top_gainers_and_losers(symbols):
    gainers = []
    losers = []

    for symbol in symbols:
        df = get_stock_data(symbol)
        if df is not None:
            df['change'] = df['close'].pct_change() * 100
            last_change = df['change'].iloc[-1]
            if last_change > 0:
                gainers.append({'symbol': symbol, 'change': last_change})
            else:
                losers.append({'symbol': symbol, 'change': last_change})

    gainers = sorted(gainers, key=lambda x: x['change'], reverse=True)[:5]
    losers = sorted(losers, key=lambda x: x['change'])[:5]

    return gainers, losers
