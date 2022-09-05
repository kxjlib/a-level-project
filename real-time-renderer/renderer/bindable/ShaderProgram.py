# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# ShaderProgram.py

# The ShaderProgram class needs to
#   - control file operations to input a shader.
#   - control storage of the shader program


class ShaderProgram(object):
    # Variables to be used in the class
    _filename = ""
    _program = None

    # Assumes that the filename will have a .vert and .frag variant
    @classmethod
    def from_filename(cls, gl_ctx, filename):
        # Vertex Shader
        vert_source = ""
        with open(filename + '.vert', 'r') as fs:
            vert_source = fs.read()
        
        # Fragment Shader
        frag_source = ""
        with open(filename + '.frag', 'r') as fs:
            frag_source = fs.read()
        
        return cls(gl_ctx, vert_source, frag_source)
    
    def __init__(self, gl_ctx, vert_src, frag_src):
        # Create the Shader Program.
        self._program = gl_ctx.program(vertex_shader=vert_src,fragment_shader=frag_src)

    # Get item dunder function
    # Will allow the class to be called like a dictionary
    # Meaning we can call the value of uniforms, like the ctx.program class allows
    def __getitem__(self, key):
        return self._program[key]
    

    # Will return the program instance when called, however cannot be overwritten
    @property
    def inst(self):
        return self._program