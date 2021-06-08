import xlsxwriter


def peelAndwaveCorrelationsWorkbook(waveCorr, peelCorr, nodeNames, writeDir, thresholds):
	for thres in thresholds:
		workbook = xlsxwriter.Workbook(writeDir + "/Correlations_"+ str(thres)+".xlsx")
		redCell = workbook.add_format()
		redCell.set_bg_color('red')	
		yellowCell = workbook.add_format()
		yellowCell.set_bg_color('yellow')
		whiteCell = workbook.add_format()
		whiteCell.set_bg_color('white')	
		worksheetWave = workbook.add_worksheet('Wave')
		worksheetPeel = workbook.add_worksheet('Peel')
		worksheetWave.write_row("B1", nodeNames)
		worksheetPeel.write_row("B1", nodeNames)
		for i in range(len(nodeNames)):
			worksheetWave.write(i+1, 0, nodeNames[i])
			worksheetPeel.write(i+1, 0, nodeNames[i])
			for j in range(0,i):
				wC = waveCorr[i][j]
				pC = peelCorr[i][j]

				highWave = (abs(wC) > thres)
				highPeel = (abs(pC) > thres)
				bothHigh = highWave and highPeel
				onlyPeel = (not highWave) and highPeel
				onlyWave = (not highPeel) and highWave
				if(bothHigh):
					worksheetWave.write(i+1,j+1,'%.3f' % wC ,redCell)
					worksheetPeel.write(i+1,j+1,'%.3f' % pC ,redCell)
				elif(onlyPeel):
					worksheetWave.write(i+1,j+1,'%.3f' % wC ,whiteCell)
					worksheetPeel.write(i+1,j+1,'%.3f' % pC ,yellowCell)
				elif(onlyWave):
					worksheetWave.write(i+1,j+1,'%.3f' % wC ,yellowCell)
					worksheetPeel.write(i+1,j+1,'%.3f' % pC ,whiteCell)
				else:
					worksheetWave.write(i+1,j+1,'%.3f' % wC ,whiteCell)
					worksheetPeel.write(i+1,j+1,'%.3f' % pC ,whiteCell)
		workbook.close()

