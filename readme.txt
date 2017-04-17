
TODO LIST

Rachel Nakamura:

1.) Build pen attachment that is reliable.
  ie: not too much friction when Cozmo lowers lift, but enough
  to make a steady line.
  Pen should not move when cozmo raises/lowers lift.

  Bonus Points: Would be helpful if lift was easily attachable/detachible


Joshua Ardito:

1.) Process images with OpenCV with parameters that produce long straight
    lines easily drawn by Cozmo.

    - OpenCV has a Canny method for this.
    - Manipulate data into world co-ordinates. This will probably call
      for some scaling /interpolation.

MVP Goals:

- Have Cozmo draw the lines
  - To move to a new endpoint, calculate (dy,dx) between current
    endpoint and new endpoint, use Cozmo's heading and the arctan
    to tell us how much to turn. Move (dx**2 + dy**2) to get to the new
    point.
  - To draw a line, we are given some (x1,y1,x2,y2). We are at x1,y1.
    Can turn using the same formula as above but our center of rotation
    should be about the point. So we move half cozmo's body length forward,
    rotate, then move back.

    Cozmo's Body Length: ~85mm

Stretch Goals:

- Have Cozmo extract the image from one seen in front of him
    - draw on paper with thick border, so contour easily detectable
    - draw with thick lines (probably using a marker)
    - crop and rectify image

- Have Cozmo move to his canvas from arbitrary location
  (providing he can see it). Maybe we can use an aruco-tag or just
  contour detection.

