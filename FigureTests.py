import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#All available sample data sets
print(sns.get_dataset_names())


data = sns.load_dataset("tips")
data = data.dropna()
#data['month'], _ = pd.factorize(data['month'])
data.info()
print(data)

#sns.pairplot(data=data, hue='size', kind="reg")
#plt.show()

#sns.barplot(data=data, x='month', y='passengers', ci=None)

numeric_columns = data.select_dtypes(exclude=['object', 'category'])
print(numeric_columns.columns)
sns.lmplot(data=data, x=numeric_columns.columns[0], y=numeric_columns.columns[1])

#data = sns.load_dataset("dots")
#data.dropna()
#data.info()
#print(data)
#data = data.corr()
#sns.heatmap(data=data)
plt.show()