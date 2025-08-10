import cv2
import numpy as np
import dlib
from math import hypot

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint (p1, p2):
    return (int((p1.x + p2.x)/2), int((p1.y + p2.y)/2))


def get_blinking_ratio(eyepoints, facial_landmarks):
    leftPoint = (facial_landmarks.part(eyepoints[0]).x, facial_landmarks.part(eyepoints[0]).y)
    rightPoint = (facial_landmarks.part(eyepoints[1]).x, facial_landmarks.part(eyepoints[1]).y)
    # hor_line = cv2.line(frame, leftPoint, rightPoint, (0, 255, 0), 2)

    topPoint = midpoint(facial_landmarks.part(eyepoints[2]), facial_landmarks.part(eyepoints[3]))
    botPoint = midpoint(facial_landmarks.part(eyepoints[4]), facial_landmarks.part(eyepoints[5]))
    # vert_line = cv2.line(frame, topPoint, botPoint, (0, 0, 255), 2)

    hor_line_length = hypot(rightPoint[0] - leftPoint[0], rightPoint[1] - leftPoint[1])
    ver_line_length = hypot(topPoint[0] - botPoint[0], topPoint[1] - botPoint[1])

    ratio = hor_line_length / ver_line_length

    return ratio


while True:
    _, frame = cap.read()
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
        left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                    (landmarks.part(37).x, landmarks.part(37).y),
                                    (landmarks.part(38).x, landmarks.part(38).y),
                                    (landmarks.part(39).x, landmarks.part(39).y),
                                    (landmarks.part(40).x, landmarks.part(40).y),
                                    (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])

        eye = frame[min_y: max_y, min_x: max_x]
        gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

        eye = cv2.resize(eye, None, fx=5, fy=5)
        threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
        cv2.imshow("Eye", eye)
        cv2.imshow("Threshold", threshold_eye)

        cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
