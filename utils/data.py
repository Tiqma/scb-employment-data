import pandas as pd

df = pd.read_csv('../data.csv', sep=';', encoding='utf-8')

ana = df.head()

print(ana)