from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import cv2
import numpy as np

wb = load_workbook('Tracking.xlsx')
ws = wb.active


#create the tracker for CSRT
trackers = cv2.MultiTracker_create()

#load the video for CSRT
v = cv2.VideoCapture('slow.mp4')
ret, frame = v.read()

k = 5
for i in range(k):
    cv2.imshow('frame', frame)
    bbi = cv2.selectROI(frame)
    tracker_i = cv2.TrackerCSRT_create()
    trackers.add(tracker_i, frame, bbi)
frameNumber = 2

while True:
    ret, frame = v.read()
    if not ret:
        break
    ret, boxes = trackers.update(frame)
    cp = []
    for box in boxes:
        (x,y,w,h) = [int(a) for a in box]
        c1 = x+int(.5*w)
        c2 = y+int(.5*h)

        cp.append((c1,c2))

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2, 1)
        cv2.circle(frame, (c1,c2), 15, (0, 255, 0), 5)
        cv2.circle(frame, (0, 0), 10, (0, 0, 255), 3)
    cv2.imshow("frame", frame)
    print(cp)


    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break

v.release()
cv2.destroyAllWindows()


