import pandas as pd

reader = pd.read_csv('2023a_bas_apriori.csv', delim_whitespace=True)

x = reader.loc[0]
print(x)