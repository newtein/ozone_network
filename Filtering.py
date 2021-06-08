#In this file, I aim to write down several peeling off techniques.

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import pandas as pd
import copy
import scipy.signal as signal

def plotData(data, smooth_data, error, filename):
	gs = gridspec.GridSpec(2,1,height_ratios = [1,0.4])
	plt.close()
	plt.subplot(gs[0,0])
	plt.style.use('ggplot')
	plt.rcParams['axes.facecolor']='white'
	plt.rcParams['grid.color']='gainsboro'
	plt.plot(smooth_data, color = 'darkred', linewidth = 0.7)
	plt.plot(data, color = 'salmon',alpha = 0.6)
	plt.subplot(gs[1,0])
	plt.plot(error, color = 'darkred',alpha = 0.6)
	plt.tight_layout()
	plt.savefig(filename)

def fillGaps(a):
	flag = False
	start = -1
	for i in range(len(a)):
		if(flag == False):
			if(a[i] == '-'):
				flag = True
				start = i
			else:
				continue
		else:
			if(a[i] == '-'):
				continue
			else:
				end = i
				if(start == 0):
					for j in range(start, end):
						a[j] = a[end]
				else:
					step = (a[end] - a[start - 1])/(end - start + 1)
					for j in range(start, end):
						a[j] = a[j - 1] + step
				flag = False
				start = -1
	if(flag == True):
		for j in range(start,len(a)):
			a[j] = a[start - 1]
	return a

def movingAverages(data, window, fillData = False):
	origData = data
	if(fillData):
		data = fillGaps(data)
	smooth_data = []
	for i in range(window,len(data)):
		smooth_data.append(np.mean(data[i - window: i]))
	peel = np.array(data[-len(smooth_data):]) - np.array(smooth_data)
	for i in range(len(origData)):
		if(origData[i] == '-'):
			peel[i] = '-'
			smooth_data[i] = '-'
	return smooth_data, peel

def detrending(data, parameter, fillData = False):
	origData = data
	if(fillData):
		data = fillGaps(data)
	smooth_data = []
	for i in range(1,len(data)):
		smooth_data.append(data[i] - data[i-1])
	peel = np.array(data[-len(smooth_data):]) - np.array(smooth_data)
	for i in range(len(origData)):
		if(origData[i] == '-'):
			peel[i] = '-'
			smooth_data[i] = '-'
	return smooth_data, peel

def singleExponentialSmoothing(data, alpha, fillData = False):
	origData = data
	if(fillData):
		data = fillGaps(data)
	smooth_data = [data[0]]
	for dat in data[1:]:
		smooth_data.append(alpha*dat + (1-alpha)*smooth_data[-1])
	peel = np.array(data[-len(smooth_data):]) - np.array(smooth_data)
	for i in range(len(origData)):
		if(origData[i] == '-'):
			peel[i] = '-'
			smooth_data[i] = '-'
	return smooth_data, peel


def fft(data, alpha, fillData = False):
	origData = data
	if(fillData):
		data = fillGaps(data)
	frequency = np.fft.rfft(data)
	frequency[alpha:] = 0.0
	smooth_data = np.fft.irfft(frequency)
	peel = np.array(data[-len(smooth_data):]) - np.array(smooth_data)
	for i in range(len(origData)):
		if(origData[i] == '-'):
			peel[i] = '-'
			smooth_data[i] = '-'
	return smooth_data, peel

def savitzkyGolay(data, parameters, fillData = False):
	origData = data
	if(fillData):
		data = fillGaps(data)
	smooth_data = signal.savgol_filter(data, parameters[0], parameters[1])
	peel = np.array(data[-len(smooth_data):]) - np.array(smooth_data)
	for i in range(len(origData)):
		if(origData[i] == '-'):
			peel[i] = '-'
			smooth_data[i] = '-'
	return smooth_data, peel