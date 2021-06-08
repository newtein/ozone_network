import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import seaborn as sns
import xlsxwriter
import scipy.stats as stats
import os,sys
import pickle
import random
import math
import commonFunctions as cf
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
def plotNetworkGraph(waveMatrix, locations,nodeNames, filename, thresholds, nodeSize,filterTo):
	
	# California
	# lower_left_lon=-125
	# lower_left_lat= 32
	# upper_right_lon=-113
	# upper_right_lat= 43
	# Texas
	# lower_left_lon=-107.4
	# lower_left_lat= 25
	# upper_right_lon=-93
	# upper_right_lat= 37
	# EC
	# lower_left_lon=-80.8
	# lower_left_lat= 37.73
	# upper_right_lon=-67.53
	# upper_right_lat= 45.88
	# WC
	# lower_left_lon=-124.90
	# lower_left_lat= 30.89
	# upper_right_lon=-113.64
	# upper_right_lat= 49.35
	# America

	cmap=plt.get_cmap("Purples")
	resolution='l'
	
	for thres in thresholds:
		Bmap_Amplitude = Basemap(projection='merc',llcrnrlon=lower_left_lon,llcrnrlat=lower_left_lat,urcrnrlon=upper_right_lon,urcrnrlat=upper_right_lat,lat_ts=0,resolution=resolution,suppress_ticks=True)

		G_Amplitude = nx.Graph()

		for name in nodeNames:
			if name in filterTo:
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
					if node1 in filterTo and node2 in filterTo:
						wC = waveMatrix[i][j]
						highWave = (wC > thres)					
						if(highWave):
							if node1 not in skip and node2 not in skip:
								G_Amplitude.add_edge(node1, node2, weight = wC)						
						else:
							continue

		calCorrDistribution(waveMatrix,G_Amplitude,nodeNames,filename)
		plt.close()

		#plt.figure(figsize = (20,8))
		#gs = gridspec.GridSpec(3,4)
		plt.axis('off')

		#plt.subplot(gs[0,0:2])
		year=filename.split('/')[-1]
		
		edgewidth_Amplitude = [ d['weight'] for (u,v,d) in G_Amplitude.edges(data=True)]
		pos=nx.get_node_attributes(G_Amplitude,'pos')
		

		nodeS=G_Amplitude.degree(weight = 'weight')
		#print(nodeS)
		nodeList=[i[0] for i in nodeS]
		nodeD=OrderedDict()
		for i in nodeS:
			nodeD[i[0]]=i[1]


		#print('nodeS', nodeS)
		maxS = max(map(lambda x:x[1], nodeS))
		minS = min(map(lambda x:x[1], nodeS))
		#nodeColor=list(map(lambda x:'#%02x%02x%02x' % (255, 250 - int(((x[1] - minS)/(maxS - minS))*250), 250 - int(((x[1] - minS)/(maxS - minS))*250)), nodeS))
		nodeColor=list(map(lambda x:'#%02x%02x%02x' % (0, 250 - int(((x[1] - minS)*150)/(maxS - minS)), 0), nodeS))
				
		#nodeColor=[(0, int(((nodeD[x] - minS)*180)/(maxS - minS)), 0) for x in nodeList]

		nodeSize=[int(3+(((nodeD[x] - minS)*7)/(maxS - minS))) for x in nodeList]

		
		#nodeColor='g'
		#nodeSize=10

		nx.draw_networkx_nodes(G_Amplitude,pos, node_color =nodeColor , nodelist = nodeList , node_size = nodeSize)
		
		#nx.draw_networkx_nodes(G_Amplitude,pos, node_color = 'r', node_size = nodeSize, alpha = 0.7)
		


		#nx.draw_networkx_edges(G_Amplitude, pos, edge_color = edgewidth_Amplitude, width=edgewidth_Amplitude, alpha = edgewidth_Amplitude)
		
		nx.draw_networkx_edges(G_Amplitude, pos,cmap=cmap,edge_color =  [cmap(i) for i in edgewidth_Amplitude], alpha = [cmap(i) for i in edgewidth_Amplitude], width=edgewidth_Amplitude)

		shp_info = Bmap_Amplitude.readshapefile('st99_d00','states',drawbounds=True)
		
		ax = plt.gca() # get current axes instance
		ax.text(-0.01, 0.9, 'a)', transform=ax.transAxes, size=15,color='purple')

		for _,seg in enumerate(Bmap_Amplitude.states):
			# skip DC and Puerto Rico.
				poly = Polygon(seg,facecolor='white',edgecolor='green', alpha = 0.9, zorder = -0.1,linewidth=0.05)
				ax.add_patch(poly)
	
		plt.axis('off')
		
		print(filename)
		lp=filename.split('/')[:-2]
		year=filename.split('/')[-2:]
		#plt.title('U.S. Ozone Network (1980 - 2017)')
		#plt.text(40, 37, "Degree Distribution", fontsize=17, ha="center")
		plt.savefig("/".join(lp)+ "/results_"+str(thres)+"{}.png".format(year), dpi = 300,bbox_inches='tight')




#if __name__=="__main__":

f=sys.argv[1]
community=sys.argv[2]
path="Community/{}".format(community)

waveMatrix=pickle.load(open("Com/waveMatrix.pickle","rb"))
locations=pickle.load(open("locations.pickle","rb"))
nodeNames=pickle.load(open("Com/Correlations/o3/2017/nodeNames.pickle".format(path),"rb"))
filterTo=pickle.load(open("Community/{}/{}.pickle".format(community,f),"rb"))
filename="{}/map{}".format(path,f)
nodeSize=15
thresholds=[0.0]
plotNetworkGraph(waveMatrix, locations,nodeNames, filename, thresholds, nodeSize,filterTo)