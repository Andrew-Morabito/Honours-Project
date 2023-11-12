import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pypfopt import objective_functions
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

def getMaxSharpeAllocation(initialInvestment):
	stockData = pd.read_csv("stockdata_2021&2022.csv", parse_dates = True, index_col = "Date")
	expectedReturns = mean_historical_return(stockData)
	shrinkage = CovarianceShrinkage(stockData).ledoit_wolf()

	ef = EfficientFrontier(expectedReturns, shrinkage, weight_bounds = (0, 1))
	ef.add_objective(objective_functions.L2_reg, gamma = 5)
	weights = ef.max_sharpe(risk_free_rate = 0.041)
	cleaned_weights = ef.clean_weights()

	dataDict = {
		"Company": [],
		"Allocation": [],
		"Quantity": []
	}

	stockData = pd.read_csv("stockdata_2023.csv")
	stockData["Date"] = pd.to_datetime(stockData["Date"])
	stockData = stockData.loc[stockData["Date"] == "2022-10-12"]

	for key, weight in cleaned_weights.items():
		if weight > 0:
			dataDict["Company"].append(key)
			dataDict["Allocation"].append(weight)

			stockQuantity = (initialInvestment * weight) / float(stockData[key])
			dataDict["Quantity"].append(stockQuantity)

	return dataDict


def getEqualWeightedAllocation(initialInvestment):
	stockData = pd.read_csv("stockdata_2023.csv")
	stockData["Date"] = pd.to_datetime(stockData["Date"])
	stockData = stockData.loc[stockData["Date"] == "2022-10-12"]

	allocationRatio = 1 / len(stockData.axes[1])

	dataDict = {
		"Company": [],
		"Allocation": [],
		"Quantity": []
	}

	for i in range(len(stockData.axes[1]) - 1):
		dataDict["Company"].append(str(stockData.columns[i + 1]))
		dataDict["Allocation"].append(allocationRatio)

		stockQuantity = (initialInvestment * allocationRatio) / float(stockData[dataDict["Company"][i]])
		dataDict["Quantity"].append(stockQuantity)

	return dataDict


def getMarketIndexValue(initialInvestment):
	stockData = pd.read_csv("marketIndex.csv")
	stockData["Date"] = pd.to_datetime(stockData["Date"])
	stockData = stockData.loc[stockData["Date"] == "2022-10-12"]

	quantity = initialInvestment / float(stockData["Adj Close"])

	stockData = pd.read_csv("marketIndex.csv")
	dailyValue = []
	monthlyValue = []

	dayCounter = 0
	for index, row in stockData.iterrows():
		dailyValue.append(quantity * float(row["Adj Close"]))
		dayCounter += 1

		# Getting the monthly value of the portfolio
		if dayCounter == 252 / 12:
			monthlyValue.append(quantity * float(row["Adj Close"]))
			dayCounter = 0

	return [dailyValue, monthlyValue]


def getPortfolioValue(allocationWeights):
	stockData = pd.read_csv("stockdata_2023.csv")
	stockData = stockData[allocationWeights["Company"]]

	dailyValue = []
	monthlyValue = []

	for index, company in enumerate(allocationWeights["Company"]):
		stockData[company] = stockData[company].mul(allocationWeights["Quantity"][index])

	dayCounter = 0
	for index, row in stockData.iterrows():
		dailyValue.append(row.sum())
		dayCounter += 1

		# Getting the monthly value of the portfolio
		if dayCounter == 252 / 12:
			monthlyValue.append(row.sum())
			dayCounter = 0

	return [dailyValue, monthlyValue]


sharpeWeights = getMaxSharpeAllocation(initialInvestment = 10000)
equalWeights = getEqualWeightedAllocation(initialInvestment = 10000)
marketIndex = getMarketIndexValue(initialInvestment = 10000)


# Maximum Sharpe ratio portfolio (out-of-sample) performance
sharpePortfolio = getPortfolioValue(sharpeWeights) # [0] is daily value, [1] is monthly value
roi = (sharpePortfolio[1][-1] / 10000) - 1

sharpePortfolioDF = pd.DataFrame(sharpePortfolio[0]).pct_change()
stdev = float(sharpePortfolioDF.std()) * np.sqrt(252)

