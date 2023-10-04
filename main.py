import yfinance
import math
import pandas as pd
import numpy as np

class Portfolio:
	allocationDates = [
			["2023-01-11", "2023-01-12"], # Wednesday the 11th of Jan
			["2023-02-15", "2023-02-16"], # Wednesday the 15th of Feb
			["2023-03-15", "2023-03-16"], # Wednesday the 15th of Mar
			["2023-04-12", "2023-04-13"], # Wednesday the 12th of Apr
			["2023-05-17", "2023-05-18"], # Wednesday the 17th of May
			["2023-06-14", "2023-06-15"], # Wednesday the 14th of June
			["2023-07-12", "2023-07-13"], # Wednesday the 12th of July
			["2023-08-16", "2023-08-17"]  # Wednesdat the 16th of August (final sale date)
	]

	balance = 10000
	allocationAmount = 20
	allocationCount = 0

	def __init__(self):
		self.balance = 10000
		self.allocationCount = 0


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
					dataDict["ConfidenceScore"][companyCount - 1] = dataDict["ConfidenceScore"][companyCount - 1] / companyOccurrences
					companyOccurrences = 0
					companyCount += 1

		return dataDict


	def getTopCompanies(self, dataframe):
		dataDict = {
			"Company": [],
			"ConfidenceScore": []
		}

		counter = 0
		for index, row in dataframe.iterrows():
			if counter < self.allocationAmount:
				dataDict["Company"].append(row.Company)
				dataDict["ConfidenceScore"].append(float(row.ConfidenceScore))
				counter += 1

			else:
				break

		return dataDict

	def getStockData(self, company, index):
		ticker = yfinance.Ticker(company)
		stockData = ticker.history(start = self.allocationDates[index][0], end = self.allocationDates[index][1])
		#stockData = yfinance.download(tickers, start = self.allocationDates[index][0], end = self.allocationDates[index][1])
		return stockData


	def allocateStocks(self, month):
		dataDict = self.getTotalConfidenceScore(month)
		monthlyDF = pd.DataFrame(dataDict)
		self.saveToCSV(monthlyDF, "monthly_confidence/" + month + "_collated.csv")

		monthlyDF = monthlyDF.sort_values(by = ["ConfidenceScore"], ascending = False)
		topCompanies = self.getTopCompanies(monthlyDF)

		# Get the sum of all the confidence scores to find the allocation ratio
		allocationRatio = 0
		for score in topCompanies["ConfidenceScore"]:
			allocationRatio += score
		allocationRatio = math.floor(self.balance / allocationRatio)

		# Fetch stock data
		stockDataBuyArray = []
		stockDataSellArray = []
		purchaseQuantityArray = []
		for index, company in enumerate(topCompanies["Company"]):
			# Get purchase price
			stockDataBuy = self.getStockData(str(company + ".AX"), self.allocationCount)
			stockDataBuyArray.append(float(stockDataBuy.Open))

			# Get sell price (1 month after purchase price)
			stockDataSell = self.getStockData(str(company + ".AX"), self.allocationCount + 1)
			stockDataSellArray.append(float(stockDataSell.Open))

			# Calculate the cost and quantity to be purchased of each stock based on sentiment confidence score
			cost = allocationRatio * float(topCompanies["ConfidenceScore"][index])
			self.balance -= cost
			purchaseQuantity = cost / float(stockDataBuy.Open)
			purchaseQuantity = round(purchaseQuantity, 3)
			purchaseQuantityArray.append(purchaseQuantity)

		topCompanies["BuyPrice"] = stockDataBuyArray
		topCompanies["SellPrice"] = stockDataSellArray
		topCompanies["Quantity"] = purchaseQuantityArray
		saveDF = pd.DataFrame(topCompanies)
		self.saveToCSV(saveDF, "monthly_allocations/" + month + ".csv")

		# Calculate the total selling amount for all the stocks that were purchased (sold 1 month later)
		for index, quantity in enumerate(topCompanies["Quantity"]):
			sale = quantity * float(topCompanies["SellPrice"][index])
			self.balance += sale

		print(allocationRatio)
		print(topCompanies)
		print(self.balance)
		#print(topCompanies)
		#print(monthlyDF)


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
	"""
	def reallocate(self, month):
		dataDict = self.getTotalConfidenceScore(month)
		monthlyDF = pd.DataFrame(dataDict)
		self.saveToCSV(monthlyDF, "monthly_confidence/" + month + "_collated.csv")"""

allocationMonths = ["jan", "feb", "mar", "apr", "may", "june", "july"]

portfolio = Portfolio()

for i in range(len(allocationMonths)):
	portfolio.allocateStocks(allocationMonths[i])
	portfolio.allocationCount += 1

"""
ticker = yfinance.Ticker("CBA.AX")
print(ticker.history(start = "2023-01-11", end = "2023-01-12"))
print("CBA" + ".AX")
portfolio = Portfolio()
print(portfolio.balance)
"""