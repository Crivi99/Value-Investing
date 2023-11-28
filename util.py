import requests
from bs4 import BeautifulSoup
import re

def GetCorporateBondYield():
    page_summary = requests.get('https://fred.stlouisfed.org/series/AAA')

    soup = BeautifulSoup(page_summary.text, 'html.parser')

    value = soup.find('div', id='series-meta-row').find('div', class_='col-xs-12 col-sm-7 col-md-6').find('span', class_='series-meta-observation-value')

    return float(re.sub("(\xa0)|(\n)|,","",value.text))

