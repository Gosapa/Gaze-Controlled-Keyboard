import numpy as np
from assets.config import *
from modules.logic import *
from modules.keyboard import *

class Keyboard:
    # Variables - General
    status = [0,-1,-1,-1,-1,-1,-1]
    cur_stage = 0
    cur_selection = -1

    # Variables - Binary Search
    total_list = []
    active_list = []
    selection_list = []

    # Main
    def __init__(self):
        self.screen = np.full((SCREEN_HEIGHT, SCREEN_WIDTH, 3), BACKGROUND_COLOR, dtype=np.uint8)
    def update_keyboard(self):
        self.screen = np.full((SCREEN_HEIGHT, SCREEN_WIDTH, 3), BACKGROUND_COLOR, dtype=np.uint8)
        if self.status[0] == 0:
            self.draw_first()
        elif self.status[0] == 1:
            self.draw_second()
        else:
            self.draw_bsearch()
    def update_current_selection(self, cur_selection_in):
        self.cur_selection = cur_selection_in
    def select(self):
        self.update_status()
        returned_characters = character(self.status)

        # Initialize Binary Search UI Variables
        if self.status[0] == 2:
            self.total_list = returned_characters[:]
            self.active_list = self.total_list[:]
            self.part_selections()

        # Update Relevant Variables
        if 2 < self.status[0] < 7:
            self.active_list = self.selection_list[self.cur_selection]
            self.part_selections()

        # Done selecting a character
        if len(returned_characters) == 1:
            self.status = [0, -1, -1, -1, -1, -1, -1]
            # enter(character) # TODO
            return True
        return False

    # Helper Functions
    def update_status(self):
        update_idx = 1
        while self.status[update_idx] != -1:
                update_idx += 1
        self.status[update_idx] = self.cur_selection
        self.status[0] += 1
    def part_selections(self):
        self.selection_list = []
        for i in range (0,2):
            status_tmp = self.status[:]
            update_idx = 1
            while status_tmp[update_idx] != -1:
                update_idx += 1
            status_tmp[update_idx] = i
            status_tmp[0] += 1
            self.selection_list.append(character(status_tmp))

    # Draw Functions
    def draw_first(self):
        box_num = 3
        width = 300
        height = 300
        draw_boxes(self.screen, box_num, width, height, self.cur_selection)

        gap_width = int((SCREEN_WIDTH - box_num * width) / (box_num + 1))
        gap_height = int((SCREEN_HEIGHT - height) / 2)
        offset = 25
        file_order = ["Consonants", "Vowels", "Special"]
        for i in range(0, 3):
            file_name = "./assets/menu/" + file_order[i] + ".png"
            put_menu(self.screen, file_name, gap_width*(i+1) + width*i + offset, gap_height + offset, width - 50, height - 50)
    def draw_second(self):
        box_num = 2
        width = 600
        height = 450
        if self.status[1] == 0:
                draw_boxes(self.screen, box_num, width, height, self.cur_selection)
        elif self.status[1] == 1:
                pass
    def draw_bsearch(self):
        box_num = len(self.total_list)
        width = 100
        height = 100
        draw_boxes(self.screen, box_num, width, height, self.selection_list[self.cur_selection])
