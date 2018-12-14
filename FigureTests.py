import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#All available sample data sets
print(sns.get_dataset_names())


#PAIRPLOT
data = sns.load_dataset("titanic")
data = data.dropna()
#data['month'], _ = pd.factorize(data['month'])
data.info()
print(data)

#sns.pairplot(data=data, kind="reg")
#plt.show()


#HEATMAP
#data = sns.load_dataset("dots")
#data.dropna()
#data.info()
#print(data)
data = data.corr()
sns.heatmap(data=data)
plt.show()