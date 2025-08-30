import cv2
from PIL import ImageFont, ImageDraw, Image
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

    gap_width = int((SCREEN_WIDTH - num * width) / (num + 1))
    gap_height = int((SCREEN_HEIGHT - height) / 2)
    for i in range(0, num):
        x1 = gap_width * (i + 1) + width * (i) + SELECTION_SCREEN_X1
        y1 = gap_height
        x2 = gap_width * (i + 1) + width * (i + 1) + SELECTION_SCREEN_X1
        y2 = gap_height + height

        current_color = SELECTION_COLOR if i in selections_to_check else DEFAULT_COLOR

        cv2.rectangle(screen, (x1, y1), (x2, y2), current_color, -1)
def draw_boxes_bsearch(screen, total_list, width, height, selection_list, active_list):
    num = len(total_list)
    error_bool = (num * width > SCREEN_WIDTH or
                  height > SCREEN_HEIGHT)
    if error_bool:
        print("Error in function `draw_boxes`")
        return

    gap_width = int((SCREEN_WIDTH - num * width) / (num + 1))
    gap_height = int((SCREEN_HEIGHT - height) / 2)
    for i in range(len(total_list)):
        x1 = gap_width * (i + 1) + width * (i) + SELECTION_SCREEN_X1
        y1 = gap_height
        x2 = gap_width * (i + 1) + width * (i + 1) + SELECTION_SCREEN_X1
        y2 = gap_height + height

        if total_list[i] in selection_list:
            current_color = SELECTION_COLOR
        elif total_list[i] in active_list:
            current_color = DEFAULT_COLOR
        else:
            current_color = DEACTIVATED_COLOR
        cv2.rectangle(screen, (x1, y1), (x2, y2), current_color, -1)


def put_letter(background_img, korean_index, x, y, w, h):
    file_name = "./assets/KOR-Characters/" + str(korean_index) + ".png"
    letter_img_raw = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    letter_img = cv2.resize(letter_img_raw, (int(0.75 * w) , int(0.75 * h)))
    put_transparent_image(background_img, letter_img, int(x + 0.25 * w), int(y + 0.25 * h))

def put_letter_font(screen, text, position, font_size):
    font_path = "./assets/nanum-kor.ttf"
    img_pil = Image.fromarray(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error: Font file not found at {font_path}")
        return screen
    draw.text(position, text, font=font, fill=(0,0,0))
    screen_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    screen[:] = screen_with_text

