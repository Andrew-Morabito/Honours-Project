import yfinance
import math
import pandas as pd
import numpy as np

class Portfolio:
	allocationDates = [
			["2022-10-12", "2022-10-13"], # Wednesday the 12th of Oct
			["2022-11-16", "2022-11-17"], # Wednesday the 16th of Nov
			["2022-12-14", "2022-12-15"], # Wednesday the 14th of Dec
			["2023-01-11", "2023-01-12"], # Wednesday the 11th of Jan
			["2023-02-15", "2023-02-16"], # Wednesday the 15th of Feb
			["2023-03-15", "2023-03-16"], # Wednesday the 15th of Mar
			["2023-04-12", "2023-04-13"], # Wednesday the 12th of Apr
			["2023-05-17", "2023-05-18"], # Wednesday the 17th of May
			["2023-06-14", "2023-06-15"], # Wednesday the 14th of June
			["2023-07-12", "2023-07-13"], # Wednesday the 12th of July
			["2023-08-16", "2023-08-17"], # Wednesday the 16th of Aug
			["2023-09-13", "2023-09-14"], # Wednesday the 14th of Sep
			["2023-10-18", "2023-10-19"]  # Wednesday the 18th of Oct (final sale date)
	]

	balance = 10000
	allocationAmount = 20
	allocationCount = 0
	dailyStdByMonth = []
	dailyValue = []
	monthlyValue = []

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
		stockData = pd.read_csv("stockdata_2023.csv")
		stockData = stockData.loc[stockData["Date"] == str(self.allocationDates[index][0]) + " " + "00:00:00"]
		return stockData[company]


	def getStockDataBetweenDates(self, companies, index1, index2):
		stockData = pd.read_csv("stockdata_2023.csv")
		stockData["Date"] = pd.to_datetime(stockData["Date"])
		dateRange = (stockData["Date"] >= str(self.allocationDates[index1][0])) & (stockData["Date"] <= str(self.allocationDates[index2][0]))
		stockData = stockData.loc[dateRange]
		return stockData[companies]


	def getDailyValue(self, companies):
		dailyValue = []

		for index, company in enumerate(companies["Company"]):
			companies["Company"][index] = str(company + ".AX")

		stockData = self.getStockDataBetweenDates(companies["Company"], self.allocationCount, self.allocationCount + 1)

		for index, company in enumerate(companies["Company"]):
			stockData[company] = stockData[company].mul(companies["Quantity"][index])

		for index, row in stockData.iterrows():
			self.dailyValue.append(float(row.sum()))
			dailyValue.append(float(row.sum()))
	
		return dailyValue
		

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
		stdArray = []

		for index, company in enumerate(topCompanies["Company"]):
			# Get purchase price
			stockDataBuy = self.getStockData(str(company + ".AX"), self.allocationCount)
			stockDataBuyArray.append(float(stockDataBuy))

			# Get sell price (1 month after purchase price)
			stockDataSell = self.getStockData(str(company + ".AX"), self.allocationCount + 1)
			stockDataSellArray.append(float(stockDataSell))

			# Calculate the cost and quantity to be purchased of each stock based on sentiment confidence score
			cost = allocationRatio * float(topCompanies["ConfidenceScore"][index])
			self.balance -= cost
			purchaseQuantity = cost / float(stockDataBuy)
			purchaseQuantity = round(purchaseQuantity, 3)
			purchaseQuantityArray.append(purchaseQuantity)

		topCompanies["BuyPrice"] = stockDataBuyArray
		topCompanies["SellPrice"] = stockDataSellArray
		topCompanies["Quantity"] = purchaseQuantityArray

		dailyPortValue = self.getDailyValue(topCompanies)
		dailyPortValueDF = pd.DataFrame(dailyPortValue)
		self.dailyStdByMonth.append(float(dailyPortValueDF.pct_change().std()))

		saveDF = pd.DataFrame(topCompanies)
		self.saveToCSV(saveDF, "monthly_allocations/" + month + ".csv")

		# Calculate the total selling amount for all the stocks that were purchased (sold 1 month later)
		for index, quantity in enumerate(topCompanies["Quantity"]):
			sale = quantity * float(topCompanies["SellPrice"][index])
			self.balance += sale

		self.monthlyValue.append(self.balance)

		#print(allocationRatio)
		#print(topCompanies)
		#print(self.balance)
		#print(dailyPortValue)
		#print(topCompanies["Company"])
		#print(monthlyDF)


allocationMonths = ["oct_2022", "nov_2022", "dec_2022", "jan_2023", "feb_2023", "mar_2023", 
				    "apr_2023", "may_2023", "june_2023", "july_2023", "aug_2023", "sep_2023"]

portfolio = Portfolio()

for i in range(len(allocationMonths)):
	portfolio.allocateStocks(allocationMonths[i])
	portfolio.allocationCount += 1


# Sentiment portfolio performance
mean = sum(portfolio.dailyValue) / len(portfolio.dailyValue)
roi = (portfolio.monthlyValue[-1] / 10000) - 1

dailyValuePctChange = pd.DataFrame(portfolio.dailyValue).pct_change()

stdev = 0
for i in range(len(portfolio.dailyStdByMonth)):
	stdev += portfolio.dailyStdByMonth[i]
stdev = stdev / len(portfolio.dailyStdByMonth) # Divide by the total number of months to get the average daily stdev
stdev = stdev * np.sqrt(252) # Annualise the stdev (252 trading days)

meanPctChange = float(dailyValuePctChange.sum() / len(dailyValuePctChange))
semidevArray = []

for index, row in dailyValuePctChange.iterrows():
	if float(row) < meanPctChange:
		value = (meanPctChange - float(row))**2
		semidevArray.append(value)

semidev = np.sqrt(sum(semidevArray) / len(portfolio.dailyValue)) * np.sqrt(252)

maximumDrawdown = (min(portfolio.dailyValue) - max(portfolio.dailyValue)) / max(portfolio.dailyValue)

sharpeRatio = (roi - 0.041) / stdev

print("\n")
print("Sentiment Portfolio evaluation metrics")
print("Average Return:", roi)
print("Standard deviation:", stdev)
print("Semi-deviation:", semidev)
print("Maximum drawdown:", maximumDrawdown)
print("Sharpe ratio:", sharpeRatio)
print("Monthly portfolio value:", portfolio.monthlyValue)