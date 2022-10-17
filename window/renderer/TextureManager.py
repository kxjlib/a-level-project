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
    def from_image(cls, ctx, filename, regname):
        img = Image.open(pathlib.Path(
            __file__).parent.resolve().as_posix() + f"/../assets/{filename}").convert('RGBA')
        
        tex = ctx.texture(img.size, 4, img.tobytes())
        cls.from_tex(tex, regname)
    
    @classmethod
    def from_tex(cls, tex, regname):
        if cls.Textures.get(regname):
            cls.Textures[regname].release()
        cls.Textures[regname] = tex


    # Only change the texture if it is necessary
    @classmethod
    def use(cls, tex_name):
        if cls.current_texture != tex_name:
            cls.Textures[tex_name].use()
            cls.current_texture = tex_name
