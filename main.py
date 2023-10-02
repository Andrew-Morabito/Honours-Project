import yfinance
import pandas as pd
import numpy as np

class Portfolio:
	balance = 10000

	def __init__(self):
		self.balance = 10000

	def saveToCSV(self, dataframe, saveLocation):
		dataframe.to_csv(saveLocation, index = False)

	def getTotalConfidenceScore(self, month):
		dataframe = pd.read_csv("monthly_confidence/" + month + ".csv")

		dataDict = {
			"Company": [],
			"ConfidenceScore": []
		}

		companyCount = 0
		companyOccurrences = 0

		for index, row in dataframe.iterrows():
			companyOccurrences += 1

			if index == 0:
				dataDict["Company"].append(row.Company)
				dataDict["ConfidenceScore"].append(float(row.ConfidenceScore))
				companyCount += 1

			else:
				if dataDict["Company"][companyCount - 1] == row.Company:
					dataDict["ConfidenceScore"][companyCount - 1] += float(row.ConfidenceScore)
					companyOccurrences += 1

				else:
					dataDict["Company"].append(row.Company)
					dataDict["ConfidenceScore"].append(float(row.ConfidenceScore))
					dataDict["ConfidenceScore"][companyCount - 1] = (dataDict["ConfidenceScore"][companyCount - 1]) / companyOccurrences
					companyOccurrences = 0
					companyCount += 1

		return dataDict

	def getTopCompanies(self, dataDict):
		print("A")

	def initialAllocation(self, startDate, endDate, month):
		dataDict = self.getTotalConfidenceScore(month)
		monthlyDF = pd.DataFrame(dataDict)
		self.saveToCSV(monthlyDF, "monthly_confidence/" + month + "_collated.csv")

		monthlyDF = monthlyDF.sort_values(by = ["ConfidenceScore"], ascending = False)
		print(monthlyDF)


		"""
		test = np.array(dataDict["ConfidenceScore"])
		indices = np.argpartition(test, -10)[-10:]
		print(dataDict)
		print(indices)
		indices = list(indices)
		print(indices)

		for i in list(indices):
			print(dataDict["Company"][i] + ", " + str(dataDict["ConfidenceScore"][i]))
		"""

	def reallocate(self, startDate, endDate, month):
		dataDict = self.getTotalConfidenceScore(month)
		monthlyDF = pd.DataFrame(dataDict)
		self.saveToCSV(monthlyDF, "monthly_confidence/" + month + "_collated.csv")

allocationDates = [
		["2023-01-11", "2023-01-12"], # Wednesday the 11th of Jan
		["2023-02-15", "2023-02-16"], # Wednesday the 15th of Feb
		["2023-03-15", "2023-03-16"], # Wednesday the 15th of Mar
		["2023-04-12", "2023-04-13"], # Wednesday the 12th of Apr
		["2023-05-17", "2023-05-18"], # Wednesday the 17th of May
		["2023-06-14", "2023-06-15"], # Wednesday the 14th of June
		["2023-07-12", "2023-07-13"]  # Wednesday the 12th of July
]

allocationMonths = ["jan", "feb", "mar", "apr", "may", "june", "july"]

portfolio = Portfolio()

for i in range(allocationMonths.len()):
	if i == 0:
		portfolio.initialAllocation(allocationDates[i][0], allocationDates[i][1], allocationMonths[i])

	else:
		portfolio.reallocate(allocationDates[i][0], allocationDates[i][1], allocationMonths[i])

"""
ticker = yfinance.Ticker("CBA.AX")
print(ticker.history(start = "2023-01-11", end = "2023-01-12").Low)
print("CBA" + ".AX")

portfolio = Portfolio()
print(portfolio.balance)
"""