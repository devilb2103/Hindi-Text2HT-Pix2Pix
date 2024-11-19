import cv2, itertools, sys, editdistance, math
import numpy as np
import tensorflow.keras.backend.ctc_batch_cost as ctcLoss
sys.path.append("../models")
from data_utils import *
from CRNN import *
from keras.models import Model

def predictImage(imgPath, weightPath):
	img = cv2.imread(imgPath, 0)
	img = preprocess(img, False)
	img = np.reshape(img, (1, img2.shape[0], img2.shape[1], 1))
	unicodes = list(np.load('unicodes.npy', allow_pickle = True))
	model = CRNN(False, len(unicodes + 1))
	model.load_weights(weightPath)
	out = model.predict(img2)
	pred = decode(out)
	print('Recognized Word: '+ str(pred))
	
def ctcLambdaFunc(yPred, labels, inputLength, labelLength):
	yPred = yPred[:,2:,:]
	loss = ctcLoss(labels, yPred, inputLength, labelLength)
	return loss

def decode(yPred, unicodes):  #Best Path Decoder
	texts = []
	for y in yPred:
		label = list(np.argmax(y[2:],1))
		label = [k for k, g in itertools.groupby(label)]
		text = labelsToText(label, unicodes)
		texts.append(text)
	return texts
	
def test(model, loader):
	validation = loader.valSet
	trueText = []
	for (i, path) in validation:
		trueText.append(i)
		
	outputs = model.predict_generator(loader.nextVal(512), steps = math.ceil(loader.valLength/512))
	predText = decode(outputs)
	
	wordOK = 0
	wordTot = 0
	charDist = 0
	charTot = 0
	for i in range(len(trueText)):
		#print(predText[i], trueText[i])
		wordOK += 1 if predText[i] == trueText[i] else 0
		wordTot += 1
		dist = editdistance.eval(predText[i], trueText[i])
		charDist += dist
		charTot += len(trueText[i])
		
	CAR = 100 - 100 * charDist/charTot
	WAR = 100 * wordOK/wordTot
	print('Character Accuracy Rate (CAR):' + str(CAR))
	print('Word Accuracy Rate (WAR):' + str(WAR))
	return (CAR, WAR)