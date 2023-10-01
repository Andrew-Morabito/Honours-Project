import pandas as pd
import numpy as np

dataframe = pd.read_csv("asx200sentiment.csv")
dataframe = dataframe[dataframe.Date != "No data for this company"]
dataframe["Date"] = pd.to_datetime(dataframe["Date"])

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"]

for monthIndex in range(7):
	monthlyDF = dataframe.loc[(dataframe["Date"].dt.month == monthIndex + 1) & (dataframe["Date"].dt.year == 2023)]

	dataDict = {
		"Company": [],
		"Date": [],
		"Title": [],
		"Positive": [],
		"Negative": [],
		"Neutral": [],
		"ConfidenceScore": []
	}

	for index, row in monthlyDF.iterrows():
		dataDict["Company"].append(row.Company)
		dataDict["Date"].append(row.Date)
		dataDict["Title"].append(row.Title)
		dataDict["Positive"].append(row.Positive)
		dataDict["Negative"].append(row.Negative)
		dataDict["Neutral"].append(row.Neutral)

		sentiment = [float(row.Positive), float(row.Negative), float(row.Neutral)]
		maxScore = max(sentiment)

		if maxScore == sentiment[0]:
			confidenceScore = sentiment[0] / np.log(2 + row.Date.daysinmonth - row.Date.day)

		elif maxScore == sentiment[1]:
			confidenceScore = -1 * (sentiment[1] / np.log(2 + row.Date.daysinmonth - row.Date.day))

		else:
			confidenceScore =  0.5 * (sentiment[2] / np.log(2 + row.Date.daysinmonth - row.Date.day))

		dataDict["ConfidenceScore"].append(confidenceScore)

	saveDF = pd.DataFrame(dataDict)
	saveDF.to_csv("monthly_confidence/" + months[monthIndex], index = False)