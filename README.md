# Fast File Copier ⚡

A high-speed, multi-threaded Windows desktop application built with Python and CustomTkinter. Designed to copy photos, videos, and large directories significantly faster than standard file explorers by leveraging concurrent I/O operations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 🌟 Key Features

- Multi-threaded Architecture: Utilizes ThreadPoolExecutor to handle concurrent I/O tasks, achieving up to 17% faster copy speeds compared to Windows Explorer in file-intensive tasks.
- Responsive GUI: Built with CustomTkinter on a dedicated background thread to prevent UI freezing (Not Responding) during heavy operations.
- Safe Cancellation: Features real-time cancellation using threading.Event() to stop ongoing copy processes instantly without locking memory or corrupting remaining files.
- Robust Error Handling: Seamlessly manages system exceptions, including PermissionError and missing file paths.
- Standalone Executable: Fully packageable into a single portable .exe file via PyInstaller.

## 🛠️ Tech Stack

- GUI Framework: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Concurrency & Threading: threading, concurrent.futures.ThreadPoolExecutor
- File System Operations: shutil, os
- Deployment: PyInstaller

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed.

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/YOUR_USERNAME/Fast-File-Copier.git](https://github.com/YOUR_USERNAME/Fast-File-Copier.git)
cd Fast-File-Copier
```
   
2. Install dependencies:
```bash
pip install customtkinter
```

3. Run the application:
```bash
python Fast_File_Copier.py
```
