# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# TextButton.py

from .Text import Text
from .InputManager import Input
import moderngl

class TextButton(Text):
    def __init__(self, gl_ctx: moderngl.Context, contents, colour, size, text_name, x, y):
        super().__init__(gl_ctx, contents, colour, size, text_name, x, y)
    
    def is_clicked(self):
        mouse_pos = Input.mouse_to_screen()
        x, y = self.pos
        w, h = self.size
        if x - w/2 <= mouse_pos[0] <= x + w/2 and y - h/2 <= mouse_pos[1] <= y + h/2:
            return Input.MPressed.get(1) and not Input.lMPressed.get(1)
        return False