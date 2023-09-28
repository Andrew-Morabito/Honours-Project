import pandas as pd

# To do:
# Add data exploration and profiling methods for the ASX data.


dataframe = pd.read_csv("asx200data.csv")

wordFreq = dataframe.Title.str.split(expand = True).stack().value_counts()

print(wordFreq)