# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# main.py

# Imports
import sys
from Application import Application

# Guard clause to close the program if it's imported
# We do this instead of sticking all the code in a main function for cleanliness
if __name__ != "__main__":
    sys.exit(-1)

app = Application("Real-Time Renderer", (800,600))
app.run()