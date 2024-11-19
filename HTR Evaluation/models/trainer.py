import random, cv2, sys, argparse, os, math
import numpy as np
sys.path.append("../utils")
sys.path.append("../models")

parser = argparse.ArgumentParser('Model Training & Testing Parameters')
parser.add_argument('--train_file', type = str, default = "")
parser.add_argument('--val_file', type = str, default = "")
parser.add_argument('--test_file', type = str, default = "")
parser.add_argument('--num_epochs', type = int, default = 35)
parser.add_argument('--starting_epoch', type = int, default = 0)
parser.add_argument('--weights', type = str, default = None)
parser.add_argument('--run_name', type = str, default = 'CRNN')
parser.add_argument('--lr', type = float, default = 0.001)
parser.add_argument('--batch_size', type = int, default = 64)
parser.add_argument('--gpu', type = str, default = 0)
args = parser.parse_args()
os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

from model_utils import *
from DataLoader import *
from CRNN import *
from keras import backend as K
from keras.models import Model
from keras.optimizers import RMSprop
K.clear_session()
unicodes = list(np.load('unicodes.npy', allow_pickle = True))

if args.train_file == "" and args.test_file == "":
	print('Enter either train_file or test_file, or both')
	exit()
	
if args.train_file != "":
	with tf.device('/cpu:0'):
		if args.val_file != "":
			loader = DataLoader(args.train_file, args.val_file, unicodes)
		else:
			loader = DataLoader(args.train_file, args.test_file, unicodes)
		trainModel = CRNN(True, len(unicodes) + 1)
		if args.weights is not None:
			trainModel.load_weights(args.weights + '.h5')
		trainModel.compile(loss = {'ctc': lambda yTrue,yPred: yPred}, optimizer = RMSprop(lr = args.lr))
		
	with tf.device('/gpu:0'):
		_ = trainModel.fit_generator(generator = loader.nextTrain(args.batch_size), \
						steps_per_epoch = math.ceil(loader.trainLength / args.batch_size), \
						epochs = args.num_epochs - args.starting_epoch, \
						validation_data = loader.nextVal(args.batch_size), \
						validation_steps = math.ceil(loader.valLength / args.batch_size))

if args.test_file != "":
	with tf.device('/cpu:0'):
		loader = DataLoader(args.train_file, args.test_file, unicodes)
		testModel = CRNN(False, len(unicodes) + 1)
		if args.weights is not None:
			testModel.load_weights(args.weights + '.h5')
		if args.train_file != "":
			testModel.set_weights(trainModel.get_weights())
		CAR, WAR = test(testModel, loader)