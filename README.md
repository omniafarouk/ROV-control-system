# ROV Control System GUI

An advanced Python-based GUI system for controlling a Remotely Operated Vehicle (ROV), featuring multithreaded video stitching, stereo vision depth estimation, and real-time serial communication with an Arduino.

---

##  Overview

This project implements a modular and multithreaded GUI using PyQt5 that serves as the main interface for controlling and monitoring an ROV. Key components include:

- Manual and Autonomous car control
- Live webcam feed and screenshots
- Real-time multithreaded video stitching
- Stereo vision processing with depth map generation
- Serial communication with Arduino

---

## Features

### GUI Control Modes
- **Manual Mode**: Directional movement buttons, speed selection, and start/stop controls.
- **Autonomous Mode**: Sensor-based display (voltage, current, distance readings).

### Serial Communication
- Bi-directional communication with an Arduino over a serial port (`pyserial`).
- Commands and sensor readings are handled via encoded strings.

### Live Camera Feed
- Real-time webcam display using OpenCV.
- Capture screenshots directly from the UI.

### Video Stitching (Multithreaded)
- Load and stitch two video streams using OpenCV’s Stitcher.
- Scrollable stitched view; fullscreen toggle supported.
- QThread usage ensures smooth UI responsiveness.

### Stereo Vision
- Full stereo processing pipeline:
  - Calibration
  - Rectification
  - Disparity computation
  - Depth map generation
- Abstract base class and modular design for extensibility.

---

## 🧠 Technologies Used

- Python 3.8+
- PyQt5
- OpenCV
- PySerial
- OOP / Threading / Qt Designer

---

## Project Structure

```bash
.
├── frontendtest.py           # Main window GUI (Qt Designer converted)
├── backendtest1.py          # Backend logic and window switching
├── video_stitching.py       # Multithreaded video stitching logic
├── stereo_vision/           # Modules for stereo vision pipeline
│   ├── calibration.py
│   ├── rectification.py
│   ├── disparity.py
│   ├── depth.py
│   └── utils.py
├── ROV_GUI_Project_Report.pdf  # Full technical report
└── README.md
