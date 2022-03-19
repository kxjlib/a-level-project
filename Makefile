CXX       := g++
CXX_FLAGS := -std=c++17 -ggdb -Wall

BIN     := bin
SRC     := src
INCLUDE := include

LIBRARIES   := -lglfw -lGL
EXECUTABLE  := a.out


all: $(BIN)/$(EXECUTABLE)

run: clean all
	clear
	./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*.c*
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE) $^ -o $@ $(LIBRARIES)

clean:
	-rm $(BIN)/*