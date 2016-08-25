#! python3
# Visualization with Pandas

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.mpl_style = 'default'

df = pd.read_csv('Rent information.csv')
df = df[np.isfinite(df['Price_per_tenant'])]

print(df.describe())
groupby_zip = df['Price_per_tenant'].groupby(df['Area_code']).mean()
print(groupby_zip)
ax = df.boxplot(column = 'Price_per_tenant', by = 'Area_code')
plt.show(ax)
input("press key to exit")


