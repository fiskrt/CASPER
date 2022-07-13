import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load(name, resample=True, resample_metric="W"):
    df = pd.read_csv(name)
    if resample:
        df.datetime = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        df.set_index(["datetime"], inplace=True)
        df = df.resample(resample_metric)
    return df


def print_items(items):
    for e in items:
        print(e)


def plot(mean_latencies, mean_carbon_intensity):
    plt.figure()
    x = np.linspace(0, 24, len(mean_latencies))
    plt.subplot(1, 2, 1)
    plt.plot(x, mean_latencies, label="Latency")
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, mean_carbon_intensity, label="Carbon")
    plt.legend()
    plt.show()
