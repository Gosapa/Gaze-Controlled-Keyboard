import cv2
import numpy as np
import dlib

def select(status, selection):
    pass

def update_status(status=[0,0,0,0,0,0,0], cur_index=0):
    pass

def find_bsearch_consonant(selections):
    left = 0, right = 14
    idx = 0
    while left + 1 < right:
        mid = left + int((right - left - 1) / 2)
        if selections[index] == 0:
            right = mid + 1
        elif selecitons[index] == 1:
            left = mid + 1
        else:
            break
        ++index
    final_range = list(range(left, right))
    return final_range
