<p align="center"><img src='app/assets/icono.ico' alt="Traductor-inador">

<h1 align="center">Traductor-inador</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12.5-%233498DB" alt="Python">
  <img src="https://img.shields.io/badge/PyQt6-6.9.0-%232ECC71" alt="PyQt6">
  <img src="https://img.shields.io/badge/PyInstaller-6.9.0-%23F1C40F" alt="PyInstaller">
  <img src="https://img.shields.io/badge/python--docx-1.1.2-%23E74C3C" alt="python-docx">
  <img src="https://img.shields.io/badge/sphinx-1.1.2-%239B59B6" alt="sphinx">
</p>

Professional desktop application for advanced translation of text and DOCX documents with format preservation.

## Table of Contents 📑

- [Features](#main-features-)
- [Installation](#installation-)
- [Usage](#basic-usage-)
  - [Text](#text-translation)
  - [Documents](#document-translation)
- [Structure](#project-structure-)
- [Executable](#download-executable-)

## Main Features ✨

### 🔠 Text Translation
- Text editor-style interface
- Support for 7+ languages
- Real-time translation
- Preservation of spaces and line breaks

### 📄 Document Translation
- DOCX file processing
- Maintains:
  - Text formatting
  - Paragraph styles
  - Tables and lists
  - Hyperlinks
- Integrated progress bar

### ⚙️ Configuration
- Engine selection:
  - MyMemory (free, default)
  - DeepL (professional accuracy)
  - Google Translate
  - Magic Loops (URL required)
- Centralized API Key management
- Theme system:
  - Dark/Light mode

## Installation 📦

Clone the repository
```console
$ git clone https://github.com/MisaelRodriguez3/Traductor-inador.git
```

Enter the project folder
```console
$ cd Traductor-inador
```

Create a virtual environment
```console
$ python -m venv .venv
```

Activate the virtual environment
```console
$ .venv\Scripts\activate # Windows
$ source .venv/bin/activate # Linux/macOS
```

Install dependencies
```console
$ pip install -r requirements.txt
```

Run the project
```console
$ python main.py
```

Optional: Create the `.exe` with default configuration
```console
$ pyinstaller Traductor-inador.spec
```

## Basic Usage 🖱️

### Text Translation
1. Select translation engine from the top bar
2. Choose source/target languages
3. Enter text in the left area
4. Click "Translate"
5. Result will appear in the lower area

### Document Translation
1. Go to the "Documents" tab
2. Click on "Select DOCX"
3. Choose source/target languages
4. Specify location and filename to save
5. Monitor progress in the bottom bar
6. A `.docx` will be created in the specified path

## Project Structure 📂
```text
Traductor-inador/
├── app/
│   ├── core/                 # Application core
│   ├── exceptions/           # Custom exceptions
│   ├── gui/                  # Graphical user interface
│   │   └── widgets/          # Custom UI components
│   ├── services/             # External service connectors
│   ├── styles/               # System styles
│   │   ├── screens/          # Screen styles
│   │   ├── theme/            # Theme styles
│   │   └── widgets/          # Custom widget styles
│   ├── utils/                # Utilities
|   └── validators/           # Validations
├── docs/                     # Technical documentation
├── requirements.txt          # Dependencies
└── main.py                   # Entry point
```

## Download Executable 📦

Click here to download the latest version of the program:  
[![Download](https://img.shields.io/badge/Download-.exe-blue)](https://github.com/MisaelRodriguez3/Traductor-inador/releases/download/v1.0.0/Traductor-inador.exe)