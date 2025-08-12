import cv2
import numpy as np
import dlib
from math import hypot
from modules.gazeDetection import *

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




while True:
    _, frame = cap.read()
    checker = np.zeros((500, 500, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame)

    for face in faces:
        # x1, y1 = face.left(), face.top()
        # x2, y2 = face.right(), face.bottom()
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        # Detect Blinking
        left_ratio = get_blinking_ratio([36, 39, 37, 38, 40, 41], landmarks)
        right_ratio = get_blinking_ratio([42, 45, 43, 44, 46, 47], landmarks)
        blinking_ratio = (left_ratio + right_ratio) / 2

        if blinking_ratio > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 8, (255, 255, 255))


        # Gaze Detection
        gazeRatio_rightEye = get_gaze_ratio(frame, [42,43,44,45,46,47], landmarks)
        gazeRatio_leftEye = get_gaze_ratio(frame, [36,37,38,39,40,41], landmarks)
        combined_gaze_ratio = (gazeRatio_rightEye + gazeRatio_leftEye) / 2


        cv2.putText(frame, "Ratio: " + str(combined_gaze_ratio), (50, 150), font, 2, (0, 0, 255), 3)
        if combined_gaze_ratio <= 1:
            cv2.putText(frame, "Right", (50, 100), font, 2, (0, 0, 255), 3)
            checker[:] = (0, 0, 255)
        elif 1 < combined_gaze_ratio < 3:
            cv2.putText(frame, "Center", (50, 100), font, 2, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "Left", (50, 100), font, 2, (0, 0, 255), 3)
            checker[:] = (255, 0, 0)

    cv2.imshow("Frame", frame)
    cv2.imshow("Checker", checker)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
