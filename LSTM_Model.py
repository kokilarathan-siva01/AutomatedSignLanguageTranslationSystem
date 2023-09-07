import os

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import LSTM, Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.utils import to_categorical

# Path for exported data, numpy arrays
PathfileData = os.path.join('LSTM_Data') 

actions = np.array(['Hello', 'Thanks', 'i_love_you'])
squenceLen = 30
label_map = {label:num for num, label in enumerate(actions)}

sequences = []
labels = []
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(PathfileData, action))).astype(int):
        window = []
        for frame_num in range(squenceLen):
            res = np.load(os.path.join(PathfileData, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

np.array(sequences).shape

np.array(labels).shape

X = np.array(sequences)
X.shape

y = to_categorical(labels).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

log_dir = os.path.join('actionRecognitonDataset')
tb_callback = TensorBoard(log_dir=log_dir)

LSTMmodel = Sequential()
LSTMmodel.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
LSTMmodel.add(LSTM(128, return_sequences=True, activation='relu'))
LSTMmodel.add(LSTM(64, return_sequences=False, activation='relu'))
LSTMmodel.add(Dense(64, activation='relu'))
LSTMmodel.add(Dense(32, activation='relu'))
LSTMmodel.add(Dense(actions.shape[0], activation='softmax'))

LSTMmodel.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
LSTMmodel.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])
#LSTMmodel.summary()
#TestOne = LSTMmodel.predict(X_test)
LSTMmodel.save('actionRecognitionLSTMmodel.h5')

## https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed