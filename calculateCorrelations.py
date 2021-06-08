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
import excelFunctions as ef
import sys

def genericFolderReader(homeFolder, writeDir, randomized = False, randomizedLevels = None, randomizedCount = None, level = 0):
	global smoothingParams, dataTransformations, fillData, thresholds
	print(homeFolder)
	subFolders = [d for d in os.listdir(homeFolder) if os.path.isdir(os.path.join(homeFolder, d))]
	if('__pycache__' in subFolders):
		subFolders.remove('__pycache__')
	subFolders.sort()
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

	if(len(subFolders) == 0):
		nodeNames = [d.split('.')[0] for d in os.listdir(homeFolder)]
		nodeData = {}
		try:
			for name in nodeNames:
				with open(homeFolder + "/" + name + '.pickle', 'rb') as f:
					data = pickle.load(f)
				nodeData[name] = {}
				#smooth_data, peel = ft.savitzkyGolay(data, smoothingParams, fillData = fillData)
				smooth_data, peel=data,data

				nodeData[name]["Wave"] = data
				# nodeData[name]["Peel"] = peel
			correlationMatrices = {}
			NPflag = True
			for trans in dataTransformations:
				print("ddd",dataTransformations)
				correlationMatrices[trans] = []
				if(NPflag):
					correlationMatrices['NumberOfPoints'] = []
				for i in range(len(nodeNames)):
					set1 = nodeData[nodeNames[i]]
					correlationMatrices[trans].append([])
					if(NPflag):
						correlationMatrices['NumberOfPoints'].append([])
					for j in range(len(nodeNames)):
						set2 = nodeData[nodeNames[j]]
						corr, numPoints = cf.correlation(set1[trans], set2[trans], gaps = fillData)
						correlationMatrices[trans][i].append(corr)
						if(NPflag):
							correlationMatrices['NumberOfPoints'][i].append(numPoints)
				NPFlag = False
			# ef.peelAndwaveCorrelationsWorkbook(correlationMatrices['Wave'], correlationMatrices['Peel'], nodeNames, writeDir, thresholds)
			with open(writeDir + "/correlations.pickle","wb") as f:
				pickle.dump(correlationMatrices,f)
			with open(writeDir + "/nodeNames.pickle","wb") as f:
				pickle.dump(nodeNames, f)
		except:
			raise
	else:
		for folder in subFolders:
			newWriteDir = cf.makeDir(writeDir + "/" + folder)
			genericFolderReader(homeFolder + "/" + folder, newWriteDir, level = level+1, randomized = randomized, randomizedLevels = randomizedLevels, randomizedCount = randomizedCount)
	return True

stateCode=sys.argv[1]
fillData = True
smoothingParams = [53,5]
thresholds = [0.0]
dataTransformations = ['Wave']
readDir = "./"+stateCode+"/Data"
writeDir = cf.makeDir("./"+stateCode+"/Correlations")

genericFolderReader(readDir, writeDir)