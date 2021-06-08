import pandas as pd
import numpy as np
import os
import pickle
import commonFunctions as cf
from datetime import date
from dateutil.rrule import rrule, DAILY
import sys

def convertDate(row):
	if(len(row) == 8):
		return pd.to_datetime(row, format = '%m/%d/%y')
	else:
		return pd.to_datetime(row, format = '%Y-%m-%d')


dataFolder = 'air-pollution/'
stateCode='Others'
masterFolder= cf.makeDir(stateCode)
masterFolder = cf.makeDir(stateCode + '/' +'Data')

#chemicals = ['co','no2','o3','pm25','so2']
chemicals = ['o3']
#colNames = {'co': 'Daily Max 8-hour CO Concentration', 'no2': 'Daily Max 1-hour NO2 Concentration', 'o3': 'Daily Max 8-hour Ozone Concentration' , 'pm25': 'Daily Mean PM2.5 Concentration', 'so2': 'Daily Max 1-hour SO2 Concentration'}

colNames = {'o3':'1st Max Value'}
#years =["1980","1985","1990","1995","2000","2005","2010","2015","2017"]
years = [str(i) for i in range(1980,2018)]
# years=['1990']


try:
	locations = pickle.load(open('./locations.pickle','rb'))
except:
	locations={}


for chem in chemicals:

	chemicalDir = cf.makeDir(masterFolder + '/' + chem)
	cf.makeDir( stateCode+'/Correlations')
	cf.makeDir( stateCode+'/Correlations/' + chem)
	for year in years:
		print(chem,year)
		cf.makeDir( stateCode+'/Correlations/' + chem + '/' + year)
		yearDir = cf.makeDir(chemicalDir + '/' + year)
		
		data = pd.read_csv(dataFolder + 'daily_44201_' + year + '.csv')
		
		
		data=data[data['State Code'].astype(str)!='CC']
		data['State Code']=data['State Code'].astype(int)
		if year=='2001':
			print(data['State Code'].unique())

		#data=data[data['State Code']==int(stateCode)]

		# East North Coast
		# statesCodes=[9,10,23,24,25,34,36,42,44,50,11]
		# data=data[(data['State Code']==statesCodes[0]) | (data['State Code']==statesCodes[1]) | \
		# (data['State Code']==statesCodes[2]) | (data['State Code']==statesCodes[3]) | \
		# (data['State Code']==statesCodes[4]) | (data['State Code']==statesCodes[5]) | \
		# (data['State Code']==statesCodes[6]) | (data['State Code']==statesCodes[7]) | \
		# (data['State Code']==statesCodes[8]) | (data['State Code']==statesCodes[9]) |
		# (data['State Code']==statesCodes[10])
		# ]

		# WC
		# statesCodes=[53,6,41]
		# data=data[(data['State Code']==statesCodes[0]) | (data['State Code']==statesCodes[1]) | \
		# (data['State Code']==statesCodes[2])  ]

		# Others
		stateCodesA=[6,53,41]
		stateCodesB=[9,10,23,24,25,34,36,42,44,50,11]
		statesCodes=stateCodesA+stateCodesB
		data=data[(data['State Code']!=statesCodes[0]) & (data['State Code']!=statesCodes[1]) & \
		(data['State Code']!=statesCodes[2]) & (data['State Code']!=statesCodes[3]) & \
		(data['State Code']!=statesCodes[4]) & (data['State Code']!=statesCodes[5]) & \
		(data['State Code']!=statesCodes[6]) & (data['State Code']!=statesCodes[7]) & \
		(data['State Code']!=statesCodes[8]) & (data['State Code']!=statesCodes[9]) & \
		(data['State Code']!=statesCodes[10]) & (data['State Code']!=statesCodes[11]) & \
		(data['State Code']!=statesCodes[12]) & (data['State Code']!=statesCodes[13])
		 ]

		data['SiteConCat'] = data['State Code'].astype(str) +'-'+data['County Code'].astype(str) +'-'+ data['Site Num'].astype(str)

		sites = data['SiteConCat'].unique()
		for site in sites:
			

			siteWiseData = data[data['SiteConCat'] == site]
			#print(siteWiseData.keys())
			siteWiseData['Date Local'] = siteWiseData['Date Local'].apply(lambda row: convertDate(row))
			try:
			#print(siteWiseData.keys())
				locations[site] = [siteWiseData.Latitude.unique()[0],siteWiseData.Longitude.unique()[0]]
			except:
				pass
			# 	print("fail")
			    
			a = date(int(year),1,1)
			b = date(int(year),12,31)
			timeSeriesData = []
			for dt in rrule(DAILY, dtstart=a, until=b):
				dateData = siteWiseData[siteWiseData['Date Local'] == dt]
				if(dateData.shape[0] == 0):
					timeSeriesData.append('-')
				else:
					timeSeriesData.append(dateData[colNames[chem]].mean())
			print(site, len(timeSeriesData))
			with open(yearDir + '/' + str(site) + '.pickle','wb') as f:
				pickle.dump(timeSeriesData, f)

with open('./locations.pickle','wb') as f:
	pickle.dump(locations,f)