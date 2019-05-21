__author__ = "Saman Soltani"

import numpy as np
import matplotlib.pyplot as plt
import math

file_names = ['i170b1h0_t0', 'i170b2h0_t0', 'i170b3h0_t0', 'i170b4h0_t0']

size = 500
scale = 255

def nonlinear(value, min_value, max_value):
    log_min = math.log(min_value) if min_value > 0 else 0
    log_max = math.log(max_value) if max_value > 0 else 0
    if value > 0:
        log = math.log(value)
        if log > 0:
            return (log - log_min) / (log_max - log_min) * scale
    return 0

def saveplot(data, title, file_name, type):
    plt.clf()
    txt = "Saman Soltani\nPaderborn University\nInteractive Data Visualization"
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.figtext(0.99, 0.01, txt, wrap=True,
                ha="right", va="bottom", fontsize=8)
    plt.title(title)
    if type == 'im':
        plt.imshow(data, 'gray')
        plt.gca().invert_yaxis()
    if type == 'imc':
        plt.imshow(data)
        plt.gca().invert_yaxis()
    elif type == 'hist':
        plt.xlabel('Value')
        plt.ylabel('Frequency')        
        plt.hist(data, histtype="step")
    elif type == 'bar':
        plt.bar(data.keys(), data.values())        
    elif type == 'plot':
        plt.plot(data)

    if type == 'im' or type == 'imc':
      x = [10, 150, 290, 430]
      y = [60, 180, 300, 380, 420]
      xlabels = ['5h45m', '5h30m', '5h15m', '5h00m']
      ylabels = ['-15:00', '-12:00', '-9:00', '5h45m', '-6:00']
      plt.xticks(x, xlabels)
      plt.yticks(y, ylabels)

    plt.savefig("./outputs/" + file_name + ".png", dpi=300)


def task(file_name):
    min_value = 0
    max_value = 0

    # load whole file
    file_path = "./orion/" + file_name + ".txt"
    with open(file_path, 'r') as content_file:
        content = content_file.read()

    # remove extra quotation marks
    content = content.replace('"', "")
    lines = content.split('\n')
    data = []
    data_list = []
    line_x = 0
    # read data with comma delimiter
    for i in range(len(lines)):
        if (len(lines[i])):
            data.append(np.fromstring(lines[i], sep=',', dtype=float))
            for value in data[len(data) - 1]:
                data_list.append(value)


    # calculate min
    min_value = min(data_list)

    # calculate max
    max_value = max(data_list)

    # calculate mean
    mean = np.mean(data_list)

    # calculate variance
    variance = np.var(data_list)

    # nonlinear filter
    nonlinear_data = np.zeros((size, size))
    profile_line = []
    for i in range(size):
        for j in range(size):
            nonlinear_data[i][j] = nonlinear(data[i][j], min_value, max_value)

            # coordinate max profile line
            if (data[i][j] == max_value):
                for k in range(size):
                    profile_line.append(data[i][k])

    # calculate histogram equalization
    r, indices = np.unique(data_list, return_inverse=True)
    p = np.zeros(len(r))
    for i in indices:
        if r[i] in r:
            p[i] += 1

    pr = np.zeros(len(r))
    cdf = np.zeros(len(r))
    cdf255 = np.zeros(len(r))
    sum_pr = 0
    for i, v in enumerate(p):
        if p[i] > 0:
            pr[i] = v/(size*size)
        else:
            pr[i] = 0

        sum_pr += pr[i]
        cdf[i] = sum_pr
        cdf255[i] = cdf[i] * scale

    cdf255_all = cdf255[indices]
    cdf255_matrix = np.ndarray.reshape(cdf255_all, (size, size))

    # save all plots
    saveplot(cdf255_matrix, "Histogram Equalization: " + file_name, file_name + "-he", "im")
    
    if (file_name == "i170b2h0_t0"):
        saveplot(profile_line, "Max Profile Line: " + file_name, file_name + "-pl", "plot")
        saveplot(nonlinear_data, "Non-Linear: " + file_name, file_name + "-nl", "imc")
        saveplot(data_list, "Histogram: " + file_name, file_name + "-h", "hist")

        # save text files
        text = ""
        text += "file: " + file_name + "\n"
        text += "min: " + str(min_value) + "\n"
        text += "max: " + str(max_value) + "\n"
        text += "mean: " + str(mean) + "\n"
        text += "variance: " + str(variance) + "\n"

        with open("./outputs/" + file_name + ".txt", "w+") as out:
            out.write(text)

    return cdf255_matrix


# run all files
cdf255_data = {}
for file_name in file_names:
    cdf255_data[file_name] = task(file_name)

# combine all bands
combine_data = np.zeros((size, size, 3), dtype=np.uint8)
for x in range(size):
    for y in range(size):
        r = int(round(cdf255_data['i170b4h0_t0'][x][y]))
        g = int(round(cdf255_data['i170b3h0_t0'][x][y]))
        b = int(round(cdf255_data['i170b1h0_t0'][x][y]))
        color = [r, g, b]
        combine_data[x][y] = color

# save combined result
saveplot(combine_data, "Histogram Equalization: Combine", "combine-he", "im")
