import threading
import time
from stock import Stock
import pandas as pd

class StockPrice:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.price = 0.0
    
    def get_current_price(self):
        try:
            self.price = Stock(self.ticker).GetCurrentPrice()
        except:
            print(self.ticker)

def get_current_prices(stock_prices: list, parallel: bool):
    if parallel:
        threads = []
        for stock_price in stock_prices:
            thread = threading.Thread(target=stock_price.get_current_price)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        for stock_price in stock_prices:
            stock_price.get_current_price()

if __name__ == '__main__':
    tickers = pd.read_csv('list_of_companies.csv')
    tickers = tickers['Company Ticker'].to_list()
    tickers = tickers[:100]

    stock_prices = [StockPrice(ticker) for ticker in tickers]

    # Retrieve prices sequentially and time it
    start_time = time.time()
    get_current_prices(stock_prices, parallel=False)
    end_time = time.time()
    sequential_time = end_time - start_time

    # Reset prices to zero for parallel retrieval
    for stock_price in stock_prices:
        stock_price.price = 0.0

    # Retrieve prices in parallel and time it
    start_time = time.time()
    get_current_prices(stock_prices, parallel=True)
    end_time = time.time()
    parallel_time = end_time - start_time

    # Print results
    print(f"Sequential time: {sequential_time:.4f}s")
    print(f"Parallel time: {parallel_time:.4f}s")
