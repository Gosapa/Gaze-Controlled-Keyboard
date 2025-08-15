import cv2
import numpy as np
import dlib
from assets.config import DEBUG_MODE

def select(status, selection):
    update_status(status, selection)
    returned_character = character(status)
    print(returned_character)
    if len(returned_character) == 1:
        if DEBUG_MODE:
            print("(DEBUG) IN function `select`: Completed entering a character")
        enter(character)
        status[:] = [0, -1, -1, -1, -1, -1, -1]
        return True
    return False

    if DEBUG_MODE:
        print("(DEBUG) Selection Ended Successfully")

def update_status(status, selection):
    update_idx = 1
    while status[update_idx] != -1:
        update_idx += 1
        # if DEBUG_MODE:
            # print("(DEBUG) Whlie loop in update_status")
            # print("(DEBUG) Current update_idx: " + str(update_idx))
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
        return find_bsearch_vowel(status[2:])
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
    if DEBUG_MODE:
        print("(DEBUG) In function `find_bsearch_consonant`: idx: " + str(idx))
    if len(final_range) == 1 and selections[4] == -1 and is_special(left):
        final_range.append(correspondance(left))
    elif len(final_range) == 1 and selections[4] != -1 and is_special(left):
        if selections[idx] == 1:
            final_range[0] = correspondance(left)
    return final_range

def find_bsearch_vowel(selections):
    left = 14
    right = 23
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
    if DEBUG_MODE:
        print("(DEBUG) In function `find_bsearch_consonant`: idx: " + str(idx))
    if len(final_range) == 1 and selections[4] == -1 and is_special(left):
        final_range.append(correspondance(left))
    elif len(final_range) == 1 and selections[4] != -1 and is_special(left):
        if selections[idx] == 1:
            final_range[0] = correspondance(left)
    return final_range


def is_special(character):
    # Add Vowels too
    SPECIAL_CHARACTERS = [0, 2, 5, 6, 8]
    return character in SPECIAL_CHARACTERS

def correspondance(character):
    SPECIAL_DICT = {0: 24,
                    2: 25,
                    5: 26,
                    6: 27,
                    8: 28}
    return SPECIAL_DICT[character]

# TODO Simulate Keyboard Input
def enter(character):
    pass
