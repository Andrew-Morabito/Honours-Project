import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


### For GitHub viewers:
### the sentiment analysis inference using FinBERT will not run unless the
### computer that it is ran from has an extremely large amount of available
### RAM or VRAM.


# To run FinBERT with the GPU.
if torch.cuda.is_available():
	checkGPU = "cuda:0"
else:
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

# Run the model. This will return a list of logits.
sentimentOutput = model(**inputHeadlines)

# Apply softmax to correctly scale the results from the list of logits.
predictions = torch.nn.functional.softmax(sentimentOutput.logits, dim = -1)
predictions = predictions.tolist()

# FinBERT returns confidence scores in the order of positive, negative, and neutral.
positive = [score[0] for score in predictions]
negative = [score[1] for score in predictions]
neutral = [score[2] for score in predictions]

# Placing the predictions into a dataframe.
table = {
	"Positive": positive,
	"Negative": negative, 
	"Neutral": neutral
}

predictiondf = pd.DataFrame(table, columns = ["Positive", "Negative", "Neutral"])
dataframe = pd.concat([dataframe, predictiondf], axis = 1)

# Saving the dataframe.
dataframe.to_csv("asx200sentiment.csv", index = False)