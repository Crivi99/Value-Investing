import pandas as pd
import numpy as pn

df = pd.read_csv('/Users/criveanubogdan/Desktop/Intrinsic value based on financials/Intrinsic.csv')

df = df[(df['Current Price']<= df['Graham Intrinsic']) & (df['Current Price']<= df['Modern Intrinsic']) & (df['Current Price']<= df['Financial Intrinsic'])]

df.to_csv('Value.csv')