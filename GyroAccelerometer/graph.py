import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv("~/Desktop/4Fun/GyroAccelerometer/data/monoangolo.csv", sep=";")

cartesian_np = np.array([[math.cos(y) for y in df["ANGLY"]], [math.sin(y) for y in df["ANGLY"]]]).T
cartesian = pd.DataFrame(cartesian_np, columns=["X", "Y"])

fig, ax = plt.subplots()

t=0
for point in cartesian_np:
    if t == 0:
        points, = ax.plot(point[0], point[1], marker='o', linestyle='None')
        ax.set_xlim(-1.2, 1.2) 
        ax.set_ylim(-1.2, 1.2) 
    else:
        points.set_data(point[0], point[1])
    t += 1
    plt.pause(0.1)