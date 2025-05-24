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

## To run StereoVision project --> run MainStereoVisionWindow (ensure you have sufficient different views of the same image)
## To run VideoStitching project --> run MainCameraSystemGUI (ensure you have different videos of 2 pov of the same view)

## Project Structure

├── video_stitching       # Multithreaded video stitching logic
|  ├── camera_state.py
|  ├── createViewThread.py
|  ├── FileExplorerDialogue.py
|  ├── MainCameraSystemGui.py
|  ├── New_View.py
├── stereo_vision           # Modules for stereo vision pipeline
│   ├── calibration.py
│   ├── rectification.py
│   ├── disparity.py
│   ├── depthComputation.py
│   ├── StereoVisionProcess
│   ├── MainStereoVisionWindow.py
│   ├── utilities.py

