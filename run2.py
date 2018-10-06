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
  global src, rect, img, height, width, tl, tr, bl, br, debug_mode

  cannyThreshold1 = 150
  cannyThreshold2 = 50
  minLineLengh = 110
  #lineIndex = -1
  #thetaParam = 0

  # Get raw pixels from the screen, save it to a Numpy array
  img = np.array(sct.grab(rect))

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  #blurred = cv2.GaussianBlur(gray, (13, 13), 0)
    
  ret,thresh = cv2.threshold(gray,100,255,1)
  #contours,h = cv2.findContours(thresh,1,2)
  cv2.imshow("thresh", thresh)

  _, contours, _=cv2.findContours(thresh,1,2)
  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==5:
      print "pentagon"
      cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
      print "triangle"
      cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
      print "square"
      cv2.drawContours(img,[cnt],0,(0,0,255),-1)

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
debug_mode = False
sct = mss()
#rect = {"top": 70, "left": 132, "width": 632, "height": 352} # DELL MONITOR
#rect = {"top": 65, "left": 150, "width": 580, "height": 322} # MAC MONITOR
rect = {"top": 47, "left": 0, "width": 1917, "height": 1053} # QUICK TIME
#rect = {"top": 91, "left": 0, "width": 1280, "height": 800} # GAME

img = np.array(sct.grab(rect))
height, width, channel = img.shape
banner = cv2.imread('banner.png', cv2.IMREAD_UNCHANGED)
banner_height, banner_width, banner_channels = banner.shape

tl = (int(0), int(0))
tr = (int(0), int(width))
bl = (int(height), int(0))
br = (int(height), int(width))

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':

  if len(sys.argv) > 1 and sys.argv[1] == 'DEBUG':
    print 'DEBUG MODE'
    debug_mode = True
  # with SocketIO('localhost', 3001, LoggingNamespace) as socketIO:
  #   socketIO.emit('aaa')
  #   socketIO.wait(seconds=1)
  with SocketIO('127.0.0.1', 3001, LoggingNamespace) as socketIO:
    socketInit()
    try:
      while True:
        time.sleep(0.03)
        detect()
        if debug_mode:
          cv2.imshow("obs", cv2.resize(img, (width // 2, height // 2)))
          #cv2.imshow("banner", banner)
          cv2.waitKey(1)
        # get coords
        array = [[int(tl[0]), int(tl[1])],[int(tr[0]), int(tr[1])],[int(br[0]), int(br[1])],[int(bl[0]), int(bl[1])]]
        quad = np.float32(array)
        source = np.float32([[0,0],[banner_width,0],[banner_width,banner_height],[0,banner_height]])

        M = cv2.getPerspectiveTransform(source, quad)
        warped = cv2.warpPerspective(banner, M, (width, height))
        #background = Image.new('RGBA', (banner_width, banner_height), (255, 0, 0, 255))
        #warped = cv2.cvtColor(warped, cv2.COLOR_BGR2RGBA)
        warped[np.all(warped == [0, 0, 0, 0], axis=2)] = [0, 255, 0, 255]
        cv2.imshow("warped", cv2.resize(warped, (banner_width // 2, banner_height // 2)))
        cv2.waitKey(1)


        #socketIO.emit('update_corners',[tl, tr, br, bl]) # order here must match frontend
    except KeyboardInterrupt:
      print 'Interrupted'
