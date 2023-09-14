import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


### For GitHub viewers:
### the sentiment analysis inference using FinBERT will not run unless the
### computer that it is ran from has an extremely large amount of available
### RAM or VRAM.


# To run FinBERT with the GPU.
'''
if torch.cuda.is_available():
	checkGPU = "cuda:0"
else:
	checkGPU = "cpu"
'''
checkGPU = "cpu"
# Initialise the FinBERT tonkenizer and model.
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
model = model.to(torch.device(checkGPU))

# Read the ASX200 data and move the headlines into a seperate array.
dataframe = pd.read_csv("asx200data.csv")
headlines = []

for index, row in dataframe.iterrows():
	title = row["Title"].strip('"')
	headlines.append(title)

# Create input tensors for each of the headlines.
inputHeadlines = tokenizer(headlines, padding = True, truncation = True, return_tensors = "pt")
inputHeadlines.to(torch.device(checkGPU))

# Run the model to return the sentiments from each headline.
sentimentOutput = model(**inputHeadlines)

# Apply softmax to the sentiment results so that the elements are scaled correctly.
predictions = torch.nn.functional.softmax(sentimentOutput.logits, dim = -1)

# To fix up.
positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()

table = {
	"Headline": headlines,
	"Positive": positive,
	"Negative": negative, 
	"Neutral": neutral
}

exampledf = pd.DataFrame(table, columns = ["Headline", "Positive", "Negative", "Neutral"])
print(exampledf.head(5))
