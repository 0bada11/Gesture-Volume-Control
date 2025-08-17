import HandTracking as ht
import cv2 as cv
import numpy as np
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Create detector object
detector = ht.handDetector(minDetectionCon=0.9)

# Initialize audio interface once
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange() # type: ignore
minVol = volRange[0]
maxVol = volRange[1]

prevVol = 0  # For smoothing

def markFingers(lmList, index1, index2):
    x1, y1 = lmList[index1][1], lmList[index1][2]
    x2, y2 = lmList[index2][1], lmList[index2][2]
    drawFingerGraphics(x1, x2, y1, y2)
    return x1, x2, y1, y2

def drawFingerGraphics(x1, x2, y1, y2):
    cv.circle(frame, (x1, y1), 10, (169, 175, 58), cv.FILLED)
    cv.circle(frame, (x2, y2), 10, (169, 175, 58), cv.FILLED)
    cv.line(frame, (x1, y1), (x2, y2), color=(169, 175, 58), thickness=3)
    midX, midY = int((x1 + x2) / 2), int((y1 + y2) / 2)
    cv.circle(frame, (midX, midY), 5, (255, 255, 255), cv.FILLED)

def findDistance(x1, x2, y1, y2):
    return math.hypot(x2 - x1, y2 - y1)

def setVolumeLevel(length, x1, x2, y1, y2, prevVol, volume, minVol, maxVol):
    # Mute if fingers are very close
    if length < 25:
        midX, midY = int((x1 + x2) / 2), int((y1 + y2) / 2)
        cv.circle(frame, (midX, midY), 7, (0, 0, 255), cv.FILLED)
        volume.SetMute(1, None)
    else:
        volume.SetMute(0, None)

    # Smooth volume adjustment
    smoothing = 3
    vol = np.interp(length, [30, 180], [minVol, maxVol])
    vol = prevVol + (vol - prevVol) / smoothing
    volume.SetMasterVolumeLevel(vol, None)
    return vol

def drawVolBar(length):
    volBar = np.interp(length, [30, 180], [400, 150])
    volPercent = np.interp(length, [30, 180], [0, 100])
    cv.rectangle(frame, (50, 150), (85, 400), (169, 175, 58), 2)
    cv.rectangle(frame, (50, int(volBar)), (85, 400), (169, 175, 58), cv.FILLED)
    cv.putText(frame, f'{int(volPercent)} %', (40, 450), cv.FONT_HERSHEY_PLAIN, 2, (169, 175, 58), 4)

# Start webcam
webcam = cv.VideoCapture(0)

while True:
    isTrue, frame = webcam.read()
    frame = cv.flip(frame, 1)

    # Detect hands
    frame = detector.findHands(frame)

    # Get landmarks
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        x1, x2, y1, y2 = markFingers(lmList, index1=4, index2=8)
        length = findDistance(x1, x2, y1, y2)
        prevVol = setVolumeLevel(length, x1, x2, y1, y2, prevVol, volume, minVol, maxVol)
        drawVolBar(length)

    # Show FPS
    frame = detector.showFPS(frame)
    cv.imshow('Hand Volume Control', frame)

    # Exit on ESC key
    if cv.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv.destroyAllWindows()