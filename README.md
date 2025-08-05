# Hand Gesture Volume Control 🎚️🖐️

This Python project uses **hand gestures** detected by your webcam to control the **system volume** in real time. It combines **MediaPipe** for hand tracking, **OpenCV** for image processing, and **pycaw** for Windows audio control.

---

## 📸 Features

- 👋 Real-time hand detection via webcam
- 👍 Controls volume using the distance between **thumb** and **index finger**
- 🔇 Automatically mutes when fingers are close together
- 📊 Displays a volume level bar and percentage
- 🎞️ Shows real-time FPS
- ⛔ Exit by pressing the **ESC** key

---

## 📦 Requirements

- Python 3.7+
- Windows OS (for `pycaw` audio control)

### 🛠️ Install Dependencies

```bash
pip install opencv-python mediapipe pycaw comtypes numpy
