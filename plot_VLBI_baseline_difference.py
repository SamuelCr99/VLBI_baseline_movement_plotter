import pandas as pd

reader = pd.read_csv('2023a_bas_apriori.bas', delim_whitespace=True, skiprows=2)

print(reader.loc(0))
