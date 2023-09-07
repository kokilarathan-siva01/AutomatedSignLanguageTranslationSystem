import os
import pickle
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


handsGUI = mp.solutions.hands

hands = handsGUI.Hands(static_image_mode=True, min_detection_confidence=0.3)
PathFileData = './data'

data = []
labels = []
for i in os.listdir(PathFileData):
    # Exclude .DS_Store files
    if i == ".DS_Store":
        continue
    for pathImage in os.listdir(os.path.join(PathFileData, i)):
        data_aux = []

        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(PathFileData, i, pathImage))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            data.append(data_aux)
            labels.append(i)

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