meanPctChange = float(sharpePortfolioDF.sum() / len(sharpePortfolioDF))
semidevArray = []
for index, row in sharpePortfolioDF.iterrows():
	if float(row) < meanPctChange:
		value = (meanPctChange - float(row))**2
		semidevArray.append(value)
semidev = np.sqrt(sum(semidevArray) / len(sharpePortfolio[0])) * np.sqrt(252)

maximumDrawdown = (min(sharpePortfolio[0]) - max(sharpePortfolio[0])) / max(sharpePortfolio[0])

sharpeRatio = (roi - 0.041) / stdev

print("\n")
print("Maximum Sharpe Ratio Portfolio")
print("Average Return:", roi)
print("Standard deviation:", stdev)
print("Semi-deviation:", semidev)
print("Maximum drawdown:", maximumDrawdown)
print("Sharpe ratio:", sharpeRatio)
print("Monthly portfolio value:", sharpePortfolio[1])

# Equal weighted portfolio performance
equalPortfolio = getPortfolioValue(equalWeights) # [0] is daily value, [1] is monthly value

roi = (equalPortfolio[1][-1] / 10000) - 1

equalPortfolioDF = pd.DataFrame(equalPortfolio[0]).pct_change()
stdev = float(equalPortfolioDF.std()) * np.sqrt(252)

meanPctChange = float(equalPortfolioDF.sum() / len(equalPortfolioDF))
semidevArray = []
for index, row in equalPortfolioDF.iterrows():
	if float(row) < meanPctChange:
		value = (meanPctChange - float(row))**2
		semidevArray.append(value)
semidev = np.sqrt(sum(semidevArray) / len(equalPortfolio[0])) * np.sqrt(252)

maximumDrawdown = (min(equalPortfolio[0]) - max(equalPortfolio[0])) / max(equalPortfolio[0])

sharpeRatio = (roi - 0.041) / stdev

print("\n")
print("Equal Weighted Portfolio")
print("Average Return:", roi)
print("Standard deviation:", stdev)
print("Semi-deviation:", semidev)
print("Maximum drawdown:", maximumDrawdown)
print("Sharpe ratio:", sharpeRatio)
print("Monthly portfolio value:", equalPortfolio[1])


# Market Index performance
roi = (marketIndex[1][-1] / 10000) - 1

marketIndexDF = pd.DataFrame(marketIndex[0]).pct_change()
stdev = float(marketIndexDF.std()) * np.sqrt(252)

meanPctChange = float(marketIndexDF.sum() / len(marketIndexDF))
semidevArray = []
for index, row in marketIndexDF.iterrows():
	if float(row) < meanPctChange:
		value = (meanPctChange - float(row))**2
		semidevArray.append(value)
semidev = np.sqrt(sum(semidevArray) / len(marketIndex[0])) * np.sqrt(252)

maximumDrawdown = (min(marketIndex[0]) - max(marketIndex[0])) / max(marketIndex[0])

sharpeRatio = (roi - 0.041) / stdev

print("\n")
print("Market Index")
print("Average Return:", roi)
print("Standard deviation:", stdev)
print("Semi-deviation:", semidev)
print("Maximum drawdown:", maximumDrawdown)
print("Sharpe ratio:", sharpeRatio)
print("Monthly portfolio value:", marketIndex[1])

# Plotting the cumulative sum
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
index = [0, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5, 21.5]
index = np.cumsum(index)
x = (1 + sharpePortfolioDF).cumprod() - 1
y = (1 + equalPortfolioDF).cumprod() - 1
z = (1 + marketIndexDF).cumprod() - 1
sentimentPort = pd.read_csv("sentiment_DVC.csv")
sentimentPort = (1 + sentimentPort).cumprod() - 1

fig = plt.figure(figsize = (10, 10))
plt.ylabel("Percent Change")
plt.title("Daily Cumulatve Returns")
plt.plot(sentimentPort, label = "Sentiment Portfolio")
plt.plot(x, label = "Maximum Sharpe Ratio Portfolio")
plt.plot(y, label = "Equally Weighted Portfolio")
plt.plot(z, label = "ASX 200")
plt.xticks(index, labels, rotation = "vertical")
plt.margins(0.1)
plt.legend(loc="upper left")
plt.subplots_adjust(bottom = 0.25)
plt.show()