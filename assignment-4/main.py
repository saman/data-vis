__author__ = "Saman Soltani"

import numpy as np
from pandas.plotting import scatter_matrix
from pandas.plotting import parallel_coordinates

import math
import pandas as pd
import matplotlib.pyplot as plt

import plotly as py
import plotly.graph_objs as go

input_file = 'DataWeierstrass.csv'
file_name = 'scatter-matrix.png'

# watermark
txt = __author__ + "\nPaderborn University\nInteractive Data Visualization"
plt.subplots_adjust(bottom=0.1)
plt.figtext(0.99, 0.01, txt, wrap=True, ha="right", va="bottom", fontsize=8)

# calculating mean for all lecture's data
data = pd.read_csv(input_file, delimiter=";").groupby(['professor', 'lecture'], as_index = False).mean()

# choosing columns that we need
df = pd.DataFrame(data, columns=['lecture','participants', 'professional expertise', 'motivation', 'clear presentation', 'overall impression'])

# generating random colors based on len of data
colors = np.random.uniform(0.2, 0.8, (len(df), 3))

# calulcating scatter matrix with help of pandas
scatter_matrix(df, alpha = 0.8, diagonal = 'kde', color=colors)
plt.suptitle("Scatterplot Matrix: Lecture Evaluation")

# plt.savefig("./outputs/" + file_name + ".png", dpi=300)
plt.show()

pc_colors = np.random.uniform(0, 1, len(df))

pc_data = [
    go.Parcoords(
        line = dict(color = pc_colors,  colorscale = 'Jet'),
        dimensions = list([
            dict(label = 'professor', values = data['professor'].values),
            dict(label = 'lecture', values = data['lecture'].values),
            dict(label = 'participants', values = data['participants'].values),
            dict(label = 'professional expertise', values = data['professional expertise'].values, range = [1,5]),
            dict(label = 'motivation', values = data['motivation'].values, range = [1,5]),
            dict(label = 'clear presentation', values = data['clear presentation'].values, range = [1,5]),
            dict(label = 'overall impression', values = data['overall impression'].values, range = [1,5]),
        ])
    )
]

py.offline.plot(pc_data, filename = 'parallel-coordinates.html')

