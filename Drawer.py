import argparse
import cv2

IMG_WIN = "drawer"

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
lines = []

def draw_line(event, x, y, flags, param):
    #grab references to the global variables
    global refPt, lines
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
        # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 2)
        lines.append(refPt)
        refPt = []
        cv2.imshow(IMG_WIN, image)

image = cv2.imread('raw_images/square.jpg')
cv2.namedWindow(IMG_WIN)
cv2.setMouseCallback(IMG_WIN, draw_line)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow(IMG_WIN, image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# close all open windows
cv2.destroyAllWindows()
