import cv2
import numpy as np
from modules.keyboard import *


# keyboard = np.zeros((1000, 1500, 3), np.uint8)
keyboard = np.full((1000, 1500, 3), [255, 255, 255], dtype=np.uint8)

draw_keyboard(keyboard)

cv2.imshow("keyboard", keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
