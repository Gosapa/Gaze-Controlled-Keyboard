import cv2
import numpy as np
import dlib
from assets.config import DEBUG_MODE

def select(status, selection):
    update_status(status, selection)
    print(character(status))

    if DEBUG_MODE:
        print("(DEBUG) Selection Ended Successfully")

def update_status(status, selection):
    update_idx = 1
    while status[update_idx] != -1:
        update_idx += 1
        if DEBUG_MODE:
            print("(DEBUG) Whlie loop in update_status")
            print("(DEBUG) Current update_idx: " + str(update_idx))
    status[update_idx] = selection
    status[0] += 1

def character(status):
    if status[0] == 0:
        print("ERROR: No type selected")
        return
    # Consonant
    if status[1] == 0:
        return find_bsearch_consonant(status[2:])
    # Vowel
    elif status[1] == 1:
        pass
    # Special
    else:
        pass

def find_bsearch_consonant(selections):
    left = 0
    right = 14
    idx = 0
    while left + 1 < right:
        mid = left + int((right - left - 1) / 2)
        if selections[idx] == 0:
            right = mid + 1
        elif selections[idx] == 1:
            left = mid + 1
        else:
            break
        idx += 1
    final_range = list(range(left, right))
    return final_range

def is_special(character):
    # Add Vowels too
    SPECIAL_CHARACTERS = [0, 2, 5, 6, 8]
    SPECIAL_DICT = {0: 24,
                    2: 25,
                    5: 26,
                    6: 27,
                    8: 28}
