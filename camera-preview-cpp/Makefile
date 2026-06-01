CXX ?= c++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Wpedantic

all: camera_preview

camera_preview: main.cpp
	$(CXX) $(CXXFLAGS) main.cpp -o camera_preview

clean:
	rm -f camera_preview
