
```markdown
# VisionAI Recognition Suite

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Advanced Image Recognition with Modern GUI**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Troubleshooting](#troubleshooting)

</div>

---

## 📋 Overview

VisionAI is a powerful desktop application that combines Optical Character Recognition (OCR) and Object Detection in a sleek, modern interface. Built with Python and featuring smooth animations, it provides an intuitive way to extract text and detect objects from images.

### 🎯 Key Capabilities

| Feature | Description | Technology |
|---------|-------------|------------|
| **Text Recognition** | Extract text from images, screenshots, and documents | Tesseract OCR |
| **Object Detection** | Identify and highlight objects in images | OpenCV Contour Detection |
| **Image Processing** | Load, display, and analyze various image formats | OpenCV + PIL |

---

## ✨ Features

### 🎨 Modern User Interface
- **Sleek Dark Theme** - Eye-friendly design with professional aesthetics
- **Smooth Animations** - Animated background and interactive elements
- **Responsive Layout** - Adapts to different screen sizes
- **Real-time Status Updates** - Live progress indicators and status messages

### 📝 OCR Capabilities
- Extract text from multiple image formats (JPG, PNG, BMP, TIFF)
- Preprocessing for better accuracy (thresholding, denoising)
- Support for multiple languages (with Tesseract language packs)
- Word and character count statistics

### 🔍 Object Detection
- Contour-based detection (no deep learning required)
- Bounding box visualization
- Object count and positioning data
- Area and size analysis

---

## 🚀 Installation

### System Requirements

- **Operating System**: Windows 10/11, Linux, or macOS
- **Python Version**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for application and dependencies

### Step 1: Install Python Dependencies

Open terminal/command prompt and run:

```bash
# Core dependencies
pip install opencv-python pillow numpy

# OCR support
pip install pytesseract

# Optional: Enhanced object detection
pip install ultralytics  # Requires Python 3.10/3.11
```

### Step 2: Install Tesseract OCR Engine

#### Windows
1. Download installer from: [Tesseract GitHub Releases](https://github.com/UB-Mannheim/tesseract/releases)
2. Get: `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
3. Run installer and **check** "Add Tesseract to system PATH"
4. Complete installation

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

### Step 3: Verify Installation

Create a test file `check_install.py`:

```python
import cv2
import pytesseract
print(f"OpenCV: {cv2.__version__}")
print(f"Tesseract: {pytesseract.get_tesseract_version()}")
print("✅ Installation successful!")
```

Run: `python check_install.py`

---

## 📖 Usage Guide

### Launching the Application

```bash
python visionai_app.py
```

### Basic Workflow

1. **Load an Image**
   - Click "📂 Load Image"
   - Select JPG, PNG, BMP, or TIFF file
   - Image appears in the left panel

2. **Select Recognition Mode**
   - **Text Recognition (OCR)** - Extract text from images
   - **Object Detection** - Find and highlight objects

3. **Process the Image**
   - Click "✨ Recognize"
   - Wait for processing (progress bar shows status)
   - Results appear in the right panel

4. **Review Results**
   - Extracted text or detected objects listed
   - Annotated image shows detection boxes
   - Statistics provided (word count, object count, etc.)

5. **Clear & Start Over**
   - Click "🗑️ Clear" to reset

### Example Use Cases

| Use Case | Recommended Mode | Best Results With |
|----------|-----------------|-------------------|
| Scanning documents | OCR | High-contrast, clear text |
| Extracting quotes | OCR | Printed text, good lighting |
| Finding products | Object Detection | Solid background, distinct shapes |
| Analyzing layouts | Object Detection | Well-separated elements |

---

## 🛠️ Configuration

### Custom Tesseract Path

If Tesseract is installed in a custom location, update the path in the code:

```python
# Add this after importing pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Your\Path\tesseract.exe'
```

### Adjusting OCR Sensitivity

Modify the threshold value in `recognize_text()` method:

```python
# Lower = more sensitive (may catch noise)
# Higher = less sensitive (may miss text)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
```

### Object Detection Sensitivity

Adjust minimum contour area in `detect_objects()` method:

