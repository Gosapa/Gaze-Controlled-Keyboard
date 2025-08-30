import cv2
import numpy as np
from assets.config import *
from .logic import *

def put_transparent_image(background_img, overlay_img, x, y):
    # background_img = background_img.copy()
    h, w = overlay_img.shape[:2]

    # Define the Region of Interest (ROI) on the background
    # Ensure the ROI is within the bounds of the background image
    y_end = min(y + h, background_img.shape[0])
    x_end = min(x + w, background_img.shape[1])
    h = y_end - y
    w = x_end - x

    # Crop the overlay if it goes past the background's edge
    overlay_img = overlay_img[0:h, 0:w]

    roi = background_img[y:y_end, x:x_end]

    if overlay_img.shape[2] == 3: # Case for a standard 3-channel BGR image
        roi[:] = overlay_img
    else: # Case for a 4-channel BGRA image
        # 1. Split the overlay into color and alpha channels
        overlay_bgr = overlay_img[:, :, :3]
        overlay_alpha = overlay_img[:, :, 3]

        # 2. Create a boolean mask where alpha is not zero
        # This mask will be True for all non-transparent pixels
        mask = overlay_alpha != 0

        # 3. Use the mask to place the overlay pixels onto the ROI
        # roi[mask] selects all pixels in the ROI that correspond to
        # a True value in the mask.
        # overlay_bgr[mask] selects the corresponding pixels from the overlay.
        roi[mask] = overlay_bgr[mask]

    return background_img

def draw_keyboard(screen, status, cur_selection):
    # Stage 0: Selecting Consonant / Vowel / Special
    if status[0] == 0:
        draw_first(screen, status, cur_selection)
    # Stage 1: Selecting first stage
    elif status[0] == 1:
        draw_second(screen, status, cur_selection)
    else:
        draw_bsearch(screen, status, cur_selection)

def draw_first(screen, status, cur_selection):
    box_num = 3
    width = 300
    height = 300
    draw_boxes(screen, box_num, width, height, cur_selection)

    gap_width = int((SCREEN_WIDTH - box_num * width) / (box_num + 1))
    gap_height = int((SCREEN_HEIGHT - height) / 2)
    offset = 25
    file_order = ["Consonants", "Vowels", "Special"]
    for i in range(0, 3):
        file_name = "./assets/menu/" + file_order[i] + ".png"
        put_menu(screen, file_name, gap_width*(i+1) + width*i + offset, gap_height + offset, width - 50, height - 50)

def draw_second(screen, status, cur_selection):
    box_num = 2
    width = 600
    height = 450
    if status[1] == 0:
        # Show 0 ~ 6 / 7 ~ 13
        draw_boxes(screen, box_num, width, height, cur_selection)
        pass
    elif status[1] == 1:
        # Show 14 ~ 18 / 19 ~ 23
        pass

def draw_bsearch(screen, status, cur_selection):
    full_range = get_range(status)
    cur_selection = character(status)
    # Iterate by the length of `full_range`, draw unselected boxes and selected boxes
    # put_letter(background_img, 0, 0, 0, 100, 100)
    # put_letter(background_img, 1, 100, 0, 100, 100)
    pass

def get_range(status):
    ret = []
    # If consonants
    if status[1] == 0:
        # If left half
        if status[2] == 0:
            ret = list(range(0, 7))
        elif status[2] == 1:
            ret = list(range(7, 14))
    elif status[1] == 1:
        if status[2] == 0:
            ret = list(range(14, 19))
        elif status[2] == 1:
            ret = list(range(19, 24))
    else:
        pass
    return ret

def put_menu(screen, file_name, start_x, start_y, w, h):
    letter_img_raw = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    letter_img = cv2.resize(letter_img_raw, (w, h))
    put_transparent_image(screen, letter_img, start_x, start_y)

def draw_boxes(screen, num, width, height, cur_selection):
    error_bool = (num * width > SCREEN_WIDTH or
                  height > SCREEN_HEIGHT)
    if error_bool:
        print("Error in function `draw_boxes`")
        return

    selections_to_check = set(cur_selection) if isinstance(cur_selection, list) else {cur_selection}
    if isinstance(cur_selection, list):
        print(cur_selection)

    gap_width = int((SCREEN_WIDTH - num * width) / (num + 1))
    gap_height = int((SCREEN_HEIGHT - height) / 2)
    for i in range(0, num):
        x1 = gap_width * (i + 1) + width * (i) + SELECTION_SCREEN_X1
        y1 = gap_height
        x2 = gap_width * (i + 1) + width * (i + 1) + SELECTION_SCREEN_X1
        y2 = gap_height + height

        current_color = SELECTION_COLOR if i in selections_to_check else DEFAULT_COLOR

        cv2.rectangle(screen, (x1, y1), (x2, y2), current_color, -1)

def put_letter(background_img, korean_index, x, y, w, h):
    file_name = "./assets/KOR-Characters/" + str(korean_index) + ".png"
    letter_img_raw = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    letter_img = cv2.resize(letter_img_raw, (int(0.75 * w) , int(0.75 * h)))
    put_transparent_image(background_img, letter_img, int(x + 0.25 * w), int(y + 0.25 * h))
