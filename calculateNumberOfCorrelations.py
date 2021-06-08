import Filtering as ft
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import xlsxwriter
import scipy.stats as stats
import os
import pickle
import random
import math
import commonFunctions as cf
import time
import numpy as np
import plotChartFunctions as pcf
import sys

def genericFolderReader(homeFolder, writeDir, randomized = False, randomizedLevels = None, randomizedCount = None, level = 0):
	print(homeFolder)
	global thresholds,locations
	subFolders = [d for d in os.listdir(homeFolder) if os.path.isdir(os.path.join(homeFolder, d))]
	if('__pycache__' in subFolders):
		subFolders.remove('__pycache__')

	subFolders.sort()
	if(level == 0):
		subFolders.reverse()
	if(randomized):
		if((level+1) in randomizedLevels):
			randomList = []
			count = 0
			while(count < randomizedCount[level + 1]):
				number = random.randrange(0,len(subFolders) - 1)
				if(number not in randomList):
					randomList.append(number)
				count += 1
			subFoldersUpdated = []
			for i in randomList:
				subFoldersUpdated.append(subFolders[i])
			subFolders = subFoldersUpdated

	correlationCounts = {}
	consistencyMatrices = [{},{},{},{},{}]
	pcMatrix = np.zeros(shape=(64,64))
	wcMatrix = np.zeros(shape=(64,64))
	
	if(len(subFolders) == 0):
		try:
			with open(homeFolder + "/correlations.pickle",'rb') as f:
				correlationMatrices = pickle.load(f)

			with open(homeFolder + '/nodeNames.pickle','rb') as f:
				nodeNames = pickle.load(f)

			# with open(homeFolder + '/mean.pickle','rb') as f:
			# 	city_mean = pickle.load(f)

		except:
			raise
			return False

		pcMatrix = np.array(correlationMatrices['Wave'])
		wcMatrix = np.array(correlationMatrices['Wave'])
		nodeSize=[10 for name in nodeNames]
		
		pcf.plotNetworkGraph(wcMatrix,pcMatrix,locations,nodeNames,writeDir,thresholds, nodeSize,stateCode)
		# for thres in thresholds:
		# 	correlationCounts[thres] = np.array([0.0,0.0,0.0,0.0,0.0])
		# 	for mlen in range(len(consistencyMatrices)):
		# 		consistencyMatrices[mlen][thres] = {}
		# 		for i in range(len(nodeNames)):
		# 			consistencyMatrices[mlen][thres][nodeNames[i]] = {}
		# 			for j in range(len(nodeNames)):
		# 				consistencyMatrices[mlen][thres][nodeNames[i]][nodeNames[j]] = 0
		# 	countTotal = 0
		# 	for i in range(len(pcMatrix)):
		# 		for j in range(0,i):
		# 			countTotal += 1
		# 			pC = pcMatrix[i][j]
		# 			wC = wcMatrix[i][j]

		# 			highPC = abs(pC) > thres
		# 			highWC = abs(wC) > thres

		# 			if((highPC)and(highWC)):
		# 				correlationCounts[thres][0] += 1
		# 				correlationCounts[thres][1] += 1
		# 				correlationCounts[thres][4] += 1

		# 				consistencyMatrices[0][thres][nodeNames[i]][nodeNames[j]] += 1
		# 				consistencyMatrices[1][thres][nodeNames[i]][nodeNames[j]] += 1
		# 				consistencyMatrices[4][thres][nodeNames[i]][nodeNames[j]] += 1

		# 				consistencyMatrices[0][thres][nodeNames[j]][nodeNames[i]] += 1
		# 				consistencyMatrices[1][thres][nodeNames[j]][nodeNames[i]] += 1
		# 				consistencyMatrices[4][thres][nodeNames[j]][nodeNames[i]] += 1

		# 			else:
		# 				if(highPC):
		# 					correlationCounts[thres][1] += 1
		# 					correlationCounts[thres][3] += 1

		# 					consistencyMatrices[1][thres][nodeNames[i]][nodeNames[j]] += 1
		# 					consistencyMatrices[3][thres][nodeNames[i]][nodeNames[j]] += 1

		# 					consistencyMatrices[1][thres][nodeNames[j]][nodeNames[i]] += 1
		# 					consistencyMatrices[3][thres][nodeNames[j]][nodeNames[i]] += 1

		# 				if(highWC):
		# 					correlationCounts[thres][0] += 1
		# 					correlationCounts[thres][2] += 1

		# 					consistencyMatrices[0][thres][nodeNames[i]][nodeNames[j]] += 1
		# 					consistencyMatrices[2][thres][nodeNames[i]][nodeNames[j]] += 1

		# 					consistencyMatrices[0][thres][nodeNames[j]][nodeNames[i]] += 1
		# 					consistencyMatrices[2][thres][nodeNames[j]][nodeNames[i]] += 1
		# 	for num in range(5):
		# 		if(countTotal != 0):
		# 			correlationCounts[thres][num] = (correlationCounts[thres][num]/countTotal)*100

	else:
		validFolders = 0
		nodeNames = []
		dataFolders = []

		for thres in thresholds:
			correlationCounts[thres] = np.zeros(5)

		for folder in subFolders:
			newWriteDir = cf.makeDir(writeDir + "/" + folder)
			if(os.path.exists(newWriteDir + "/correlationSummary.pickle")):
				with open(newWriteDir + "/correlationSummary.pickle", "rb") as f:
					data_oneFolder = pickle.load(f)
			else:
				start = time.time()
				data_oneFolder = genericFolderReader(homeFolder + "/" + folder, newWriteDir, level = level+1, randomized = randomized, randomizedLevels = randomizedLevels, randomizedCount = randomizedCount)
				end = time.time()
				print(str(end - start) + "seconds")
			if(data_oneFolder != False):
				dataFolders.append(data_oneFolder)
				validFolders += 1

		for data_oneFolder in dataFolders:
			for thres in thresholds:
				correlationCounts[thres] += data_oneFolder[0][thres]/validFolders
		
		for data_oneFolder in dataFolders:
			if(nodeNames == []):
				nodeNames = set(data_oneFolder[2])
			else:
				nodeNames.intersection_update(data_oneFolder[2])

		nodeNames = list(nodeNames)
		if(len(nodeNames) > 1):
			for mlen in range(len(consistencyMatrices)):
				consistencyMatrices[mlen][thres] = {}
				for i in range(len(nodeNames)):
					consistencyMatrices[mlen][thres][nodeNames[i]] = {}
					for j in range(len(nodeNames)):
						consistencyMatrices[mlen][thres][nodeNames[i]][nodeNames[j]] = 0

			for data_oneFolder in dataFolders:
				for i in range(len(nodeNames)):
					for j in range(len(nodeNames)):
						consistencyMatrices[mlen][thres][nodeNames[i]][nodeNames[j]] += (float(data_oneFolder[1][mlen][thres][nodeNames[i]][nodeNames[j]])/float(validFolders))
		else:
			nodeNames = []
			consistencyMatrices = False




	dataToreturn = [correlationCounts, consistencyMatrices,nodeNames]
	with open(writeDir + "/correlationSummary.pickle","wb") as f:
		try:
			pickle.dump(dataToreturn, f)
		except:
			pickle.dump({}, f)
	#pcf.plotTotalCorrelations(correlationCounts, writeDir + '/numberOfCorrelations.png')
	return dataToreturn



with open('./locations.pickle','rb') as f:
	locations = pickle.load(f)

stateCode=sys.argv[1]



thresholds = [0.0]
readDir = "./"+stateCode+"/Correlations"
writeDir = cf.makeDir("./"+stateCode+"/CorrelationSummary")
nodeSize = 1

genericFolderReader(readDir, writeDir)