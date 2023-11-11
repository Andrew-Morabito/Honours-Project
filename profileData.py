import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataframe = pd.read_csv("asx200data.csv")
# Drop all the companies that have no data for them.
dataframe = dataframe[dataframe.Date != "No data for this company"]
print("Number of entries after removing null companies:", len(dataframe))

averageHeadlineLength = dataframe["Title"].apply(lambda row: min(len(row.split(" ")), len(row)) if isinstance(row, str) else None)
print("Average headline length:", averageHeadlineLength.mean())
averageHeadlineLengthValue = []
for index, value in enumerate(averageHeadlineLength):
	averageHeadlineLengthValue.append(value)

# Headlines length boxplot
fig = plt.figure(figsize = (5, 5))
plt.boxplot(averageHeadlineLengthValue, vert = True, patch_artist = True, labels = ["Headlines"], widths = 0.5)
plt.ylabel("Headline Length")
plt.title("Length of News Headlines")
plt.show()

#wordFreq = dataframe["Title"].str.split(expand = True).stack().value_counts()

companyFreq = dataframe["Company"].value_counts()
print(companyFreq.head(10))
companyFreqValue = []
for index, value in enumerate(companyFreq):
	companyFreqValue.append(value)

# Company frequency boxplot
fig = plt.figure(figsize = (5, 5))
plt.boxplot(companyFreqValue, vert = True, patch_artist = True, labels = ["ASX"], widths = 0.5)
plt.ylabel("Frequency")
plt.title("Frequency of News Headlines by Company")
plt.show()

# Highest news headlines count bar chart
fig, ax = plt.subplots()
labels = ["NCM", "BHP", "AMC", "DMP", "QAN", "ORG", "RIO", "RMD","WBC", "MQG"]
ax.bar(labels, companyFreqValue[:10])
ax.set_ylabel("News Headlines")
ax.set_title("Companies with the highest count of News Headlines")
plt.show()

# Headline count per month
dataframe["Date"] = pd.to_datetime(dataframe["Date"], dayfirst = True)
headlineCountMonth = dataframe.groupby(pd.Grouper(key = "Date", axis = 0, freq = "M")).agg({"count"})
headlineCountMonthValue = []
for index, value in headlineCountMonth["Company"].iterrows():
	headlineCountMonthValue.append(float(value))

print(headlineCountMonthValue)
fig, ax = plt.subplots()
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
ax.barh(labels, headlineCountMonthValue[1:14])
ax.invert_yaxis()
ax.set_xlabel("News Headlines")
ax.set_title("News Headlines count by Month")
plt.show()

# Sentiment portfolio pct change graph
monthlyValue = [10000, 10489.239144629835, 10870.789795372873, 10913.889110465589, 10910.672575798306, 10729.027526433103, 11183.850785329187, 11445.838920084658, 11357.420990581133, 11587.470701758572, 11958.092486728447, 11954.939831924596, 12108.032293092447]
pctChange = []
for i in range(len(monthlyValue)):
	if i == 0:
		pctChange.append(0.0)

	else:
		change = (monthlyValue[i] / monthlyValue[i - 1]) - 1
		pctChange.append(change)
print(pctChange)

fig, ax = plt.subplots(figsize = (8,8))
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
ax.plot(pctChange, "o-r")
ax.set_ylabel("Percent Change")
ax.set_ylim(-0.08, 0.08)
ax.grid(True)
ax.set_title("Sentiment Portfolio percent change by Month")
plt.xticks(x, labels, rotation = "vertical")
plt.margins(0.1)
plt.subplots_adjust(bottom = 0.25)
plt.show()

# Maximum Sharpe portfolio pct change graph
monthlyValue = [10000, 10267.297476731595, 10031.122717102075, 9904.335846947413, 9969.240817417964, 9616.737615587943, 9999.802091080406, 10534.988013248581, 10342.158992820277, 10558.079491611534, 10676.510054380557, 10646.07328506669, 10587.763522694328]
pctChange = []
for i in range(len(monthlyValue)):
	if i == 0:
		pctChange.append(0.0)

	else:
		change = (monthlyValue[i] / monthlyValue[i - 1]) - 1
		pctChange.append(change)
print(pctChange)

fig, ax = plt.subplots(figsize = (8,8))
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
ax.plot(pctChange, "o-r")
ax.set_ylabel("Percent Change")
ax.set_ylim(-0.08, 0.08)
ax.grid(True)
ax.set_title("Maximum Sharpe Ratio Portfolio percent change by Month")
plt.xticks(x, labels, rotation = "vertical")
plt.margins(0.1)
plt.subplots_adjust(bottom = 0.25)
plt.show()

# Equally Weighted portfolio pct change graph
monthlyValue = [10000, 10351.896852319216, 10621.370200933598, 10744.12849994217, 10919.443696854101, 10695.609068180598, 11134.838082760278, 11191.758648848174, 10961.339545057548, 11231.536747094207, 11332.712146902964, 11166.583618475928, 10917.339641273778]
pctChange = []
for i in range(len(monthlyValue)):
	if i == 0:
		pctChange.append(0.0)

	else:
		change = (monthlyValue[i] / monthlyValue[i - 1]) - 1
		pctChange.append(change)
print(pctChange)

fig, ax = plt.subplots(figsize = (8,8))
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
ax.plot(pctChange, "o-r")
ax.set_ylabel("Percent Change")
ax.set_ylim(-0.08, 0.08)
ax.grid(True)
ax.set_title("Equally Weighted Portfolio percent change by Month")
plt.xticks(x, labels, rotation = "vertical")
plt.margins(0.1)
plt.subplots_adjust(bottom = 0.25)
plt.show()

# ASX 200 Market Index pct change graph
monthlyValue = [10000, 10529.221218033095, 10794.283565250094, 10824.068905133508, 11182.700557070326, 10693.944798326438, 11017.826397376833, 10932.079876128244, 10773.524174971793, 10901.692218644226, 11041.895596323806, 10819.555930330951, 10591.350278535163]
pctChange = []
for i in range(len(monthlyValue)):
	if i == 0:
		pctChange.append(0.0)

	else:
		change = (monthlyValue[i] / monthlyValue[i - 1]) - 1
		pctChange.append(change)
print(pctChange)

fig, ax = plt.subplots(figsize = (8,8))
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
labels = ["Oct 2022", "Nov 2022", "Dec 2022", "Jan", "Feb", "Mar", "Apr", "May","June", "July", "Aug", "Sep", "Oct"]
ax.plot(pctChange, "o-r")
ax.set_ylabel("Percent Change")
ax.set_ylim(-0.08, 0.08)
ax.grid(True)
ax.set_title("ASX 200 Market Index percent change by Month")
plt.xticks(x, labels, rotation = "vertical")
plt.margins(0.1)
plt.subplots_adjust(bottom = 0.25)
plt.show()