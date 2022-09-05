# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# TextureManager.py

# This class needs to:
#   - Store all textures used by the program
#   - Have a numbered reference to each
#   - Allow for more to be opened

from PIL import Image
import pathlib


class TextureManager(object):
    # Variables used by the class
    Textures = {}
    current_texture = ""


    @classmethod
    def from_image(cls, ctx, filename, regname, channels):
        img = Image.open(pathlib.Path(
            __file__).parent.resolve().as_posix() + f"/../assets/{filename}")
        
        tex = ctx.texture(img.size, channels, img.tobytes())

        cls.Textures[regname] = tex
    
    # Only change the texture if it is necessary
    @classmethod
    def use(cls, tex_name):
        if cls.current_texture != tex_name:
            cls.Textures[tex_name].use()
            cls.current_texture = tex_name
