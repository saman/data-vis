__author__ = "Saman Soltani"

import struct
import matplotlib.pyplot as plt
import numpy as np
import math

file_path = "slice150.raw"
size = 512
scale = 255
min = 0
max = 0


def saveplot(data, title, file_name, type):
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

    plt.savefig("./outputs/" + file_name + ".png")


def makehistogram(data):
    i = 0
    histogram = {}
    for x in range(0, size):
        for y in range(0, size):
            value = data[x, y]
            if value in histogram:
                histogram[value] += 1
            else:
                histogram[value] = 1
            i += 1
    return histogram

# linear transformation function
def linear(value):
    return (value - min) / (max - min) * scale

# nolinear transformation function
def nonlinear(value):
    log_min = math.log(min) if min > 0 else 0
    log_max = math.log(max) if max > 0 else 0
    if value > 0:
        log = math.log(value)
        if log > 0:
            return (log - log_min) / (log_max - log_min) * scale
    return 0


# reading raw data
with open(file_path, "rb") as f:
    raw_data = f.read()

# get 12 bit data
data = []
total = 0
total_sqr = 0
histogram_data = {}

for i in range(0, len(raw_data), 2):
    # combining bits of first byte and bits of second byte with bitwise
    value = raw_data[i] | raw_data[i + 1] << 8
    data.append(value)
    total += value
    total_sqr += value * value

    # making histogram data
    if value in histogram_data:
        histogram_data[value] += 1
    else:
        histogram_data[value] = 1

    # calculate min and max
    if i == 0:
        min = value
        max = value

    if value < min:
        min = value

    if value > max:
        max = value


# calculate mean
mean = total / len(data)
with open("./outputs/slice150-mean.txt", "w+") as out:
    out.write(str(mean))

# calculate variance
variance = total * total
variance /= len(data)
variance = total_sqr - variance
variance /= len(data) - 1
with open("./outputs/slice150-variance.txt", "w+") as out:
    out.write(str(variance))

# visualize the image
i = 0
pixels = np.zeros((size, size))
pixels_linear = np.zeros((size, size))
pixels_nonlinear = np.zeros((size, size))
for x in range(size - 1, -1, -1):
    for y in range(0, size):
        pixels[x, y] = data[i]
        # linear transformation
        pixels_linear[x, y] = linear(data[i])
        pixels_nonlinear[x, y] = nonlinear(data[i])
        i += 1

# calculating boxcar and median filter
filter_size = 11
min_range = int(filter_size / 2)
max_range = int(filter_size / 2) + 1
pixels_boxcar = np.zeros((size, size))
pixels_median = np.zeros((size, size))
pixels_nonlinear_min = np.zeros((size, size))
pixels_nonlinear_max = np.zeros((size, size))
for x in range(min_range, size - min_range):
    for y in range(min_range, size - min_range):
        s_total = 0
        square_data = []
        new_x = 0
        new_y = 0
        # making the square cut
        for s_x in range(-min_range, max_range):
            for s_y in range(-min_range, max_range):
                current_x = x + s_x
                current_y = y + s_y
                square_data.append(pixels[current_x, current_y])
                if s_x == 0 and s_y == 0:
                    new_x = current_x
                    new_y = current_y
        # calculate the boxcar and median base on filter
        square_data.sort()
        pixels_boxcar[new_x, new_y] = sum(square_data) / (filter_size * filter_size)
        pixels_median[new_x, new_y] = square_data[int(len(square_data)/2)]
        pixels_nonlinear_min[new_x, new_y] = linear(square_data[0])
        pixels_nonlinear_max[new_x, new_y] = linear(square_data[len(square_data) - 1])
        

# 256 profile line
profile_line = []
y = 255
for x in range(0, size):
    profile_line.append(pixels[x, y])

# making histrograms
pixels_linear_histogram = makehistogram(pixels_linear)
pixels_nonlinear_histogram = makehistogram(pixels_nonlinear)
pixels_nonlinear_min_histogram = makehistogram(pixels_nonlinear_min)
pixels_nonlinear_max_histogram = makehistogram(pixels_nonlinear_max)


# logs data (just in case)
# log_data = pixels_nonlinear
# log = ""
# for x in range(0, size):
#     for y in range(0, size):
#         log += str(log_data[y, x]) + ","
#     log += "\n"
# with open("./outputs/log.csv", "w+") as out:
#     out.write(log)

# for index, (key, value) in enumerate(histogram_data.items()):
    # print(key,', ', value, sep='', flush=True)


saveplot(pixels, "Slice 150", "slice150", "img")
saveplot(histogram_data, "Histogram", "slice150-histogram", "bar")

saveplot(pixels_boxcar, "Boxcar Filter", "slice150-boxcar", "img")
saveplot(pixels_median, "Median Filter", "slice150-median", "img")

saveplot(pixels_linear, "Linear Transformation", "slice150-linear", "img")
saveplot(pixels_linear_histogram, "Linear Transformation Histogram", "slice150-linear-histogram", "bar")

saveplot(pixels_nonlinear, "Non-Linear Transformation", "slice150-nonlinear", "img")
saveplot(pixels_nonlinear_histogram, "Non-Linear Transformation Histogram", "slice150-nonlinear-histogram", "bar")

saveplot(pixels_nonlinear_max, "Non-Linear Transformation (Max Filter)", "slice150-nonlinear-max", "img")
saveplot(pixels_nonlinear_max_histogram, "Non-Linear Transformation Histogram (Max Filter)", "slice150-nonlinear-min-histogram", "bar")

saveplot(pixels_nonlinear_min, "Non-Linear Transformation (Min Filter)", "slice150-nonlinear-min", "img")
saveplot(pixels_nonlinear_min_histogram, "Non-Linear Transformation Histogram (Min Filter)", "slice150-nonlinear-max-histogram", "bar")

saveplot(profile_line, "256 Profile Line", "slice150-profile-line", "plot")