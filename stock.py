import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class Stock:
    def __init__(self,ticker):
        self.ticker = ticker
        self.yahoo_finance_url = 'https://finance.yahoo.com/quote/'

        self.summary = None
        self.analysis = None
        self.current_price = None

        # self.df_summary = None
        # self.df_analysis= None

            

    def GetSummary(self):
        ticker = self.ticker
        yahoo_finance_url = self.yahoo_finance_url

        page_summary = requests.get(yahoo_finance_url + ticker, headers={'User-Agent': 'Custom'})

        soup = BeautifulSoup(page_summary.text, 'html.parser')

        table1 = soup.find('table', class_ = 'W(100%)')

        info_rows = table1.find_all('tr')

        info_summary = {}

        for info_num in range(len(info_rows)):
            row = []
            for row_item in info_rows[info_num].find_all("td"):
                aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
                row.append(aa)
            info_summary[row[0]] = row[1]


        table2 = soup.find('table', class_ = 'W(100%) M(0) Bdcl(c)') #the table with the useful info inside summary

        info_rows = table2.find_all('tr')

        for info_num in range(len(info_rows)):
            row = []
            for row_item in info_rows[info_num].find_all("td"):
                aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
                row.append(aa)
            info_summary[row[0]] = row[1]

        return info_summary

    def GetCurrentPrice(self):
        ticker = self.ticker
        yahoo_finance_url = self.yahoo_finance_url

        page_summary = requests.get(yahoo_finance_url + ticker, headers={'User-Agent': 'Custom'})

        soup = BeautifulSoup(page_summary.text, 'html.parser')

        price = soup.find('div', class_='D(ib) Mend(20px)').find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')

        return float(re.sub("(\xa0)|(\n)|,","",price.text))

    def GetAnalysis(self):
        infos = {}
        ticker = self.ticker
        yahoo_finance_url = self.yahoo_finance_url

        page_analysis = requests.get(yahoo_finance_url + ticker + '/analysis', headers={'User-Agent': 'Custom'})

        soup = BeautifulSoup(page_analysis.text, 'html.parser')

        main_div = soup.find('div', id= 'Main')

        tables = main_div.find_all('table')

        for table in tables:
            try:
                title = table.find('tr', class_='Ta(start)').find('th', class_='Fw(b) Fw(s) W(20%) Py(10px) C($primaryColor)').find('span')
                
            except:
                title = table.find('tr', class_='Ta(start)').find('th', class_='W(20%) Fz(s) Fw(b) C($primaryColor) Py(10px) Ta(start)')

            title = re.sub("(\xa0)|(\n)|,","",title.text)

            content = table.find('tbody')
            table_info = {}
            for row in content.find_all('tr'):
                try:
                    row_name = re.sub("(\xa0)|(\n)|,","",row.find('td', class_='Py(10px) Ta(start)').text)
                except:
                    row_name = re.sub("(\xa0)|(\n)|,","",row.find('td', class_='Ta(start) Py(10px)').text)
                
                row_content = []

                for value in row.find_all('td')[1:]:
                    row_content.append(re.sub("(\xa0)|(\n)|,","",value.text))

                table_info[row_name] = row_content
            
            infos[title] = table_info

        return infos

    
def get_all_data(stock: Stock):
    stock.summary = stock.GetSummary()
    stock.analysis = stock.GetAnalysis()
    stock.current_price = stock.GetCurrentPrice()





if __name__ == '__main__':
    # print(Stock('LEO.DE').GetCurrentPrice())

    stock = Stock('AAPL')
    get_all_data(stock)
