import cv2
import numpy as np
import time

cap = cv2.VideoCapture('2dot.mp4')

while (1):

    # Take each frame
    ret, frame = cap.read()
    if not ret: break
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_red = np.array([40, 40,40]) #red = [0, 150, 0] and [10, 255, 255]
    upper_red = np.array([70, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert BGR to GRAY for the circle detection
    red = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    grayFrame = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)

    # circle array and paramaters
    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, .5, 10,
                               param1=100, param2=25, minRadius=0, maxRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(res, (i[0], i[1]), 5, (0, 0, 255), 3)

    # we are just adding 2 more channels on the mask so we can stack it along other images
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stacking up all three images together
    stacked = np.hstack((mask_3, frame, res))

    cv2.imshow('Result', cv2.resize(stacked, None, fx=0.4, fy=0.5))
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(.2)

    print(circles)
cv2.destroyAllWindows()
cap.release()