import pandas as pd
import matplotlib.pyplot as plt


def load(name, resample=True, resample_metric="W"):
    df = pd.read_csv(name)
    if resample:
        df.datetime = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        df.set_index(["datetime"], inplace=True)
        df = df.resample(resample_metric)
    return df


# def plot(df_i):
#     fig = plt.figure(figsize=(18, 14))
#     for i, c in enumerate(columns):
#         ax = plt.subplot(4, 4, i + 1)
#         dfs[df_i][c].mean().plot(ax=ax, label=c)
#         ax.set_xticklabels([])
#         ax.legend(loc="upper left")

#     fig.suptitle(filenames[df_i])
#     plt.show()


def print_items(items):
    for e in items:
        print(e)
