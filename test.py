from modules.logic import *
from modules.keyboard_c import *


keyboard = Keyboard()

print(keyboard.status)

keyboard.cur_selection = 2
keyboard.select()
print(keyboard.status)

print(character([1,0,-1,-1,-1,-1,-1]))
