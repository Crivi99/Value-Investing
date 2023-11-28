import pandas as pd
import numpy as np
from IntrinsicValue import GrahamIntrinsic, ModernIntrinsic, FinancialIntrinsic
from stock import Stock, get_all_data
import threading
import time

class IntrinsicTable():
    def __init__(self, tickers_path) -> None:
        self.tickers = pd.read_csv(tickers_path)
        self.tickers = self.tickers['Company Ticker'].to_list()[:100]
        self.stocks = [Stock(ticker) for ticker in self.tickers]

    @staticmethod
    def paralel_computing(inputs, function):
        threads = []
        for input in inputs:
            thread = threading.Thread(target=function(input))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
 
    def create_dataframe(self):

        res = pd.DataFrame(list(zip(self.stocks, self.tickers)), columns=['stock','ticker'])

        res['Current Price'] = res['stock'].apply(lambda x: x.current_price)
        res['Graham Intrinsic'] = np.vectorize(GrahamIntrinsic)(res['stock'])
        res['Modern Intrinsic'] = np.vectorize(ModernIntrinsic)(res['stock'])
        res['Financial Intrinsic'] = np.vectorize(FinancialIntrinsic)(res['stock'])
        
        res = res.drop(columns=['stock'])
        print(res)
        return res


if __name__ == '__main__':
    start_time = time.time()
    table = IntrinsicTable('/Users/criveanubogdan/Desktop/Intrinsic value based on financials/list_of_companies.csv')
    end_time = time.time()
    create_table = end_time - start_time

    start_time = time.time()
    table.paralel_computing(table.stocks, get_all_data)
    end_time = time.time()
    get_data = end_time - start_time

    start_time = time.time()
    table.create_dataframe()
    end_time = time.time()
    intrinsic_table = end_time - start_time

    print(f'Creating the instances: {create_table:.4f}s')
    print(f'Get all data: {get_data:.4f}s')
    print(f'Compute intrinsic: {intrinsic_table:.4f}s')