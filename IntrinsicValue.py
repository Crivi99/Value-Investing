from stock import Stock
from util import GetCorporateBondYield
import numpy as np

def Intrinsic(stock: Stock, NoGrowth, MultiplierGrowth, CorporateBond):
    EPS = float(stock.summary['EPS (TTM)'])
    G = float(stock.analysis['Growth Estimates']['Next 5 Years (per annum)'][0][:-1])
    print(EPS, G)
    return (EPS*(NoGrowth + MultiplierGrowth * G)*4.4)/CorporateBond


def GrahamIntrinsic(stock: Stock):
    try:
        return Intrinsic(stock, 8.5, 2, GetCorporateBondYield())
    except:
        return np.nan

def ModernIntrinsic(stock: Stock):
    try:
        return Intrinsic(stock, 7, 1, GetCorporateBondYield())
    except:
        return np.nan

def FinancialIntrinsic(stock: Stock):
    try:
        EPS = float(stock.summary['EPS (TTM)'])
        PEratio = float(stock.summary['PE Ratio (TTM)'])
        G = float(stock.analysis['Growth Estimates']['Next 5 Years (per annum)'][0][:-1])
        return (EPS * (1 + G/100) * PEratio)
    except:
        return np.nan

if __name__ == '__main__':
    functions = [GrahamIntrinsic,ModernIntrinsic,FinancialIntrinsic]
    for evaluation in functions:

        print(evaluation(Stock('LEO.DE')))