import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


print(sns.get_dataset_names())
data = sns.load_dataset('diamonds')
data.info()
bp_x = 'cut'
bp_y = 'carat'
bp_hue = 'clarity'
bp_ci = None

bp = sns.barplot(data=data, x=bp_x, y=bp_y, hue=bp_hue, ci=bp_ci)
plt.show()