import cv2
import time
import numpy as np

cap = cv2.VideoCapture('vtest.avi')

ret, frame1 = cap.read()
ret, frame2 = cap.read()
diff = cv2.absdiff(frame1, frame2)
cv2.imshow('Diff', diff)

gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

cv2.imshow('Gray', gray)

blur = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('Blur', blur)

_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
cv2.imshow('Thresh', thresh)

dilated = cv2.dilate(thresh, None, iterations=3)
cv2.imshow('dilate', dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()
