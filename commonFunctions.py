import os
import scipy.stats as stats

def makeDir(name):
	if(not os.path.isdir(name)):
		os.mkdir(name)
	return name

def correlation(wave1, wave2, gaps = False):
	if(gaps):
		newWave1 = []
		newWave2 = []
		if(len(wave1) != len(wave2)):
			raise Exception('Length not similar')
		else:
			for i in range(len(wave1)):
				if(wave1[i] != '-')and(wave2[i] != '-'):
					newWave1.append(wave1[i])
					newWave2.append(wave2[i])
		if stats.pearsonr(newWave1,newWave2)[1]<0.01:
				return stats.pearsonr(newWave1,newWave2)[0], len(newWave1)
		else:
			return 0.0, len(newWave1)
	else:
		size = min(len(wave1), len(wave2))
		if stats.pearsonr(wave1[:size], wave2[:size])[1]<0.01:
				return stats.pearsonr(wave1[:size], wave2[:size])[0], size
		else:
			return 0, size