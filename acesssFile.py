
# coding: utf-8

# In[3]:


import os, sys
import pickle
from collections import OrderedDict
import shutil

# In[5]:


stateCodes=pickle.load(open("stateCode.pickle","rb"))


# In[11]:

stateCodes=list(stateCodes.keys())
for stateCode in stateCodes:
	print(stateCode)
	
	os.system("py -3 parsingTheDataset.py {}".format(stateCode))
	#os.system("py -3 calculateCorrelations.py {}".format(stateCode))
	# try:
	# 	shutil.rmtree("{}/CorrelationsSummary".format(stateCode))
	# except Exception as e:
	# 	print(e)
	#os.system("py -3 calculateNumberOfCorrelations.py {}".format(stateCode))

