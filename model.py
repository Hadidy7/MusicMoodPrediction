import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score

from spotifyAPI import *

df = pd.read_csv("music_mood_dataset.csv")

col_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
X = MinMaxScaler().fit_transform(df[col_features])
X2 = np.array(df[col_features])
Y = df['mood']

encoder = LabelEncoder()
encoder.fit(Y)
encoded_y = encoder.transform(Y)
dummy_y = np_utils.to_categorical(encoded_y)

X_train, X_test, Y_train, Y_test = train_test_split(X, encoded_y, test_size=0.2, random_state=15)

target = pd.DataFrame({'mood': df['mood'].tolist(), 'encode': encoded_y}).drop_duplicates().sort_values(['encode'], ascending=True)


def build_model():
    model = Sequential()
    model.add(Dense(9, input_dim=9, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


estimator = KerasClassifier(build_fn=build_model, epochs=100, batch_size=64, verbose=0)

kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, encoded_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

estimator.fit(X_train, Y_train)
y_preds = estimator.predict(X_test)


def predict_mood(id_song):
    pip = Pipeline([('minmaxscaler', MinMaxScaler()), ('keras', KerasClassifier(build_fn=build_model, epochs=100,
                                                                                 batch_size=64, verbose=0))])
    pip.fit(X2, encoded_y)
    # Obtain the features of the song using get_songs_features() function

    preds = get_songs_features(id_song)
    preds_features = np.array(preds[0][7:-1]).reshape(1, -1)
    results = pip.predict(preds_features)

    mood = np.array(target['mood'][target['encode'] == int(results)])
    name_song = preds[0][1]
    artist = preds[0][2]

    return name_song, artist, mood[0]

