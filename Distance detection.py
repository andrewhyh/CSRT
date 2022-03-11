import cv2
import numpy as np



v = cv2.VideoCapture('2dot.mp4')
ret, frame = v.read()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of red color in HSV
lower_green = np.array([60, 100, 50])
upper_green = np.array([60, 255, 255])



# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_green, upper_green)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame, frame, mask=mask)

# Convert BGR to GRAY for the circle detection
red = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
grayFrame = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)

circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, .5, 10,
                           param1=100, param2=25, minRadius=0, maxRadius=40)
positions = []

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(res, (i[0], i[1]), 5, (0, 0, 255), 3)
        positions.append(i)

# we are just adding 2 more channels on the mask so we can stack it along other images
mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# stacking up all three images together
stacked = np.hstack((mask_3, frame, res))

cv2.imshow('Result', cv2.resize(stacked, None, fx=0.4, fy=0.5))


print(positions)




cv2.waitKey(0)
cv2.destroyAllWindows()