import cv2
import os
import numpy as np
import HandTrackingModule as HTM

folder = "Photos"
Names = os.listdir(folder)
images = []
for path in Names:
    image = cv2.imread(f'{folder}/{path}')
    image = cv2.resize(image, (1280, 125))
    images.append(image)

cap = cv2.VideoCapture(1)
detector = HTM.handDetector()
tipIds = [4, 8, 12, 16, 20]
color = (0, 0, 255)
header = images[3]
xPrev = 0
yPrev = 0

board = np.zeros((1280, 720, 3), dtype=np.uint8)
th = 20


while True:
    isTrue, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame = detector.findHands(frame, True)
    lmList = detector.findPosition(frame)
    if len(lmList) != 0:

        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        if y1 < lmList[7][2]:
            index = 1
        else:
            index = 0
        if y2 < lmList[11][2]:
            mid = 1
        else:
            mid = 0

        if index and mid:
            xPrev, yPrev = x1, y1
            print("selection")
            if y1 < 125:
                # in the header
                if 0 < x1 < 300:
                    # red
                    header = images[3]
                    color = (0, 0, 255)

                if 320 < x1 < 620:
                    # blue
                    header = images[1]
                    color = (255, 0, 0)

                if 640 < x1 < 940:
                    # yellow
                    header = images[2]
                    color = (0, 191, 255)

                if 960 < x1 < 1280:
                    # erase
                    color = (0, 0, 0)
                    header = images[0]
                    print("erase")

            cv2.rectangle(frame, (x1, y1 - 50), (x2, y2 + 50), color, cv2.FILLED)

        if index and not mid:
            print("drawing")
            if xPrev == 0 and yPrev == 0:
                xPrev, yPrev = x1, y1

            if color == (0, 0, 0):
                th = 100
            else:
                th = 20

            cv2.circle(frame, (x1, y1), 15, color, cv2.FILLED)
            cv2.line(frame, (xPrev, yPrev), (x1, y1), color, th)
            cv2.line(board, (xPrev, yPrev), (x1, y1), color, th)

            xPrev, yPrev = x1, y1

    frame[0:125] = header
    board = cv2.resize(board, (frame.shape[1], frame.shape[0]))
    frame = cv2.addWeighted(frame, 0.5, board, 0.5, 0)
    cv2.imshow("Board", frame)

    cv2.waitKey(1)
