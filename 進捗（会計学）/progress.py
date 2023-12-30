# 学習進捗をプロットするスクリプト

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from pandas import Timedelta


def draw_event(ax, date, label, xlim):
    deltax = Timedelta((xlim[1] - xlim[0]) / 100, unit="D")
    ax.vlines(date, 0, 1, transform=ax.get_xaxis_transform(), colors="red")
    ax.text(date + deltax, 0.5, label, transform=ax.get_xaxis_transform(), color="red")


if __name__ == "__main__":
    plt.rcParams["font.family"] = "Noto Sans JP"

    progress = pd.read_csv("progress.csv", index_col=0)
    event = pd.read_csv("event.csv", index_col=0)

    mm = 25.4
    width = 120 / mm
    height = 80 / mm

    fig, ax = plt.subplots(figsize=(width, height), tight_layout=True)

    progress.index = pd.to_datetime(progress.index)
    event.index = pd.to_datetime(event.index)

    progress = progress.sort_index()
    progress["time"] = progress["h"] + progress["m"] / 60

    progress["time"] = progress["time"].cumsum()

    ax.plot(progress.index, progress["time"], label="勉強時間")
    ax.set_ylabel("累積勉強時間（時間）")
    ax.set_title("会計系資格勉強時間")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

    xlim = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.2)

    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))

    for i in range(len(event)):
        draw_event(ax, event.index[i], event["event"].iloc[i], xlim)

    plt.savefig("progress.svg")
    plt.savefig("progress.png", dpi=300)
