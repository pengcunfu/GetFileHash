# File SHA-256 Calculator

A graphical interface tool based on PySide6 for calculating file SHA-256 hash values.

## Features

- 🎨 Modern graphical user interface
- 📊 Progress display for large file calculations
- 📋 One-click copy hash value to clipboard
- 🚀 Support for files of any size
- 💻 Cross-platform support (Windows, Linux, macOS)

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Program

### Run Python Script Directly

```bash
python get_file_sha256.py
```

### Package as Executable

Use the provided build.py script for packaging:

```bash
python build.py
```

After packaging is complete, the executable file will be located in the `dist` directory.

## Packaging Instructions

The `build.py` script will automatically:
1. Check if PyInstaller is installed
2. Clean previous build files
3. Use PyInstaller to package the program
4. Generate a single-file executable (can run without Python environment)

### Custom Packaging Options

Edit the `pyinstaller_args` list in `build.py` to modify packaging options:

- `--name`: Executable file name
- `--onefile`: Package into a single file
- `--windowed`: Windows GUI program (no console display)
- `--icon`: Specify icon file (.ico format)

## Usage

1. Click the "Select File" button to choose the file for hash calculation
2. Click the "Calculate SHA-256" button to start calculation
3. Wait for calculation to complete (progress bar will show for large files)
4. Click the "Copy to Clipboard" button to copy the hash value

## Tech Stack

- Python 3.x
- PySide6 (Qt for Python)
- PyInstaller (Packaging tool)

## License

MIT License
