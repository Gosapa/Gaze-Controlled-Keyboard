import cv2
import numpy as np
import dlib
from modules.gazeDetection import *
# from modules.keyboard import *
from modules.keyboard_c import *
from assets.config import *
from modules.logic import *

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cur_frame = 0
cur_selection = 0
gaze_direction = 0

blinked = False
blink_frozen = False

keyboard = Keyboard()
keyboard.update_keyboard()

while True:
    blinked = False
    _, frame = cap.read()
    checker = np.zeros((500, 500, 3), np.uint8) # Giant Screen that indicates the direction of gaze
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Gray version of BGR image

    faces = detector(frame)
    # print(len(faces))

    # Find Gaze
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
            blinked = True
            cv2.putText(frame, "BLINKING", (50, 150), font, 8, (255, 255, 255))


        # Gaze Detection
        gazeRatio_rightEye = get_gaze_ratio(frame, [42,43,44,45,46,47], landmarks)
        gazeRatio_leftEye = get_gaze_ratio(frame, [36,37,38,39,40,41], landmarks)
        combined_gaze_ratio = (gazeRatio_rightEye + gazeRatio_leftEye) / 2


        cv2.putText(frame, "Ratio: " + str(combined_gaze_ratio), (50, 150), font, 2, (0, 0, 255), 3)
        looking_right = (combined_gaze_ratio <= RIGHT_GAZE_THRESHOLD)
        looking_left = (LEFT_GAZE_THRESHOLD < combined_gaze_ratio )
        if looking_right:
            cv2.putText(frame, "Right", (50, 100), font, 2, (0, 0, 255), 3)
            checker[:] = (0, 0, 255)
            gaze_direction = 1
        elif looking_left:
            cv2.putText(frame, "Left", (50, 100), font, 2, (0, 0, 255), 3)
            checker[:] = (255, 0, 0)
            gaze_direction = -1
        else:
            cv2.putText(frame, "Center", (50, 100), font, 2, (0, 0, 255), 3)
            gaze_direction = 0

    unfreeze_frame = (blink_frozen and cur_frame % BLINK_FREEZE_THRESHOLD == 0)
    blink_select = (blinked and not blink_frozen)
    gaze_move_index = (cur_frame % FRAME_THRESHOLD == 0)


    # Blink - Selection Logic
    if (blink_select):
        blinked = False
        blink_frozen = True
        cur_frame = 0
        if DEBUG_MODE:
            print("(DEBUG) Selected")
            print("(DEBUG) Current status: " + str(keyboard.status))
        keyboard.select()
        keyboard.update_keyboard()
        cur_selection = 0
        if DEBUG_MODE:
            print("(DEBUG) After Selection: " + str(keyboard.status))
    if (unfreeze_frame):
        blink_frozen = False
        blinked = False
        cur_frame = 0
        print("Unfroze")

    # Updates current selection according to the gaze
    if (gaze_move_index):
        change_in_selection = False
        if 0 <= cur_selection + gaze_direction < MAX_SELECTION_STAGE[keyboard.status[0]]:
            cur_selection += gaze_direction
            keyboard.update_current_selection(cur_selection)
            keyboard.update_keyboard()
        print("Selection: " + str(cur_selection))
        cur_frame = (cur_frame % BLINK_FREEZE_THRESHOLD)


    cv2.imshow("Frame", frame)
    # cv2.imshow("Checker", checker)
    cv2.imshow("Keyboard", keyboard.screen)

    cur_frame += 1
    # print(cur_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
