import os
import sys
import cv2
import numpy as np
import math
import time
import json
from multiprocessing import Process
from mss import mss
from PIL import Image
#from socketIO_client import SocketIO, LoggingNamespace
from socketIO_client_nexus import SocketIO, LoggingNamespace


def get_distance(pointA, pointB):
  x1, y1 = pointA
  x2, y2 = pointB
  return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

def detect():
  global src, rect, img, height, width, left, right, top, bottom

  cannyThreshold1 = 150
  cannyThreshold2 = 50
  minLineLengh = 100
  #lineIndex = -1
  #thetaParam = 0

  # Get raw pixels from the screen, save it to a Numpy array
  img = np.array(sct.grab(rect))

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (11, 11), 0)
  edges = cv2.Canny(blurred, cannyThreshold1, cannyThreshold2, apertureSize = 3)
  lines = cv2.HoughLines(edges, 1, np.pi/180, minLineLengh)

  left = 0
  right = width
  top = 0
  bottom = height

  left_theta = 0
  right_theta = width
  top_theta = 0
  bottom_theta = height

  for i in range(0, len(lines)):
    for rho, theta in lines[i]:
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))
      
      # horizontal
      if theta > 1.31 and theta < 1.6:
        if y0 < height / 2: # top side of the screen
          if y0 > top:
            top = y0
            top_theta = theta
        else: # bottom side of the screen
          if y0 < bottom:
            bottom = y0
            bottom_theta = theta

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

      # vertical
      if theta < 0.34 or theta > 2.8:
        if x0 < width / 2: # left side of screen
          if x0 > left:
            left = x0  
            left_theta = theta
        else: # right side of screen
          if x0 < right:
            right = x0
            right_theta = theta

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
    left_frame_length = get_distance((left, top), (left, bottom))

    cv2.line(img, (left, top), (right, top), (0, 0, 255), 2) # top
    cv2.line(img, (left, bottom), (right, bottom), (0, 0, 255), 2) # bottom
    cv2.line(img, (left, top), (int(left - left_frame_length * np.sin(left_theta)), bottom), (0, 0, 255), 2) # left
    cv2.line(img, (right, top), (right, bottom), (0, 0, 255), 2) # right

    cv2.circle(img, (left, top), 5, (0, 255, 255))
    cv2.circle(img, (left, bottom), 5, (0, 255, 255))
    cv2.circle(img, (right, top), 5, (0, 255, 255))
    cv2.circle(img, (right, bottom), 5, (0, 255, 255))
    cv2.circle(img, (width/2, height/2), 5, (0, 255, 255))

    # lines = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLengh)
    # for i in range(0, len(lines)):
    #   for x1, y1, x2, y2 in lines[i]:
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Display the picture
    #cv2.imshow("gray", gray)

    # keyPress = cv2.waitKey(0)
    # if keyPress == 27: # escape
    #   cv2.destroyAllWindows()

def socketInit():
    socketIO.on('connect', onConnect)
    socketIO.on('reconnect', onReconnect)
    socketIO.on('disconnect', onDisconnect)

def onConnect():
    print('!CONNECT!')

def onDisconnect():
    print('!DISCONNECT!')

def onReconnect():
    print('!RECONNECT!')
    socketInit()
#------------------------------------------------------------------------------
# Global
#------------------------------------------------------------------------------
sct = mss()
rect = {"top": 70, "left": 132, "width": 632, "height": 352} # DELL MONITOR
#rect = {"top": 65, "left": 150, "width": 580, "height": 322} # MAC MONITOR
img = np.array(sct.grab(rect))
height, width, channel = img.shape
left = 0
right = width
top = 0
bottom = height

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':

  # with SocketIO('localhost', 3001, LoggingNamespace) as socketIO:
  #   socketIO.emit('aaa')
  #   socketIO.wait(seconds=1)
  with SocketIO('127.0.0.1', 3001, LoggingNamespace) as socketIO:
    socketInit()
    try:
      while True:
        time.sleep(0.5)
        detect()
        cv2.imshow("obs", img)
        cv2.waitKey(1)

        # get coords
        tl = {"x": float(left), "y": float(top)} #.x .y
        tr = {"x": float(right), "y": float(top)} #.x .y
        bl = {"x": float(left), "y": float(bottom)} #.x .y
        br = {"x": float(right), "y": float(bottom)} #.x .y
        print tl, tr, bl, br
        socketIO.emit('update_corners',[tl, tr, br, bl]) # order here must match frontend
    except KeyboardInterrupt:
      print 'Interrupted'