```python
# Lower = detects smaller objects
# Higher = ignores small noise
min_area = 500  # Pixels
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### ❌ "Tesseract not found" Error

**Problem**: Application can't find Tesseract installation

**Solutions**:
1. Verify Tesseract is installed:
   ```bash
   tesseract --version
   ```
2. Add Tesseract to system PATH
3. Set path manually in code (see Configuration section)

#### ❌ "No module named cv2"

**Solution**:
```bash
pip install opencv-python
```

#### ❌ "DLL initialization failed" on Python 3.14

**Cause**: PyTorch compatibility issues with Python 3.14

**Solutions**:
- Use the contour-based detection (already included)
- Downgrade to Python 3.10 or 3.11
- Use virtual environment with older Python

#### ❌ Poor OCR Accuracy

**Tips for better results**:
- Use high-resolution images
- Ensure good contrast (dark text on light background)
- Avoid blurry or skewed images
- Preprocess images with photo editing software

#### ❌ Object Detection Not Finding Objects

**Adjust detection parameters**:
- Lower the `min_area` threshold
- Ensure good lighting in image
- Use images with clear foreground/background separation

---

## 📁 Project Structure

```
VisionAI/
├── visionai_app.py          # Main application
├── models/                  # Detection models (auto-created)
│   ├── yolov3.cfg          # YOLO config (optional)
│   ├── yolov3.weights      # YOLO weights (optional)
│   └── coco.names          # Class names (optional)
├── test_images/             # Sample images (auto-created)
└── README.md               # This file
```

---

## 🎯 Performance Tips

### For Faster OCR
- Use smaller images (resize to < 2000px)
- Convert images to grayscale before processing
- Use SSD for temporary files

### For Better Detection
- Ensure even lighting
- Use plain backgrounds when possible
- Avoid shadows and reflections

---

## 🔧 Advanced Configuration

### Custom Color Scheme

Modify the color variables in `__init__` method:

```python
self.bg_dark = "#0f0f13"        # Main background
self.bg_card = "#1a1a2e"        # Card background
self.accent_primary = "#6c63ff" # Primary button color
self.accent_secondary = "#ff6584" # Hover color
```

### Window Size

Adjust initial window dimensions:

```python
self.root.geometry("1400x800")  # Width x Height
self.root.minsize(1200, 700)    # Minimum size
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Add support for more OCR languages
- Implement YOLO object detection (when PyTorch compatible)
- Add batch processing capability
- Export results to PDF/TXT
- Add image preprocessing tools

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

## 📞 Support

- **Issues**: Check Troubleshooting section first
- **Documentation**: See inline code comments
- **Updates**: Watch this repository for updates

---

## 🙏 Acknowledgments

- **Tesseract OCR** - Google's OCR engine
- **OpenCV** - Computer vision library
- **Pillow** - Python Imaging Library

---

<div align="center">

**Made with ❤️ using Python**

[Report Bug](issues) • [Request Feature](issues) • [Star on GitHub](github)

</div>
```

## 📄 Additional Quick Start Guide

Save this as `QUICKSTART.md`:

```markdown
# VisionAI Quick Start Guide

## 5 Minutes to Recognition

### 1. Install (2 minutes)

```bash
# Core packages
pip install opencv-python pillow numpy pytesseract

# Download and install Tesseract from:
# https://github.com/UB-Mannheim/tesseract/releases
```

### 2. Run (1 minute)

```bash
python visionai_app.py
```

### 3. Test (2 minutes)

1. **Load any image** with text (screenshot, photo of a sign)
2. **Select "Text Recognition"**
3. **Click "Recognize"**
4. **View extracted text!**

## Sample Test Images

Create a quick test image:

```python
# test_image.py
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (800, 200), color='white')
draw = ImageDraw.Draw(img)
draw.text((50, 80), "Hello VisionAI! This is a test.", fill='black')
img.save('test.png')
print("✅ Created test.png")
```

Run: `python test_image.py`

Then load `test.png` in VisionAI!

## Need Help?

- **OCR not working?** Run: `tesseract --version`
- **Import errors?** Run: `pip install opencv-python pillow numpy`
- **Slow performance?** Use smaller images (max 2000px)

**That's it! You're ready to recognize! 🎉**
```

## 📋 Installation Check Script

Save as `setup_check.py`:

```python
#!/usr/bin/env python3
"""VisionAI Installation Checker"""

import sys
import subprocess
import importlib.util

def check_package(package_name, display_name=None):
    """Check if a Python package is installed"""
    if display_name is None:
        display_name = package_name
    
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"✅ {display_name}: Installed")
        return True
    else:
        print(f"❌ {display_name}: Not installed")
        print(f"   Run: pip install {package_name}")
        return False

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ Tesseract: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Tesseract: Not found")
    print("   Download from: https://github.com/UB-Mannheim/tesseract/releases")
    return False

def main():
    print("="*50)
    print("VisionAI - Installation Checker")
    print("="*50)
    print(f"Python Version: {sys.version.split()[0]}\n")
    
    # Check Python version
    if sys.version_info >= (3, 14):
        print("⚠️ Warning: Python 3.14 may have compatibility issues")
        print("   Consider using Python 3.10 or 3.11 for best results\n")
    
    # Check packages
    packages = [
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("pytesseract", "pytesseract"),
    ]
    
    for package, display in packages:
        check_package(package, display)
    
    print()
    check_tesseract()
    
    print("\n" + "="*50)
    print("Setup Complete!")
    print("Run 'python visionai_app.py' to start")
    print("="*50)

if __name__ == "__main__":
    main()
```

Run the checker:
```bash
python setup_check.py
```

This will show you exactly what's installed and what needs to be installed!
