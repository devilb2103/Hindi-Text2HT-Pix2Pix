import random, cv2
import numpy as np
seed = 13
random.seed(seed)
np.random.seed(seed)

def truncateLabel(text, maxStringLen = 32):
	cost = 0
	for i in range(len(text)):
		if i!=0 and text[i] == text[i-1]:
			cost+=2
		else:
			cost+=1
		if cost > maxStringLen:
			return text[:i]
	return text
	
def textToLabels(text, unicodes):
	ret = []
	for c in text:
		ret.append(unicodes.index(c))
	return ret

def labelsToText(labels, unicodes):
	ret = []
	for c in labels:
		if c == len(unicodes):
			ret.append("")
		else:
			ret.append(unicodes[c])
	return "".join(ret)
	
def preprocess(img, dataAugmentation = False):
	(wt, ht) = (128, 32)
	if img is None:
		img = (np.zeros((wt, ht, 1))).astype('uint8')
	img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] * 255
	
	if dataAugmentation:
		stretch = (random.random() - 0.5) 						# -0.5 .. +0.5
		wStretched = max(int(img.shape[1] * (1 + stretch)), 1)  # random width, but at least 1
		img = cv2.resize(img, (wStretched, img.shape[0])) 		# stretch horizontally by factor 0.5 .. 1.5
	img = closeFit(img)                                         # to avoid lot of white space around text
	
	h = img.shape[0]
	w = img.shape[1]
	fx = w / wt
	fy = h / ht
	f = max(fx, fy)
	newSize = (max(min(wt, int(w / f)), 1), max(min(ht, int(h / f)), 1)) 	#scale according to f (result at least 1 and at most wt or ht)
	img = cv2.resize(img, newSize, interpolation = cv2.INTER_AREA)   		#INTER_AREA important, Linear loses all info
	img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] * 255
	
	target = np.ones([ht, wt]) * 255
	target[0:newSize[1], 0:newSize[0]] = img
	img = cv2.transpose(target)
	(m, s) = cv2.meanStdDev(img)
	m = m[0][0]
	s = s[0][0]
	img = img - m
	img = img / s if s>1e-3 else img
	return np.reshape(img, (img.shape[0], img.shape[1], 1))
	
def closeFit(img):
	i = 2
	col = 255 - np.sum(img, axis=0)/img.shape[0]
	while i<img.shape[1] and col[i]<=5:
		i+=1
	w1 = max(0,i - 15)
	i = img.shape[1]-1
	while i>=0 and col[i]<=5:
		i-=1
	w2 = i + 15

	row = 255 - np.sum(img, axis=1)/img.shape[1]
	i = 2
	while i<img.shape[0] and row[i]<=4:
		i+=1
	h1 = max(0,i - 20)
	i = img.shape[0] - 1
	while i>=0 and row[i]<=5:
		i-=1
	h2 = i + 20
	final = img[h1:h2,w1:w2]
	if final.shape[0]*final.shape[1] == 0:
		return img
	return final