import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def saveplot(data, title, file_name, type, label):
    plt.clf()
    txt = "Saman Soltani\nPaderborn University\nInteractive Data Visualization"
    plt.subplots_adjust(bottom=0.2)
    plt.figtext(0.99, 0.01, txt, wrap=True,
                ha="right", va="bottom", fontsize=8)
    plt.title(title)
    if type == 'img':
        plt.imshow(data, 'gray')
    elif type == 'bar':
        plt.bar(data.keys(), data.values())
    elif type == 'plot':
        plt.plot(data)

    if label:
        plt.xlabel(label[0])
        plt.ylabel(label[1])

    plt.savefig("./outputs/" + file_name + ".png", dpi=300)


file_raw = np.fromfile("volume.raw", dtype="int16")
data = np.ndarray.reshape(file_raw, (421, 512, 512))

data_a = np.zeros((421, 512))
for z in range(421):
  for x in range(512):
    data_a[z, x] = np.sum(data[z, 0:512, x])

saveplot(data_a, 'Medical CT Image (Task a) X/Z Plane', 'task-a', 'img', ['X axis', 'Z axis'])

data_b = np.zeros((421, 512))
for z in range(421):
    plane = data[z, 0:512, 0:512]
    for k in range(-255, 256):
      x = k + 256
      data_b[z, x] = np.sum(np.diag(plane, k))

saveplot(data_b, 'Medical CT Image (Task b) X/Z Plane', 'task-b', 'img', ['X axis', 'Z axis'])