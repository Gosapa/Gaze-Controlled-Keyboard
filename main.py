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

def get_gaze_ratio(eye_points, facial_landmarks):
    # Gaze Detection
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    # Mask
    frame_height, frame_width, _ = frame.shape
    mask = np.zeros((frame_height, frame_width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye_mask = cv2.bitwise_and(gray, gray, mask=mask)

    grayed_eye = eye_mask[min_y: max_y, min_x: max_x]

    _, threshold_eye = cv2.threshold(grayed_eye, 70, 255, cv2.THRESH_BINARY)
    threshold_height, threshold_width = threshold_eye.shape
    leftHalf_threshold = threshold_eye[0: threshold_height, 0: int(threshold_width / 2)]
    rightHalf_threshold = threshold_eye[0: threshold_height, int(threshold_width / 2): threshold_width]

    leftHalf_whiteCount = cv2.countNonZero(leftHalf_threshold)
    rightHalf_whiteCount = cv2.countNonZero(rightHalf_threshold)

    eye = cv2.resize(grayed_eye, None, fx=5, fy=5)
    threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
    cv2.imshow("Threshold", threshold_eye) # Black & White Image

    cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)
    if rightHalf_whiteCount == 0:
        gaze_ratio_ltr = 1
    else:
        gaze_ratio_ltr = leftHalf_whiteCount / rightHalf_whiteCount

    return gaze_ratio_ltr

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
        gazeRatio_rightEye = get_gaze_ratio([42,43,44,45,46,47], landmarks)
        gazeRatio_leftEye = get_gaze_ratio([36,37,38,39,40,41], landmarks)

        cv2.putText(frame, "Left: " + str(gazeRatio_leftEye), (50, 100), font, 2, (0, 0, 255), 3)
        cv2.putText(frame, "Right: " + str(gazeRatio_rightEye), (50, 150), font, 2, (0, 0, 255), 3)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
