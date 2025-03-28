# 🚀 PyReader

## 📖 Overview
**PyReader** is a Python-based barcode and QR code scanner that utilizes OpenCV and pyzbar to read and decode barcodes from a live camera feed. It provides a simple interface for selecting available cameras and displays real-time barcode scanning results.

## ✨ Features
- 🔍 Detects and decodes barcodes and QR codes in real-time
- 🖼️ Highlights detected barcodes with bounding boxes
- 📷 Supports multiple camera devices
- 🛑 Filters duplicate scans to reduce redundancy
- 🎨 ANSI color-coded console output for better readability
- 🛠️ Graceful error handling and logging

## 📦 Requirements
- 🐍 Python 3.x
- 🖼️ OpenCV (`cv2`)
- 📑 Pyzbar (`pyzbar`)

## ⚙️ Installation
Ensure you have Python installed, then install the required dependencies:

```sh
pip install opencv-python pyzbar
```

## ▶️ Usage
Run the script using:

```sh
python pyreader.py
```

### 🔄 Steps:
1. 🖥️ The script lists available cameras and prompts the user to select one.
2. 🎥 Once a camera is selected, the live feed starts.
3. 📜 Place a barcode or QR code in front of the camera.
4. 📢 The detected barcode will be displayed in the console along with its type.
5. ❌ Press `q` to exit the scanner.

## 📌 Example Output
```
[25.03.2025, 14:15:30] Using camera 0
[25.03.2025, 14:15:35] Barcode detected: 123456789012 (Type: EAN13)
```

## 📜 License
This project is open-source and licensed under the MIT License.

## 👨‍💻 Author
Developed by [LolgamerHDDE](https://github.com/LolgamerHDDE).
