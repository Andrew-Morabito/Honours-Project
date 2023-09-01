import json
import feedparser
import pandas as pd
import csv
from datetime import datetime

# ASX 200 ticker references for Yahoo Finance.
tickers = ["A2M.AX", "AAA.AX", "ABC.AX", "ABP.AX", "AFI.AX", "AGL.AX", "AIA.AX", "ALD.AX",
		   "ALL.AX", "ALQ.AX", "ALU.AX", "ALX.AX", "AMC.AX", "AMP.AX", "ANN.AX", "ANZ.AX",
		   "APA.AX", "APE.AX", "APT.AX", "APX.AX", "ARB.AX", "ARG.AX", "AST.AX", "ASX.AX",
		   "AWC.AX", "AZJ.AX", "BAP.AX", "BEN.AX", "BGA.AX", "BHP.AX", "BIN.AX", "BKW.AX",
		   "BLD.AX", "BOQ.AX", "BPT.AX", "BRG.AX", "BSL.AX", "BWP.AX", "BXB.AX", "CAR.AX",
		   "CBA.AX", "CCL.AX", "CCP.AX", "CDA.AX", "CGF.AX", "CHC.AX", "CHN.AX", "CIA.AX",
		   "CIM.AX", "CLW.AX", "CMW.AX", "CNU.AX", "COH.AX", "COL.AX", "CPU.AX", "CQR.AX",
		   "CSL.AX", "CSR.AX", "CTD.AX", "CWN.AX", "CWY.AX", "DEG.AX", "DHG.AX", "DMP.AX",
		   "DOW.AX", "DRR.AX", "DXS.AX", "EBO.AX", "ELD.AX", "EML.AX", "EVN.AX", "EVT.AX",
		   "FBU.AX", "FLT.AX", "FMG.AX", "FPH.AX", "GMG.AX", "GNE.AX", "GOZ.AX", "GPT.AX",
		   "GXY.AX", "HLS.AX", "HVN.AX", "IAG.AX", "IEL.AX", "IFL.AX", "IFT.AX", "IGO.AX",
		   "ILU.AX", "IOO.AX", "IOZ.AX", "IPL.AX", "IRE.AX", "IVV.AX", "JBH.AX", "JHX.AX",
		   "LFG.AX", "LFS.AX", "LLC.AX", "LNK.AX", "LYC.AX", "MCY.AX", "MEZ.AX", "MFG.AX",
		   "MGF.AX", "MGOC.AX", "MGR.AX", "MIN.AX", "MLT.AX", "MP1.AX", "MPL.AX", "MQG.AX",
		   "MTS.AX", "NAB.AX", "NCM.AX", "NEC.AX", "NHF.AX", "NIC.AX", "NSR.AX", "NST.AX",
		   "NUF.AX", "NWL.AX", "NXT.AX", "ORA.AX", "ORE.AX", "ORG.AX", "ORI.AX", "OSH.AX",
		   "OZL.AX", "PBH.AX", "PDL.AX", "PLS.AX", "PME.AX", "PMGOLD.AX", "PMV.AX", "PNI.AX",
		   "PNV.AX", "PPT.AX", "PTM.AX", "QAN.AX", "QBE.AX", "QUB.AX", "REA.AX", "REH.AX",
		   "RHC.AX", "RIO.AX", "RMD.AX", "RRL.AX", "RWC.AX", "S32.AX", "SCG.AX", "SCP.AX",
		   "SDF.AX", "SEK.AX", "SGM.AX", "SGP.AX", "SGR.AX", "SHL.AX", "SKC.AX", "SKI.AX",
		   "SLK.AX", "SNZ.AX", "SOL.AX", "SPK.AX", "STO.AX", "STW.AX", "SUL.AX", "SUN.AX",
		   "SVW.AX", "SYD.AX", "TAH.AX", "TCL.AX", "TLS.AX", "TLT.AX", "TNE.AX", "TPG.AX",
		   "TWE.AX", "TYR.AX", "VAP.AX", "VAS.AX", "VCX.AX", "VEA.AX", "VEU.AX", "VGS.AX",
		   "VOC.AX", "VTS.AX", "VUK.AX", "WAM.AX", "WBC.AX", "WEB.AX", "WES.AX", "WOR.AX",
		   "WOW.AX", "WPL.AX", "WPR.AX", "WTC.AX", "XRO.AX", "YAL.AX", "Z1P.AX", "ZIM.AX"]

# Dictionary for storing data before converting to a DataFrame.
dataDict = {
	"Company": [],
	"Date": [],
	"Title": []
}

# Request header for accessing Yahoo Finance services.
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

# Retrieve data.
for ticker in tickers:
	RSSfeed = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US" % ticker
	newsfeed = feedparser.parse(RSSfeed)
	company = ticker.split(".")[0]

	# Checking if any data actually exists for the company.
	try:
		checkEntries = newsfeed.entries[0]

		for entry in newsfeed.entries:
			date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").strftime("%d/%m/%Y")
			title = '"{}"'.format(entry.title)

			dataDict["Company"].append(company)
			dataDict["Date"].append(date)
			dataDict["Title"].append(title)

	# If no	data.	
	except IndexError:
		date = "No data for this company"
		title = '"' + "No data for this company" +'"'

		dataDict["Company"].append(company)
		dataDict["Date"].append(date)
		dataDict["Title"].append(title)

dataframe = pd.DataFrame(dataDict)

dataframe.to_csv("asx200data.csv", index = False)