import cv2
import numpy as np

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

def draw_keyboard(background_img):
    put_letter(background_img, 0, 0, 0, 100, 100)
    put_letter(background_img, 1, 100, 0, 100, 100)

def put_letter(background_img, korean_index, x, y, w, h):
    file_name = "./assets/KOR-Characters/" + str(korean_index) + ".png"
    letter_img_raw = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    letter_img = cv2.resize(letter_img_raw, (int(0.75 * w) , int(0.75 * h)))
    put_transparent_image(background_img, letter_img, int(x + 0.25 * w), int(y + 0.25 * h))
