
import argparse
import cv2
import numpy as np

IMG_WIN = "drawer"

# Dimensions in mm for letter size paper
# (May want to make dimensions smaller to allow for some margin

WIDTH = 215
HEIGHT = 279

# Amount we should scale the drawer by
SCALE = 2.0

# tolerance level for snapping to last drawn line
EPSILON = 20

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
lines = []

def close(x1,x2): return abs(x1-x2) < EPSILON

def snapToLast(x,y):
    global lines
    if(len(lines)==0):
        return (x,y)
    else:
        (prev_x,prev_y) = lines[-1][1]
        if (close(prev_x,x) and close(prev_y,y)):
            return (prev_x, prev_y)
    return (x,y)

def draw_line(event, x, y, flags, param):
    #grab references to the global variables
    global refPt, lines
    if event == cv2.EVENT_LBUTTONDOWN:
        (x,y) = snapToLast(x,y)
        refPt = [(x, y)]
        cropping = True
        # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x , y))
        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 2)
        lines.append(refPt)
        refPt = []
        cv2.imshow(IMG_WIN, image)

cv2.namedWindow(IMG_WIN)
cv2.setMouseCallback(IMG_WIN, draw_line)


image = np.zeros([int(WIDTH * SCALE),int(HEIGHT * SCALE),3], dtype=np.uint8)
image.fill(255)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow(IMG_WIN, image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'c' key is pressed, break from the loop
    if key == ord("c"):
        break

# close all open windows
cv2.destroyAllWindows()

