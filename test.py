import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

W = None
H = None

ret, frame1 = cap.read()
ret, frame2 = cap.read()
ret, frame3 = cap.read()
ret, frame4 = cap.read()
ret, frame5 = cap.read()
ret, frame6 = cap.read()
diff = cv2.absdiff(frame1, frame2)
cv2.imshow('Test', diff)

diff2 = cv2.absdiff(frame5, frame6)
cv2.imshow('a', diff2)
cv2.waitKey(0)
cv2.destroyAllWindows()
