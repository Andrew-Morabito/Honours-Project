import pandas as pd
import numpy as np

dataframe = pd.read_csv("asx200sentiment.csv")
dataframe = dataframe[dataframe.Date != "No data for this company"]
dataframe["Date"] = pd.to_datetime(dataframe["Date"], dayfirst = True)

months = ["oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sep", "oct"]
startYear = 2022
startMonth = 10

for monthIndex in range(len(months)):
	# Reset the months for the new year
	if startMonth == 13:
		startMonth = 1
		startYear = 2023

	monthlyDF = dataframe.loc[(dataframe["Date"].dt.month == startMonth) & (dataframe["Date"].dt.year == startYear)]

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
		sentiment = [float(row.Positive), float(row.Negative), float(row.Neutral)]
		maxScore = max(sentiment)

		# Positive
		if maxScore == sentiment[0]:
			confidenceScore = sentiment[0] / np.log(2 + row.Date.daysinmonth - row.Date.day)

		# Negative
		elif maxScore == sentiment[1]:
			confidenceScore = -1 * (sentiment[1] / np.log(2 + row.Date.daysinmonth - row.Date.day))

		# Neutral
		else:
			confidenceScore =  0.5 * (sentiment[2] / np.log(2 + row.Date.daysinmonth - row.Date.day))

		dataDict["Company"].append(row.Company)
		dataDict["Date"].append(row.Date)
		dataDict["Title"].append(row.Title)
		dataDict["Positive"].append(row.Positive)
		dataDict["Negative"].append(row.Negative)
		dataDict["Neutral"].append(row.Neutral)
		dataDict["ConfidenceScore"].append(confidenceScore)

	startMonth += 1
	saveDF = pd.DataFrame(dataDict)
	saveDF.to_csv("monthly_confidence/" + months[monthIndex] + "_" + str(startYear) + ".csv", index = False)