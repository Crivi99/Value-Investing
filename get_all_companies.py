import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def GetCompanies():
    all_companies = []
    for page_number in range(74):
        page = requests.get(f'https://companiesmarketcap.com/page/{page_number}/')

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('table', class_='default-table table marketcap-table dataTable').find('tbody')

        for row in table.find_all('tr'):
            company = row.find('td', class_='name-td')
            company_ticker = company.find('div', class_='name-div').find('div', class_='company-code')
            company_ticker = re.sub("(\xa0)|(\n)|,","",company_ticker.text)
            all_companies.append(company_ticker)

    return all_companies


df = pd.DataFrame(GetCompanies(), columns=['Company Ticker'])
print(df)
df.to_csv('/Users/criveanubogdan/Desktop/Intrinsic value based on financials/list_of_companies.csv')