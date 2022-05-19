# from django.test import TestCase

# Create your tests here.
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .models import Testdata

plt.style.use('fivethirtyeight')

def plotgraph():

    def animate(i):
        # data = pd.read_csv('/home/pt/ARLIS/ARLISDJ/MLWB/performance/data.csv')
        # x = data['x_value']
        # y1 = data['total_1']
        # y2 = data['total_2']
        qs = Testdata.objects.all()
        x = [x.item for x in qs]
        y1 = [y1.item for y1 in qs]
        y2 = [y2.item for y2 in qs]

        plt.cla()
        plt.plot(x, y1, label='Channel 1')
        plt.plot(x, y2, label='Channel 2')

        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()


