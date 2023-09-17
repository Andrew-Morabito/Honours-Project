import pandas as pd

dataframe = pd.read_csv("asx200data.csv")

wordFreq = dataframe.Title.str.split(expand = True).stack().value_counts()

print(wordFreq)