import yfinance
import pandas as pd

tickers = ['A2M.AX', 'AAA.AX', 'ABC.AX', 'ABP.AX', 'AFI.AX', 'AGL.AX', 'AIA.AX', 'ALD.AX', 'ALL.AX', 'ALQ.AX', 
		   'ALU.AX', 'ALX.AX', 'AMC.AX', 'AMP.AX', 'ANN.AX', 'ANZ.AX', 'APA.AX', 'APE.AX', 'APT.AX', 'APX.AX', 
		   'ARB.AX', 'ARG.AX', 'AST.AX', 'ASX.AX', 'AWC.AX', 'AZJ.AX', 'BAP.AX', 'BEN.AX', 'BGA.AX', 'BHP.AX', 
		   'BIN.AX', 'BKW.AX', 'BLD.AX', 'BOQ.AX', 'BPT.AX', 'BRG.AX', 'BSL.AX', 'BWP.AX', 'BXB.AX', 'CAR.AX', 
		   'CBA.AX', 'CCL.AX', 'CCP.AX', 'CDA.AX', 'CGF.AX', 'CHC.AX', 'CHN.AX', 'CIA.AX', 'CIM.AX', 'CLW.AX', 
		   'CMW.AX', 'CNU.AX', 'COH.AX', 'COL.AX', 'CPU.AX', 'CQR.AX', 'CSL.AX', 'CSR.AX', 'CTD.AX', 'CWN.AX', 
		   'CWY.AX', 'DEG.AX', 'DHG.AX', 'DMP.AX', 'DOW.AX', 'DRR.AX', 'DXS.AX', 'EBO.AX', 'ELD.AX', 'EML.AX', 
		   'EVN.AX', 'EVT.AX', 'FBU.AX', 'FLT.AX', 'FMG.AX', 'FPH.AX', 'GMG.AX', 'GNE.AX', 'GOZ.AX', 'GPT.AX', 
		   'GXY.AX', 'HLS.AX', 'HVN.AX', 'IAG.AX', 'IEL.AX', 'IFL.AX', 'IFT.AX', 'IGO.AX', 'ILU.AX', 'IOO.AX', 
		   'IOZ.AX', 'IPL.AX', 'IRE.AX', 'IVV.AX', 'JBH.AX', 'JHX.AX', 'LFG.AX', 'LFS.AX', 'LLC.AX', 'LNK.AX', 
		   'LYC.AX', 'MCY.AX', 'MEZ.AX', 'MFG.AX', 'MGF.AX', 'MGOC.AX', 'MGR.AX', 'MIN.AX', 'MLT.AX', 'MP1.AX', 
		   'MPL.AX', 'MQG.AX', 'MTS.AX', 'NAB.AX', 'NCM.AX', 'NEC.AX', 'NHF.AX', 'NIC.AX', 'NSR.AX', 'NST.AX', 
		   'NUF.AX', 'NWL.AX', 'NXT.AX', 'ORA.AX', 'ORE.AX', 'ORG.AX', 'ORI.AX', 'OSH.AX', 'OZL.AX', 'PBH.AX', 
		   'PDL.AX', 'PLS.AX', 'PME.AX', 'PMGOLD.AX', 'PMV.AX', 'PNI.AX', 'PNV.AX', 'PPT.AX', 'PTM.AX', 'QAN.AX', 
		   'QBE.AX', 'QUB.AX', 'REA.AX', 'REH.AX', 'RHC.AX', 'RIO.AX', 'RMD.AX', 'RRL.AX', 'RWC.AX', 'S32.AX', 
		   'SCG.AX', 'SCP.AX', 'SDF.AX', 'SEK.AX', 'SGM.AX', 'SGP.AX', 'SGR.AX', 'SHL.AX', 'SKC.AX', 'SKI.AX', 
		   'SLK.AX', 'SNZ.AX', 'SOL.AX', 'SPK.AX', 'STO.AX', 'STW.AX', 'SUL.AX', 'SUN.AX', 'SVW.AX', 'SYD.AX', 
		   'TAH.AX', 'TCL.AX', 'TLS.AX', 'TLT.AX', 'TNE.AX', 'TPG.AX', 'TWE.AX', 'TYR.AX', 'VAP.AX', 'VAS.AX', 
		   'VCX.AX', 'VEA.AX', 'VEU.AX', 'VGS.AX', 'VOC.AX', 'VTS.AX', 'VUK.AX', 'WAM.AX', 'WBC.AX', 'WEB.AX', 
		   'WES.AX', 'WOR.AX', 'WOW.AX', 'WPL.AX', 'WPR.AX', 'WTC.AX', 'XRO.AX', 'YAL.AX', 'Z1P.AX', 'ZIM.AX', 
		   'WDS.AX', 'TLC.AX', 'EDV.AX', 'WHC.AX', 'AKE.AX', 'NHC.AX', 'GQG.AX', 'QUAL.AX', 'LTR.AX', 'WBCPJ.AX',
		   'SMR.AX', 'NDQ.AX', 'A200.AX', 'GOLD.AX', 'PDN.AX', 'VHY.AX', 'CRN.AX', 'AUB.AX', 'TLX.AX', 'AVZ.AX', 
		   'SFR.AX', 'HUB.AX', 'ETHI.AX', 'NABPH.AX', 'VGAD.AX', 'BFL.AX', 'RGN.AX', 'VNT.AX', 'PRU.AX', 'HDN.AX', 
		   'HYGG.AX', 'SQ2.AX', 'HBRD.AX', 'AIZ.AX', 'PXA.AX', 'NABPI.AX', 'LOV.AX', 'GOR.AX', 'IAF.AX', 'VDHG.AX', 
		   'DDR.AX', 'NABPF.AX', 'APM.AX', 'RMS.AX', 'MVW.AX', 'CIP.AX', 'CEN.AX', 'IVC.AX', 'CBAPL.AX', 'MXT.AX']

stockData = yfinance.download(tickers, start = "2022-10-12", end = "2023-10-19")["Adj Close"]
stockData = stockData.dropna(axis = "columns", how = "all")
stockData.to_csv("stockdata_2023.csv")
print(stockData)