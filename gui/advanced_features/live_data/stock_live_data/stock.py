from taipy.gui import Gui, invoke_long_callback, notify, navigate
import yahoo_fin.stock_info as si
import yfinance as yf
import datetime as dt
import time

import warnings
import pandas as pd

import numpy as np


# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

list_of_stocks = ['Simulation', 'AAPL', 'MSFT', 'AMZN', 'TSLA', "EURUSD=X", "GC=F", "BTC-USD", "ETH-USD", "XRP-USD"]
stock_str = 'Simulation'
news = None


class Stock:
    def __init__(self, stock):
        self.simulation = True if stock == 'Simulation' else False
        self.stock = stock if not self.simulation else 'TSLA'
        self.stock_obj = yf.Ticker(self.stock)

        self.update_news()
        self.update_history()

        self.live_data = pd.DataFrame(columns=['Date', 'Stock'])
        self.before_value = self.value = si.get_live_price(self.stock)
        self.open = False


    def check_if_open(self):
        last_date = self.data['Date'].iloc[-1]
        now = dt.datetime.now()
        if (now - last_date > dt.timedelta(hours=4) and self.value == self.before_value) or np.sum(self.live_data['Stock']-self.value)==0:
            self.open = False
        else:
            self.open = True

    def update_news(self):
        self.news = [(n["link"], n["title"]) for n in self.stock_obj.news]

    def update_history(self):
        self.data = yf.download(self.stock, start=dt.datetime.now()-dt.timedelta(days=3), interval='1m')[-700:]
        self.data.loc[:, 'Date'] = self.data.index.tz_localize(None)
        self.data.loc[:, 'Stock'] = (self.data['High']+self.data['Low'])/2

    def update_data(self):
        now = dt.datetime.now()
        diff = self.value - self.before_value

        self.check_if_open()
        self.before_value = self.value 

        if self.simulation:
            diff /= np.abs(np.sum(self.data['Stock'][:-5]))
            self.value += np.random.uniform(-0.03+diff, 0.03+diff)
        else:
            self.value = si.get_live_price(self.stock) 

        self.live_data.loc[len(self.live_data), ['Date','Stock']] = now, self.value
        self.live_data.reset_index(drop=True, inplace=True)
        self.live_data = self.live_data[-100:]


#<|{stock_str}|selector|lov={list_of_stocks}|dropdown|class_name=fullwidth|label=Select the Stock|on_change=change_stock|>

page = """<|toggle|theme|>
<|container|
# Live **Stock**{: .color-primary} Data

<|{stock_str}|selector|lov={list_of_stocks}|dropdown|class_name=fullwidth|label=Select the Stock|on_change=change_stock|>


**Market Status:** <|{'Open' if stock_object.open else 'Closed - Waiting for a response...'}|text|raw|>

# <|{stock_object.stock}|text|raw|> <|{'- Simulation' if stock_object.simulation else ''}|> 

<|2 2 5|layout|
<stock_value|
Stock value
### <|{round(stock_object.value, 4)}|text|raw|> $ <|{'↗️' if stock_object.value > stock_object.before_value else '↘️'}|>
|stock_value>

<stock_variation|
Stock variation
#### <|{round(stock_object.value - stock_object.before_value, 4)} ({round(((stock_object.value - stock_object.before_value)/stock_object.before_value)*100, 4)} %)|text|class_name={'red' if stock_object.value - stock_object.before_value < 0 else 'green'}|raw|>
|stock_variation>
|>

<|{stock_object.live_data}|chart|x=Date|y=Stock|title=Live View|>

## **Historical**{: .color-primary}  Data

<|{historical_data}|chart|type=candlestick|x=Date|open=Open|close=Close|low=Low|high=High|height=600px|title=Historical Data|>

<|Tables|expandable|not expanded|
<|{stock_object.live_data}|table|>

<|{historical_data}|table|>
|>

## Related **News**{: .color-primary} 

<|{news}|selector|class_name=fullwidth|lov={stock_object.news}|value_by_id|on_change=navigate_to_link|>
|>
"""


def change_stock(state):
    state.updating = True
    new_stock = state.stock_str
    notify(state, "info", f'Changing to {new_stock}...')
    state.stock_object = Stock(new_stock)
    notify(state, "success", f'Changed to {state.stock_object.stock}!')
    state.updating = False

def update(state, status):
    if not state.updating:
        state.stock_object.update_data()
        state.refresh('stock_object')

        if status % 100 == 0:
            print(f"Status: {status}")
            state.stock_object.update_history()
            state.historical_data = state.stock_object.data


def iddle():
     while True:
        time.sleep(1)

def on_init(state):
    invoke_long_callback(state, iddle, [], update, [], 2000)

def on_exception(state, function_name: str, ex: Exception):
    print(ex, 'in ', function_name)
    notify(state, 'error', f"A problem occured in {function_name}")


def navigate_to_link(state):
    navigate(state, to=state.news, force=True)
    state.news = None


updating = False
stock_object = Stock(stock_str)
historical_data = stock_object.data


if __name__ == "__main__":
    gui = Gui(page=page)
    gui.run(title='Real Live Stock', port=5960)
