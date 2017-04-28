
import argparse
import cv2
import numpy as np
from time import *
IMG_WIN = "drawer"

# Dimensions in mm for letter size paper

WIDTH = 279
WIDTH_MARGIN = 25

HEIGHT = 215
HEIGHT_MARGIN = 25

# Amount we should scale the drawer by
SCALE = 2.0

# tolerance level for snapping to last drawn line
EPSILON = 20

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not

badStart = False

def scaleDownPoint(p):
    (x,y) = p
    return (int( x / SCALE),int(y / SCALE))

def close(x1,x2): return abs(x1-x2) < EPSILON


class Drawer:
    def __init__(self):
        self.refPt = []
        self.lines = []
        self.done = False

        cv2.namedWindow(IMG_WIN)
        cv2.setMouseCallback(IMG_WIN, self.drawLine)

        (self.width, self.height) = (int(WIDTH * SCALE), int(HEIGHT * SCALE))

        self.image = np.zeros([self.height, self.width,3], dtype=np.uint8)
        self.image.fill(255)

        #draw rectangle on blank image showing margin lines
        bp1  = (WIDTH_MARGIN, HEIGHT_MARGIN)
        bp2 = (self.width - WIDTH_MARGIN, self.height - HEIGHT_MARGIN)
        cv2.rectangle(self.image, bp1, bp2, 0)
        cv2.imshow(IMG_WIN, self.image)

    def inBounds(self, x,y):
        return (
            x > WIDTH_MARGIN and x < self.width - WIDTH_MARGIN and
            y > HEIGHT_MARGIN and y < self.height - HEIGHT_MARGIN
        )

    def snapToLast(self,x,y):
        if(len(self.lines)==0):
            return (x,y)
        else:
            (prev_x,prev_y) = self.lines[-1][1]
            if (close(prev_x,x) and close(prev_y,y)):
                return (prev_x, prev_y)
        return (x,y)

    def getImage(self):
        return self.image

    def getImageName(self):
        return IMG_WIN

    def parseLines(self):

        real_lines = []
        for line in self.lines:
            ((x1,y1),(x2,y2)) = (
                scaleDownPoint(line[0]),scaleDownPoint(line[1])
            )

            # flip x and y because cozmo has x as straight ahead
            # while drawer has x relative to cozmo's vertical axis.

            # y negated because negative y is to Cozmo's right at start.
            # and we start cozmo to the left of the paper.

            real_lines.append((-y1,x1,False))
            real_lines.append((-y2,x2, True))

        return real_lines

    def drawLine(self, event, x, y, flags, param):

        global badStart

        if (event == cv2.EVENT_LBUTTONDOWN):
            if (self.inBounds(x,y)):
                (x,y) = self.snapToLast(x,y)
                self.refPt = [(x, y)]
            else:
                badStart = True

        elif (event == cv2.EVENT_LBUTTONUP):
            if (self.inBounds(x,y) and (not badStart)):
                self.refPt.append((x , y))
                cv2.line(
                    self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2
                )
                self.lines.append(self.refPt)
                self.refPt = []
            badStart = False

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.done = True

        cv2.imshow(IMG_WIN, self.image)


    # Use this function in fsm's where the waitKey is called externally
    def getLines(self, wait=False):
        while True:
            if(self.done):
                cv2.destroyWindow(IMG_WIN)
                return self.parseLines()

            if (wait): cv2.waitKey(20)

