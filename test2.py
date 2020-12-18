import matplotlib.style
import matplotlib.pyplot as plt
from matplotlib import figure
import pandas as pd
from matplotlib.animation import FuncAnimation
from itertools import count

plt.style.use('classic')

x_vals = []
y_vals = []
#index = count()

frame_len = 10000
fig = plt.figure(figsize=(9, 6))
#fig, ax = plt.subplots(figsize=(9, 6))


def animate(i):
    data = pd.read_csv('sentiment.csv')

    y1 = data['Trump']
    y2 = data['Biden']

    if len(y1) <= frame_len:
        plt.cla()
        plt.plot(y1, label='Donald Trump')
        plt.plot(y2, label='Joe Biden')

    else:
        plt.cla()

        plt.plot(y1[-frame_len:], label='Donald Trump')
        plt.plt(y2[-frame_len:], label='Joe Biden')
        # plt.gcf().autofmt_xdate()

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)
