import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import seaborn as sns

import os,sys
import pickle
import random
import math
import time
import numpy as np
import networkx as nx
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon, Rectangle
from collections import OrderedDict

def calCorrDistribution(A,G,nodeNames,filename):
	'''N: Number of Nodes
	L: Number of Edges while considering weight
	k: Average degree'''
	
	path='/'.join(filename.split('/')[:-2])
	print("-->",path)
	f=open(path+"/networkfeautures.csv","a")
	yr=filename.split('_')[-1]
	L=0.0
	N=G.number_of_nodes()
	for i in range(0,len(A)):
		for j in range(0,len(A)):
			node1 = nodeNames[i]
			node2 = nodeNames[j]
			if node1 not in skip and node2 not in skip:
				if A[i][j]!=0.0:
					L=L+A[i][j]
		  
	L=L/2
	try:
		k=2*L/N
		CC1=(2*L)/(N*(N-1))
		CC2=nx.average_clustering(G,weight='weight')
		randomDiameter=math.log(N)/math.log(k)
	except Exception as e:
		k=e
		CC1=e
		CC2=e
		randomDiameter=e

	try:
		diameter=nx.diameter(G)
		radius=nx.radius(G)
	except Exception as e:
		diameter=e
		radius=e
		
	
	
	degreeDistribution=G.degree(weight='weight')
	temp=[yr,N,L,k,diameter,radius,randomDiameter,CC1,CC2]
	f.write(",".join([str(i) for i in temp])+"\n")
	f.close()

def validateLocation(longitude,latitude):
	if ( lower_left_lon< longitude <upper_right_lon ) and (lower_left_lat < latitude < upper_right_lat):
		return True
	else:
		print("False------------------------------------>")
		print(longitude,latitude)
		return False

lower_left_lon=-129.75
lower_left_lat= 20.91
upper_right_lon=-64.63
upper_right_lat= 50.08

