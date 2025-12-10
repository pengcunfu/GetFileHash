# GetFileHash - Hash Calculator

A modern graphical interface tool based on PySide6 for calculating file and text hash values.

## ✨ Features

- 🎨 **Modern Graphical User Interface** - Based on PySide6 (Qt for Python)
- 🔄 **Multiple Hash Algorithm Support** - MD5, SHA-1, SHA-256, SHA-384, SHA-512
- 📊 **Large File Progress Display** - Real-time calculation progress
- 📋 **One-Copy Function** - Quickly copy hash values to clipboard
- 📝 **Text Hash Calculation** - Support for calculating text content hash values
- 🖱️ **File Drag & Drop** - Directly drag files to the interface for calculation
- 🚀 **High Performance** - Support for files of any size
- 💻 **Cross-Platform Support** - Windows, Linux, macOS
- 📦 **Convenient Distribution** - Provides installer and portable versions

## 🚀 Quick Start

### Download and Installation

#### 📦 Recommended Download: Installer Version
- **File Name**: `GetFileHash-Setup-{VERSION}.exe`
- **Description**: Complete Windows installer with uninstall functionality
- **Advantages**: Automatically creates desktop shortcuts, start menu items, supports program uninstallation

#### 🗂️ Portable Version
- **File Name**: `GetFileHash-{VERSION}.zip`
- **Description**: Green portable version, extract and use
- **Advantages**: No installation required, does not write to registry, suitable for USB drives

Download the latest version from the [Releases page](https://github.com/pengcunfu/GetFileHash/releases).

### System Requirements
- Windows 10 and above
- **Recommended**: Installer version requires administrator privileges for installation
- **Portable**: No special permissions required

## 💻 Development Environment

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Program

```bash
python main.py
```

### Build Executable

```bash
# Build Windows executable
python scripts/build.py

# Build Windows installer
python scripts/build_installer.py
```

## 📖 Usage Instructions

### File Hash Calculation
1. Click the "Select File" button or directly drag files to the interface
2. Select the required hash algorithm (default SHA-256)
3. Click the "Calculate Hash" button
4. Wait for calculation to complete (progress bar shows for large files)
5. Click "Copy to Clipboard" to copy the result

### Text Hash Calculation
1. Switch to the "Text Hash" tab
2. Enter or paste text in the text box
3. Select hash algorithm
4. Click "Calculate Hash" button
5. Copy calculation result

## 🛠️ Tech Stack

- **Python 3.9** - Core development language
- **PySide6** - GUI framework (Qt for Python)
- **Nuitka** - Compilation tool for generating high-performance executables
- **Inno Setup** - Windows installer creation

## 📁 Project Structure

```
GetFileHash/
├── main.py                 # Main program entry
├── requirements.txt        # Python dependencies
├── resources/             # Resource files
│   └── icon.png          # Application icon
├── scripts/               # Build scripts
│   ├── build.py          # Build executable
│   └── build_installer.py # Build installer
├── scripts/installer.iss  # Inno Setup configuration
└── .github/workflows/     # CI/CD workflows
    ├── ci.yml            # Continuous integration
    └── release.yml       # Auto release
```

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PySide6](https://doc.qt.io/qtforpython/) - Excellent Python GUI framework
- [Nuitka](https://nuitka.net/) - Powerful Python compiler
- [Inno Setup](https://jrsoftware.org/isinfo.php) - Professional installer creation tool

---

<p align="center">
  <strong>If this project helps you, please give it a ⭐ Star to support!</strong>
</p>
