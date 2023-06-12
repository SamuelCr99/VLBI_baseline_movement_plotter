import matplotlib.pyplot as plt
import pandas as pd

distance = []
year = []

data = pd.read_csv('matching_rows.csv', delim_whitespace=True)

for i in range(len(data)):
    x = data.loc[i]
    distance.append(data.loc[i].length)
    year.append(data.loc[i].year)
    

plt.plot(year, distance)
plt.show()

