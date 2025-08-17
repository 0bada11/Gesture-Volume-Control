# Hand Gesture Volume Control 

A Python project that allows you to **control your computer's volume using hand gestures** via your webcam.  
The program detects your hand using **MediaPipe** and adjusts the system volume based on the distance between your **thumb** and **index finger**.

---

## Features
- Real-time **hand detection** using OpenCV + MediaPipe.
- **Gesture-based volume control**:
  - Small distance → **Mute**.
  - Larger distance → Adjust system volume smoothly.
- **Visual feedback**:
  - Circles and lines drawn between fingers.
  - Volume bar with percentage display.
  - FPS counter on screen.
- Runs on Windows using **pycaw** for audio control.

---

## Requirements
Make sure you have Python 3.8+ installed, then install the required libraries:

```bash
pip install opencv-python mediapipe comtypes pycaw numpy
