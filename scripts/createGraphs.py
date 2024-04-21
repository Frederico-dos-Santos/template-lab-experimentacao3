from matplotlib import pyplot as plt
from pandas import DataFrame

def dispertion(df: DataFrame, columns: object, labels: object, title: str, color: str="orange"):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[columns["x"]], df[columns["y"]], color=color)
    plt.xlabel(labels["x"])
    plt.ylabel(labels["y"])
    plt.title(title)
    plt.show()

def violin(df: DataFrame, column: str, title: str):
    plt.figure(figsize=(10, 6))
    plt.violinplot(df[column].fillna(0))
    plt.xlabel(column)
    plt.title(title)
    plt.show()

    