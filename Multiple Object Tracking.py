import cv2 #openCV is our computer vision library for accessing videos and using tracking algorithms
from openpyxl import Workbook #openpyXL is our library for creating and inserting data into excel files

#creating a new workbook and selecting the first sheet
wb = Workbook()
ws = wb.active
ws.title = "Data" #this data sheet will be called 'Data'

ws.append(['Frame', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3']) #creating the header aka the first row

#create the tracker for CSRT
trackers = cv2.MultiTracker_create()

#load the video for CSRT
v = cv2.VideoCapture('slow.mp4')
ret, frame = v.read()

class Point(): #creating a class for points with objects
     def __init__(self):
        self.xpositions=[]
        self.ypositions=[]



point1= Point()
point2= Point()
point3 =Point()


point = 0
k = 3

for i in range(k):
    cv2.imshow('frame', frame)
    bbi = cv2.selectROI(frame)
    tracker_i = cv2.TrackerCSRT_create()
    trackers.add(tracker_i, frame, bbi)
    data_i = []

framenum=0

while True:
    ret, frame = v.read()
    if not ret:
        break
    ret, boxes = trackers.update(frame)

    for i, box in enumerate(boxes):

        point += 1
        framenum +=1

        (x,y,w,h) = [int(a) for a in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2, 1)

        c1 = x+int(.5*w)
        c2 = y+int(.5*h)

        if point == 1:
            point1.xpositions.append(c1)
            point1.ypositions.append(c2)

        if point == 2:
            point2.xpositions.append(c1)
            point2.ypositions.append(c2)

        if point == 3:
            point3.xpositions.append(c1)
            point3.ypositions.append(c2)

        cv2.circle(frame, (c1,c2), 15, (0, 255, 0), 5)
        cv2.circle(frame, (0, 0), 10, (0, 0, 255), 3)

        if point ==3:
            point -= 3


    cv2.imshow("frame", frame)

    wb.save('MACH2.xlsx')

    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break

for i in range(framenum+1):
    data_i = ['Frame '+str(i), point1.xpositions[i], point1.ypositions[i], point2.xpositions[i], point2.ypositions[i],point3.xpositions[i], point3.ypositions[i]]
    print(data_i)
    ws.append(data_i)
    wb.save('MACH2.xlsx')


v.release()
cv2.destroyAllWindows()

print(point1.xpositions[0])


