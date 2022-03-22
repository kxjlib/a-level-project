CXX       := g++
CXX_FLAGS := -std=c++17 -ggdb -Wall

BIN     := bin
SRC     := src
INCLUDE := include

LIBRARIES   := -lglfw3dll -lopengl32
EXECUTABLE  := a.exe


all: $(BIN)/$(EXECUTABLE)

run: clean all
	clear
	./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*.c*
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE) $^ -o $@ $(LIBRARIES)

clean:
	-rm $(BIN)/*