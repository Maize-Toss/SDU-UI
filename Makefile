# Makefile for PyInstaller

PY_SCRIPT = display.py
ICON_FILE = maize_toss.ico
OUTPUT_DIR = dist

.PHONY: all clean

all: build

build:
	pyinstaller --onefile --icon=$(ICON_FILE) $(PY_SCRIPT)

clean:
	rm -rf $(OUTPUT_DIR)
	rm -rf __pycache__
	rm -f *.spec
