import os
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

current_letter = 'A'
end_letter = 'Z'
dataset_size = 100

cap = cv2.VideoCapture(0)
for i in range(35):    
    if not os.path.exists(os.path.join(DATA_DIR, str(i))):
        os.makedirs(os.path.join(DATA_DIR, str(i)))

    # Making the increment in the Alphebet for easier labeling of the folders.
    # current_letter = chr(ord(current_letter) + 1)

    print('Collecting data for class {}'.format(i))
    
    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Press X to collect data!', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('Dataset Collection Tool', frame)
        if cv2.waitKey(25) == ord('x'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('Dataset Collection Tool', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(i), '{}.jpg'.format(counter)), frame)

        counter += 1


cap.release()
cv2.destroyAllWindows()
