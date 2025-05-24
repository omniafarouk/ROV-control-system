# ROV Control System GUI

An advanced Python-based GUI system for controlling a Remotely Operated Vehicle (ROV), featuring multithreaded video stitching, stereo vision depth estimation, and real-time serial communication with an Arduino.

** For more information about the project read the project report pdf attached

---

##  Overview

This project implements a modular and multithreaded GUI using PyQt6 that serves as the main interface for controlling and monitoring an ROV. Key components include:

- Manual and Autonomous car control
- Live webcam feed and screenshots
- Real-time multithreaded video stitching
- Stereo vision processing with depth map generation
- Serial communication with Arduino

---

## Features

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

## Technologies Used

- Python 3.8+
- PyQt6
- OpenCV
- OOP / Threading / Qt Designer

---

* To run StereoVision project --> run MainStereoVisionWindow (ensure you have sufficient different views of the same image)
* To run VideoStitching project --> run MainCameraSystemGUI (ensure you have different videos of 2 pov of the same view)

## Project Structure

``` bash

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

