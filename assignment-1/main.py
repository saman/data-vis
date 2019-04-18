import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl
import math 

cmap = plt.cm.jet
cNorm  = colors.Normalize(vmin=0, vmax=1)
scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=cmap)

# read the file with pandas
df = pd.read_csv('field2.csv')

fig = plt.figure()

# make axis
ax  = fig.add_axes([0.1, 0.1, 0.7, 0.85]) # [left, bottom, width, height]
axc = fig.add_axes([0.85, 0.10, 0.05, 0.85])

# iterate between flow items
for index, row in df.iterrows():
  
  # caluclate length of arrow
  new_pos_x = row.x + row.u
  new_pos_y = row.y + row.v
  a = row.x - new_pos_x
  b = row.y - new_pos_y
  length = math.sqrt(a * a + b * b)

  # make color base of length
  colorVal = scalarMap.to_rgba(length)

  # add an arrow
  ax.arrow(  row.x,
             row.y,
             row.u,
             row.v,
             color=colorVal,
             head_width=0.009,
             head_length=0.009
          ) 

# make the legend
cb1 = mpl.colorbar.ColorbarBase(axc, cmap=cmap, norm=cNorm,orientation='vertical')              

# show the result
plt.show()