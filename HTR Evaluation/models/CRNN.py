from keras import backend as K
from keras.layers import *
from keras.models import Model
from keras.activations import elu

def CRNN(train, outClasses):
	inputShape = (128, 32, 1)
	kernels = [5, 5, 3, 3, 3]
	filters = [32, 64, 128, 128, 256]
	strides = [(2,2), (2,2), (1,2), (1,2), (1,2)]
	rnnUnits = 256
	maxStringLen = 32
	
	inputs = Input(name = 'inputX', shape = inputShape, dtype = 'float32')
	labels = Input(name='label', shape=[maxStringLen], dtype='float32')
	inputLength = Input(name='inputLen', shape=[1], dtype='int64')
	labelLength = Input(name='labelLen', shape=[1], dtype='int64')
	
	inner = inputs
	for i in range(len(kernels)):
		inner = convolutional.Conv2D(filters[i], (kernels[i], kernels[i]), padding = 'same',\
					   name = 'conv' + str(i+1), kernel_initializer = 'glorot_normal') (inner)
		inner = BatchNormalization() (inner)
		inner = Activation(elu) (inner)
		inner = convolutional.MaxPooling2D(pool_size = strides[i], name = 'max' + str(i+1)) (inner)
	inner = Reshape(target_shape = (maxStringLen,rnnUnits1), name = 'reshape')(inner)
	
	LSF = recurrent.LSTM(rnnUnits, return_sequences=True, kernel_initializer='glorot_normal', name='LSTM1F') (inner)
	LSB = recurrent.LSTM(rnnUnits, return_sequences=True, go_backwards = True, kernel_initializer='glorot_normal', name='LSTM1B') (inner)
	LSB = Lambda(lambda inputTensor: K.reverse(inputTensor, axes=1)) (LSB)
	LS1 = merge.average([LSF, LSB])
	LS1 = BatchNormalization() (LS1)
	
	LSF = recurrent.LSTM(rnnUnits, return_sequences=True, kernel_initializer='glorot_normal', name='LSTM2F') (LS1)
	LSB = recurrent.LSTM(rnnUnits, return_sequences=True, go_backwards = True, kernel_initializer='glorot_normal', name='LSTM2B') (LS1)
	LSB = Lambda(lambda inputTensor: K.reverse(inputTensor, axes=1)) (LSB)
	LS2 = merge.concatenate([LSF, LSB])
	LS2 = BatchNormalization() (LS2)
	
	yPred = Dense(outClasses, kernel_initializer='glorot_normal', name='dense2') (LS2)
	yPred = Activation('softmax', name='softmax') (yPred)
	lossOut = Lambda(ctcLambdaFunc, output_shape=(1,), name='ctc') ([yPred, labels, inputLength, labelLength])
	
	if training:
		return Model(inputs=[inputs, labels, inputLength, labelLength], outputs=[lossOut, yPred])
	return Model(inputs=[inputs], outputs=yPred)