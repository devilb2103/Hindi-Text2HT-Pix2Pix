import random, cv2, sys
import numpy as np
sys.path.append("../utils")
from data_utils import *
seed = 13
random.seed(seed)
np.random.seed(seed)

class DataLoader():
	def __init__(self, trainFile, valFile, unicodes):
		self.unicodes = unicodes
		self.trainFile = trainFile
		self.valFile = valFile
		self.maxStringLen = 32
		self.trainSet = []
		self.valSet = []
		self.trainIndex = 0
		self.valIndex = 0
		
		if self.trainFile != "":
			self.trainSet = self.importSet(True)
		if self.valFile != "":
			self.valSet = self.importSet(False)
		self.valLength = len(self.valSet)
		self.trainLength = len(self.trainSet)
		
	def importSets(train):
		set = []
		if train:
			file = open(self.trainFile, 'r', encoding='utf-8')
		else:
			file = open(self.valFile, 'r', encoding='utf-8')
		for line in file:
			inUnicodes = True
			if not line or line[0] =='#':
				#Ignoring Erroneous Lines manually skipped with # in file
				continue
			lineSplit = line.strip().split(' ')
			if len(lineSplit) >= 2:
				fileName = lineSplit[0]
				text = truncateLabel(' '.join(lineSplit[1:]))
				
				for ch in text:
					if not ch in self.unicodes:
						print('Char '+ str(ch)+ ' Not in Unicodes, and Word Omitted')
						#print(ch,('0'+hex(ord(ch))[2:]))
						inUnicodes = False
						
				if inUnicodes:
					if train:
						set.append((text, fileName))
					else:
						set.append((text, fileName))
			else:
				print(line + 'Check this Line')
		file.close()
		random.shuffle(set)
		return set
	
	def nextTrain(self, batchSize):
		while True:
			if self.trainIndex + batchSize >= self.trainLength:
				self.trainIndex = 0
				random.shuffle(self.trainSet)
			ret = self.getBatch(self.trainIndex, batchSize, True)
			self.trainIndex += batchSize
			yield ret
			
	def nextVal(self, batchSize):
		while True:
			if self.valIndex >= self.valLength:
				self.valIndex = 0
			ret = self.getBatch(self.valIndex, batchSize, False)
			self.valIndex += batchSize
			yield ret
			
	def getBatch(self, index, batchSize, train):
		if train:
			batch = self.trainSet[index:index + batchSize]
			size = self.trainLength
		else:
			batch = self.valSet[index:index + batchSize]
			size = self.valLength
		
		imgs = []
		labels = np.ones([batchSize, self.maxStringLen]) * len(self.unicodes)
		inputLength = np.zeros([batchSize, 1])
		labelLength = np.zeros([batchSize, 1])
		
		for i in range(min(batchSize, size-index)):
			img = cv2.imread(batch[i][1], 0)
			if img is None:
				img = np.zeros((128,32,1))
				print(batch[i][1] + 'is not available')
				
			img = img.astype('uint8')
			imgs.append(preprocess(img.astype('uint8'), train))
			labels[i, 0:len(batch[i][0])] = textToLabels(batch[i][0], self.unicodes)
			labelLength[i] = len(batch[i][0])
			inputLength[i] = self.maxStringLen - 2
		
		inputs = {
				'inputX' : np.asarray(imgs),
				'label' : labels,
				'inputLen' : inputLength,
				'labelLen' : labelLength,
					}
		outputs = {'ctc' : np.zeros([batSize])}
		if train:
			return (inputs, outputs)
		else:
			return imgs