import numpy as np
import cv2

def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x,y))

originalImage = cv2.imread('./image/frame_0.jpg')
image = cv2.imread('./image/frame_0.jpg')

cap = cv2.VideoCapture(0)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

coords = []

while True:
    if len(coords) == 3:
        coords = []
        image = originalImage
    if len(coords) == 2:
        image = cv2.line(originalImage, coords[0], coords[1], (0,0,255), 2) 
    cv2.imshow("Frame", originalImage)

    key=cv2.waitKey(1)
    if key == 27:
        break

cap.realease()
cv2.destroyAllWindows()