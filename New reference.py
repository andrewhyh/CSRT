#openCV is our computer vision library for accessing videos and using tracking algorithms
#openpyXL is our library for creating and inserting data into excel files
import cv2
from openpyxl import Workbook


#creating a new workbook and selecting the first sheet
wb = Workbook()
ws = wb.active
ws.title = "Data" #this data sheet will be called 'Data'


ws.append(['x1', 'y1', 'x2', 'y2', 'x3', 'y3']) #creating the header aka the first row


#create the tracker for CSRT
trackers = cv2.MultiTracker_create()

#load the video for CSRT
v = cv2.VideoCapture('slow vid.mp4')
ret, frame = v.read()


class Point(): #creating a class for points with objects


     def __init__(self):
        self.xpositions = []
        self.ypositions = []
        self.xref = []
        self.yref = []

     def compare(self):
         pass


point0= Point()
point1= Point()
point2= Point()
point3= Point()


#initialize the variable that records what frame we are on
frameNumber = 1
point = 0
k = 4



#using the first frame of the video, we can select the "region of interests" or "ROI" for each point
for i in range(k):
    cv2.imshow('frame', frame)
    bbi = cv2.selectROI(frame)
    tracker_i = cv2.TrackerCSRT_create()
    trackers.add(tracker_i, frame, bbi)
    data_i = []
    newdata_i = []



while True:
    ret, frame = v.read()
    cp = []
    if not ret:
        break
    ret, boxes = trackers.update(frame)

    for i, box in enumerate(boxes):

        (x,y,w,h) = [int(a) for a in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2, 1)
        cv2.circle(frame, (0, 0), 10, (0, 0, 255), 3)

        cx = x+int(.5*w)
        cy = y+int(.5*h)
        cv2.circle(frame, (cx, cy), 15, (0, 255, 0), 5)
        cp.append((cx,cy))


        if point == 0:
            point0.xpositions.append(cx)
            point0.ypositions.append(cy)

            cv2.putText(frame, "Reference", (cx, cy - 35), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)


        if point == 1:
            point1.xpositions.append(cx)
            point1.ypositions.append(cy)

            cv2.putText(frame, "Point" + str(point), (cx, cy - 50), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)


        if point == 2:
            point2.xpositions.append(cx)
            point2.ypositions.append(cy)

            cv2.putText(frame, "Point" + str(point), (cx, cy - 40), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)


        if point == 3:
            point3.xpositions.append(cx)
            point3.ypositions.append(cy)

            cv2.putText(frame, "Point" + str(point), (cx, cy - 35), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

        point += 1
        frameNumber += 1

        if point == 4:
            point -= 4

        print(cp)

    cv2.imshow("frame", frame)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break

v.release() #close the windows that were created by the py file
cv2.destroyAllWindows()


for i in range(frameNumber-1):
    data_i = [point1.xpositions[i], point1.ypositions[i], point2.xpositions[i], point2.ypositions[i],point3.xpositions[i], point3.ypositions[i]]
    newdata_i = [(point0.xpositions[i]-point1.xpositions[i]), (point0.xpositions[i]-point1.ypositions[i]),
                 (point0.xpositions[i]-point2.xpositions[i]), (point0.xpositions[i]-point2.ypositions[i]),
                 (point0.xpositions[i]-point3.xpositions[i]), (point0.xpositions[i]-point3.ypositions[i])]

    ws.append(newdata_i)
    wb.save('MACH3.xlsx')