skip=[]
def plotNetworkGraph(waveMatrix, locations,nodeNames, filename, thresholds, nodeSize,yearInput):
	cmap=plt.get_cmap("Purples")
	resolution='h'
	# # new carb
	# carbA=[6,41,53,8,16,31,40,49]
	# carbB=[9,10,23,24,25,34,36,42,44,50,11,13]

	carbA=[6,41,53]
	carbB=[9,10,23,24,25,34,36,42,44,50,11]
	noState = ['"Guam"','"Puerto Rico"','"Hawaii"','"Virgin Islands"','"Alaska"']
	noStateCode = [66,72,15,78,2]

	others = [int(i.split('-')[0]) for i in nodeNames if int(i.split('-')[0]) not in carbA+carbB and int(i.split('-')[0]) not in noStateCode]
	print(list(set(others)))
	communities= [carbA,carbB,list(set(others))]
	for thres in thresholds:
		Bmap_Amplitude = Basemap(projection='merc',llcrnrlon=lower_left_lon,llcrnrlat=lower_left_lat,urcrnrlon=upper_right_lon,urcrnrlat=upper_right_lat,lat_ts=0,resolution=resolution,suppress_ticks=True)
		G_Amplitude = nx.Graph()
		for name in nodeNames:
			try:
				longitude=locations[int(name)][0]
				latitude=locations[int(name)][1]
			except:
				longitude=locations[name][0]
				latitude=locations[name][1]
			#print(latitude,longitude)
			if(validateLocation(latitude,longitude)):
				x,y=Bmap_Amplitude(latitude,longitude)
				#print(x,y)
				G_Amplitude.add_node(name,pos=(x,y))
			else:
				skip.append(name)

		for i in range(len(waveMatrix)):
			for j in range(i+1,len(waveMatrix)):
				node1 = nodeNames[i]
				node2 = nodeNames[j]
				statea,stateb=int(node1.split('-')[0]),int(node2.split('-')[0])
				for community in communities:
					if statea in community and stateb in community:		
						wC = waveMatrix[i][j]
						highWave = (wC > thres)					
						if(highWave):
							if node1 not in skip and node2 not in skip:
								G_Amplitude.add_edge(node1, node2, weight = wC)						
									
					

		#calCorrDistribution(waveMatrix,G_Amplitude,nodeNames,filename)

		for node in skip:
			del nodeNames[nodeNames.index(node)]

		plt.close()
		plt.axis('off')
		year=filename.split('/')[-1]
		
		edgewidth_Amplitude = [ d['weight'] for (u,v,d) in G_Amplitude.edges(data=True)]
		pos=nx.get_node_attributes(G_Amplitude,'pos')
		

		nodeS=G_Amplitude.degree(weight = 'weight')

		
		nodeD=OrderedDict()
		for i in nodeS:
			nodeD[i[0]]=i[1]

		maxS = max(map(lambda x:x[1], nodeS))
		minS = min(map(lambda x:x[1], nodeS))
		#nodeColor=list(map(lambda x:'#%02x%02x%02x' % (255, 250 - int(((x[1] - minS)/(maxS - minS))*250), 250 - int(((x[1] - minS)/(maxS - minS))*250)), nodeS))
		nodeColor=list(map(lambda x:'#%02x%02x%02x' % (0, 250 - int(((x[1] - minS)*150)/(maxS - minS)), 0), nodeS))
		nCom=len(communities)
		comColors=[i for i in np.arange(0,1,1/nCom)]
		colorMaps=['Greens','Purples','Reds','Blues','Greys','Oranges']
		# so^>v<dph8
	
		edgeColor,nodeColor,alphaList=[],[],[]
		
		for node in nodeNames:
			for community,num in zip(communities,range(len(communities))):
				statecode = int(node.split('-')[0])
				if statecode in community:
					tcmap=plt.get_cmap(colorMaps[num])
					nodeColor.append(tcmap(nodeD[node]))

		for node1,node2,d in G_Amplitude.edges(data=True):
			flag=0
			for community,tempc,num in zip(communities,comColors,range(nCom)):
				statea,stateb=int(node1.split('-')[0]),int(node2.split('-')[0])

				if statea in community and stateb in community:
					
					tempCmap=plt.get_cmap(colorMaps[num])
					colorMark=tempCmap(d['weight'])
					edgeColor.append(colorMark)
					alphaList.append(0.9)

					flag=1
					
			if flag==0:
				tempCmap=plt.get_cmap('binary')
				colorMark=tempCmap(0.1)
				alphaMark=tempCmap(0.1)
				edgeColor.append(colorMark)
				alphaList.append(0.1)

				
					

		#nodeColor=[(0, int(((nodeD[x] - minS)*180)/(maxS - minS)), 0) for x in nodeList]

		nodeSize=[int(3+(((nodeD[x] - minS)*7)/(maxS - minS))) for x in nodeNames]
		
		nx.draw_networkx_nodes(G_Amplitude,pos, node_color =nodeColor , nodelist = nodeNames , node_size = nodeSize)
		nx.draw_networkx_edges(G_Amplitude, pos,cmap=cmap,edge_color =  edgeColor, alpha = alphaList, width=edgewidth_Amplitude)

		shp_info = Bmap_Amplitude.readshapefile('st99_d00','states',drawbounds=True)
		
		ax = plt.gca() # get current axes instance
		ax.text(-0.0003, 0.98, 'd)', transform=ax.transAxes, size=12,color='purple')

		for _,seg in enumerate(Bmap_Amplitude.states):
			# skip DC and Puerto Rico.
				poly = Polygon(seg,facecolor='white',edgecolor='green', alpha = 0.9, zorder = -0.1,linewidth=0.05)
				ax.add_patch(poly)
	
		plt.axis('off')
		
		print(filename)
		lp=filename.split('/')[:-2]
		year=filename.split('/')[-2:]
		# plt.title(str(yearInput))
		#plt.text(40, 37, "Degree Distribution", fontsize=17, ha="center")
		plt.savefig("Carbresults_"+str(thres)+"{}.png".format(yearInput), dpi = 300,bbox_inches='tight')





#if __name__=="__main__":


yearInput = sys.argv[1]

waveMatrix=pickle.load(open("USA/Correlations/o3/{}/correlations.pickle".format(yearInput),"rb"))
locations=pickle.load(open("locations.pickle","rb"))
nodeNames=pickle.load(open("USA/Correlations/o3/{}/nodeNames.pickle".format(yearInput),"rb"))
waveMatrix = waveMatrix['Wave']
filename="newcarbnon"
nodeSize=15
thresholds=[0.0]
plotNetworkGraph(waveMatrix, locations,nodeNames, filename, thresholds, nodeSize,yearInput)