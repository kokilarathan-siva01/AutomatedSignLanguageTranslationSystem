import cv2
import mediapipe as mp
import numpy as np
from tensorflow.python.keras.models import load_model


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def probabilityCal(res, actions, input_frame):
    finalFrame = input_frame.copy()
    max_text_width = 0 

    for index, probability in enumerate(res):
        text = f"{actions[index]}: {probability:.2f}"
        text_width, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

        if text_width > max_text_width:
            max_text_width = text_width

    for index, probability in enumerate(res):
        y = 60 + index * 40
        x1 = max_text_width + 10
        x2 = x1 + int(probability * 100)
        cv2.putText(finalFrame, f"{actions[index]}: {probability:.2f}", (x1 + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return finalFrame

def getKeypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

def runAction():
   # Using the trained model from previous step as the base for probability prediction.
    model = load_model('actionRecognitionModel.h5')

    # Trained Actions that can be used.
    actions = ['Hello', 'Thanks', 'I Love You']
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5
    box_coords = (100, 10, 100, 50)
    box_color = (255, 0, 0)
    cap = cv2.VideoCapture(0)

    # initate mediapipe holistic model
    mp_holistic = mp.solutions.holistic

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            # Read feed
            ret, frame = cap.read()

            # Make detections
            image, results = mediapipe_detection(frame, holistic)


            # Prediction logic
            keypoints = getKeypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
                predictions.append(np.argmax(res))

                # Add recognized action to the sentence
                if np.unique(predictions[-10:])[0] == np.argmax(res):
                    if res[np.argmax(res)] > threshold:
                        if len(sentence) > 0:
                            if actions[np.argmax(res)] != sentence[-1]:
                                sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])
                            

                if len(sentence) > 5:
                    sentence = sentence[-5:]

                
                image = probabilityCal(res, actions, image)

                # Calculate the text width and height
                text_size = cv2.getTextSize(' '.join(sentence), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_width = text_size[0]
                text_height = text_size[1]

                # Calculate the position for the rectangle and text
                rect_x = (image.shape[1] - text_width) // 2 - 5 
                rect_y = image.shape[0] - text_height - 10
                text_x = rect_x + 5 
                text_y = rect_y + text_height - 5 

                # Draw the rectangle and text at the new positions
                cv2.rectangle(image, (rect_x, rect_y), (rect_x + text_width + 10, rect_y + text_height + 10), (188, 238, 144), -1)
                cv2.putText(image, ' '.join(sentence), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)


            # Show to screen
            cv2.imshow('Action Recognition', image)
            
            if cv2.waitKey(25) & 0xFF == ord('x'):
                with open("Action's Sentence.txt", "w") as file: # writes down the last formed sentence into a text file.
                    file.write(" ".join(sentence))
                break

    cap.release()
    cv2.destroyAllWindows()
