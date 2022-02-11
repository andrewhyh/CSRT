import cv2 #openCV is our computer vision library for accessing videos and using tracking algorithms
from openpyxl import Workbook #openpyXL is our library for creating and inserting data into excel files

#creating a new workbook and selecting the first sheet
wb = Workbook()
ws = wb.active
ws.title = "Data" #this data sheet will be called 'Data'

ws.append(['Frame', '(X,', 'Y)']) #creating the header aka the first row


#create the tracker for CSRT
tracker = cv2.TrackerCSRT_create()

#load the video for CSRT
v = cv2.VideoCapture('slow.mp4')
ret, frame = v.read()

#using the first frame of the video, we can select the "region of interest" or "ROI"
bbox = cv2.selectROI(frame)
print(bbox)

ret = tracker.init(frame, bbox)

#initialize the variable that records what frame we are on
frameNumber = 1


while True:
    ret, frame = v.read() #plays the video
    if not ret:
        break
    ret, bbox = tracker.update(frame) #updates each frame to check if the object is still tracking

    if ret:
        frameNumber += 1 #increase the frame number variable

        (x,y,w,h) = [int(a) for a in bbox] #the variables of the box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2, 1)  #displays the box of "ROI" in each frame

        c1 = x+int(.5*w) #c1 and c2 is the center coordinates of the circle imagine as if it is (x,y)
        c2 = y+int(.5*h)

        data = ['Frame ' + str(frameNumber), c1, c2] #create the data list for excel file

        cv2.circle(frame, (x+int(.5*w),y+int(.5*h)), 15, (0, 255, 0), 5) #displays the circle each frame
        cv2.circle(frame, (0, 0), 10, (0, 0, 255), 3) #looking at the top left corner of the frame there
        ws.append(data) #adds our data to the excel file
    cv2.imshow("frame", frame) #displays video

    print(c1, c2) #this will print our center coordinates in real time
    wb.save('MACH1.xlsx') #saves the excel file and names it "MACH1"

    key = cv2.waitKey(5) & 0xFF #to exit the video while it plays, press q
    if key == ord('q'):
        break

v.release() #close the windows that were created by the py file
cv2.destroyAllWindows()


