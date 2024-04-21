from matplotlib import pyplot as plt
from pandas import DataFrame

def dispertion(df: DataFrame, columns: object, labels: object, title: str, color: str="orange"):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[columns["x"]], df[columns["y"]], color=color)
    plt.xlabel(labels["x"])
    plt.ylabel(labels["y"])
    plt.title(title)
    plt.show()

def bar(bars: list, values: list, value_label: str, title: str, colors: list=['blue', 'green', 'orange', 'red', 'purple']):
    plt.figure(figsize=(10, 6))
    plt.bar(bars, values, color=colors)
    plt.ylabel(value_label)
    plt.title(title)
    plt.grid(axis='y')
    plt.show()
    