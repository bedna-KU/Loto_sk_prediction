from __future__ import print_function
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import LSTM, RepeatVector, TimeDistributed, Dense, Dropout, Activation, Input, Conv2D, Conv1D, Flatten, Reshape
from keras.optimizers import Adam
from numpy import array
from numpy import argmax
import numpy as np
import sys
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from os import path

import csv

from supermario.model import model_cnn_3

####################################################
# PARAMETERS
####################################################

MAX_LEN = 7
MAX_VALUE = 49
ACTIVATION = "relu"
EPOCHS = 22000
BATCH_SIZE = 8192
FILEPATH = "weights_cnn_tst2.hdf5"

####################################################

# Load data
def data_load ():
	results = []

	# Read CSV file into array
	with open ("loto1.csv", newline="") as csvfile:
		reader = csv.reader (csvfile, delimiter=';')
		for row in reader:
			results.append (row)

	# Remove firs line with array
	del results[0]

	# Extract only numbers to list
	data = []
	for row in results:
		numbers = row[3:10]
		line_data = []
		for num in numbers:
			line_data.append (int (num))
		data.append (line_data)

	print ('*** Lines count', len (data))
	numbers = set (x for l in data for x in l)
	numbers = sorted (numbers)
	MAX_VALUE = len (numbers)
	print ('*** Total numbers: ', MAX_VALUE)
	print ('*** Numbers:', numbers)
	# Split data to prev/next numbers
	X = data[-1]
	y = [0, 0, 0, 0, 0, 0, 0]
	X_nums = X
	y_nums = y
	# To ndarray
	y = np.array (y, dtype = np.float32)
	# Encode data
	X = one_hot_encode ([X], MAX_VALUE)
	y = encode (y, MAX_VALUE)
	# To ndarray
	X = np.array (X)

	return X, y, X_nums, y_nums

# Unvectorize data
def one_hot_decode (value, max):
	strings = list ()
	for pattern in value:
		string = str (argmax (pattern))
		strings.append (string)
	return ' '.join (strings)

# Vectorize data
def one_hot_encode (value, max_int):
	max_int = max_int + 1
	value_enc = list ()
	for seq in value:
		pattern = list ()
		for index in seq:
			vector = [0 for _ in range (max_int)]
			vector[index] = 1
			pattern.append (vector)
		value_enc.append (pattern)
	return value_enc

# Invert encoding
def decode (value, max):
	return value * max

# Encode data
def encode (value, max):
	result = value / max
	return result

# Run evry epoch
def predict ():
	length = 7
	diversity = 1.0
	generated = ''
	prev_nums_arr = X_nums
	prev_nums_arr = np.array (prev_nums_arr)
	print (">>>PREV>>>>", prev_nums_arr)
	numbers_enc = one_hot_encode ([prev_nums_arr], MAX_VALUE)
	numbers_enc = np.expand_dims (numbers_enc, axis = 3)
	result = model.predict (numbers_enc, batch_size = BATCH_SIZE, verbose=0)
	predicted_nums = decode (result[0], MAX_VALUE)
	predicted_nums = np.around (predicted_nums)
	real_nums_arr = y_nums
	print (">>>REAL>>>>", np.array (real_nums_arr))
	predicted_nums = predicted_nums.astype ('int')
	print (">>>TIP>>>>>", predicted_nums)
	predicted_nums_arr = predicted_nums.tolist ()
	matches = len ([key for key, val in enumerate (predicted_nums_arr) if val in set (real_nums_arr)])
	print (">>>MATCH>>>", matches)

# Load trained weights
def model_load (model):
	if path.exists (FILEPATH):
		model.load_weights (FILEPATH)

model = model_cnn_3 (MAX_LEN, MAX_VALUE, ACTIVATION)
model_load (model)
X, y, X_nums, y_nums = data_load ()
predict ()
