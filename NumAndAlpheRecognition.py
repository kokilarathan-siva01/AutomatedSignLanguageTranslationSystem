import pickle
import cv2
import mediapipe as mp
import numpy as np


def NumAlpheRecognition():
    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']

    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    # A dictionary for numbers 0-9 and English alphabet letters
    labels_dict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
                20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
                30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}

    while True:
        allData = []
        xValue = []
        yValue = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        outputs = hands.process(frame_rgb)
        if outputs.multi_hand_landmarks:
            for hand_landmarks in outputs.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    xValue.append(x)
                    yValue.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    allData.append(x - min(xValue))
                    allData.append(y - min(yValue))

            x1 = int(min(xValue) * W) - 10
            y1 = int(min(yValue) * H) - 10

            x2 = int(max(xValue) * W) - 10
            y2 = int(max(yValue) * H) - 10

            prediction = model.predict([np.asarray(allData)])

            probabilityPrediction = labels_dict[int(prediction[0])]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (144, 238, 144), 10)
            cv2.putText(frame, probabilityPrediction, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

        cv2.imshow('Number & Alphabet Recognition', frame)
        cv2.waitKey(1)
        if cv2.waitKey(10) == ord('x'):
            break

    cap.release()
    cv2.destroyWindow()
