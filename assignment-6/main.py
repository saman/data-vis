import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import re

# read data from file
data = pd.read_csv('DataWeierstrass.csv', delimiter = ';')
# group by professor and lecture name and get the mean value
grouped = data.groupby(['professor', 'lecture'], as_index=False).mean()
text=[grouped.loc[ i, 'professor'] for i in range(len(grouped))]

professors = grouped['professor'].drop_duplicates()

profColor ={professors.values[i]: i for i in range(len(professors))}

color_vals=[profColor[c] for c in grouped['professor']]

result = go.Splom(dimensions=[dict(label='Lecture',
                                 values=grouped['lecture']),
                            dict(label='Parti',
                                 values=grouped['participants']),
                            dict(label='Exp',
                                 values=grouped['professional expertise']),
                            dict(label='Motive',
                                 values=grouped['motivation']),
                            dict(label='Present',
                                 values=grouped['clear presentation']),
                            dict(label='Imp',
                                 values=grouped['overall impression'])],

                text=text,
                marker=dict(color=color_vals,
                            size=6,
                            colorscale= 'Jet',
                            showscale=True,
                            line=dict(width=0.5,
                                      color='rgb(230,230,230)'))
                )

result['diagonal'].update(visible=False)

layout = go.Layout(
    showlegend=True,
    title=go.layout.Title(
        text='Scatterplot matrix'
    ))
fig1 = dict(data=[result], layout = layout)
# py.plot(fig1, filename =  "scatterplot matrix")


#converting lecture names to lecture numbers
lectureNumbers = []
for i in range(101):
    str1 = grouped['lecture'].values[i]
    lectureNumbers.append(int(re.findall('\d+', str1)[0]))

data = [
    go.Parcoords(
        line = dict(color = color_vals, showscale = False),
        dimensions = list([
            dict(range = [0,44],
                    label = 'professors', values = np.array(range(1,45))),
            dict(range = [0,101],
                    label = 'lectures', values = lectureNumbers),
            dict(range = [0,max(grouped['participants'])],
                label = 'participants', values = grouped['participants']),
            dict(range = [0,5],
                label = 'professional expertise', values =grouped['professional expertise']),
            dict(range = [0,5],
                label = 'motivation', values = grouped['motivation']),
            dict(range = [0,5],
                label = 'clear presentation', values = grouped['clear presentation']),
            dict(range = [0,5],
                label = 'overall impression', values = grouped['overall impression']),
        ])
    )
]
layout2 = go.Layout(
    title=go.layout.Title(
        text='Parallel Coordinates.'
    ))
fig2 = go.Figure(data = data, layout = layout2)
py.plot(fig2,filename =  "parallel coordinates")
