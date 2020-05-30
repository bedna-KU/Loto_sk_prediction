import keras
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, LSTM, RepeatVector, TimeDistributed
from keras.optimizers import Adam

def model_cnn_3 (max_len, max_value, activation):
	model = Sequential ()
	model.add (Conv2D (32, kernel_size = (3, 3), padding = "valid", strides = (1, 1), activation = activation, input_shape = (max_len, max_value + 1, 1)))
	model.add (Conv2D (64, kernel_size = (3, 3), padding = "valid", strides = (1, 1), activation = activation))
	model.add (Conv2D (128, kernel_size = (3, 3), padding = "valid", strides = (1, 1), activation = activation))
	model.add (Flatten ())
	model.add (Dense (1000, activation = activation))
	model.add (Dense (max_len, activation = activation))

	model.compile (optimizer = Adam (),
				   loss = 'mse',
				   metrics = ['accuracy'])
	return model
