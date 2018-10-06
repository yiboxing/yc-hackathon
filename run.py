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
  minLineLength = 60
  maxLineGap = 20

  # Get raw pixels from the screen, save it to a Numpy array
  img = np.array(sct.grab(rect))

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ret,thresh = cv2.threshold(gray,60,255,1)
  cv2.imshow("ret", cv2.resize(thresh, (width // 2, height // 2)))

  blurred = cv2.GaussianBlur(thresh, (9, 9), 0)
  edges = cv2.Canny(blurred, cannyThreshold1, cannyThreshold2, apertureSize = 7)
  lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = 30, minLineLength = minLineLength, maxLineGap = maxLineGap)
  vertical_lines = []
  if lines is not None:
    for i in range(0, len(lines)):
      for x1, y1, x2, y2 in lines[i]:
        if abs(y1 - y2) > 180 and abs(x1 - x2) < 50:
          cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
          vertical_lines.append([x1, y1, x2, y2])
  # left_index = -1
  # right_index = -1
  # max_vertical_cluster_gap = 0
  # for i in range(1, len(vertical_cluster)):
  #   if abs(vertical_cluster[i][0] - vertical_cluster[i - 1][0]) > max_vertical_cluster_gap:
  #     max_vertical_cluster_gap = abs(vertical_cluster[i][0] - vertical_cluster[i - 1][0])
  #     left_index = i - 1
  #     right_index = i

  # # left and right
  # if left_index != -1:
  #   rho, theta = vertical_cluster[left_index]
  #   a = np.cos(theta)
  #   b = np.sin(theta)
  #   x0 = a*rho
  #   y0 = b*rho
  #   x1 = int(x0 + 500*(-b))
  #   y1 = int(y0 + 500*(a))
  #   x2 = int(x0 - 500*(-b))
  #   y2 = int(y0 - 500*(a))
  #   cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
  # if right_index != -1:
  #   rho, theta = vertical_cluster[right_index]
  #   a = np.cos(theta)
  #   b = np.sin(theta)
  #   x0 = a*rho
  #   y0 = b*rho
  #   x1 = int(x0 + 500*(-b))
  #   y1 = int(y0 + 500*(a))
  #   x2 = int(x0 - 500*(-b))
  #   y2 = int(y0 - 500*(a))
  #   cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

  # # for i in range(0, len(vertical_cluster)):
  #   rho, theta = vertical_cluster[i]
  #   a = np.cos(theta)
  #   b = np.sin(theta)
  #   x0 = a*rho
  #   y0 = b*rho
  #   x1 = int(x0 + 500*(-b))
  #   y1 = int(y0 + 500*(a))
  #   x2 = int(x0 - 500*(-b))
  #   y2 = int(y0 - 500*(a))
  #   cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)



  # draw white left
  # boundry = []
  # boundry.append(top_index)
  # boundry.append(bottom_index)
  # boundry.append(left_index)
  # boundry.append(right_index)

  # for i in range(0, len(boundry)):
  #   for rho, theta in lines[boundry[i]]:
  #     a = np.cos(theta)
  #     b = np.sin(theta)
  #     x0 = a*rho
  #     y0 = b*rho
  #     x1 = int(x0 + 1000*(-b))
  #     y1 = int(y0 + 1000*(a))
  #     x2 = int(x0 - 1000*(-b))
  #     y2 = int(y0 - 1000*(a))
  #     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
  #     cv2.circle(img, (x1, y1), 10, (255, 255, 255))
  #     cv2.circle(img, (x2, y2), 10, (255, 255, 255))
    
  # left_frame_length = get_distance((left, top), (left, bottom))
  # right_frame_length = get_distance((right, top), (right, bottom))

  # tl_x = left
  # tl_y = top
  # tr_x = right
  # tr_y = int(top - (right - left) * np.cos(top_theta))

  # bl_x = int(left - (bottom - top) * np.sin(left_theta))
  # bl_y = bottom
  # br_x = int(right + (bottom - top) * np.sin(right_theta))
  # br_y = int(bottom - (right - left) * np.cos(bottom_theta))

  # tl = (int(tl_x), int(tl_y))
  # tr = (int(tr_x), int(tr_y))
  # bl = (int(bl_x), int(bl_y))
  # br = (int(br_x), int(br_y))

  # if debug_mode:
  #   cv2.line(img, (tl_x, tl_y), (tr_x, tr_y), (0, 0, 255), 2) # top
  #   cv2.line(img, (bl_x, bl_y), (br_x, br_y), (0, 0, 255), 2) # bottom
  #   cv2.line(img, (tl_x, tl_y), (bl_x, bl_y), (0, 0, 255), 2) # left
  #   cv2.line(img, (tr_x, tr_y), (br_x, br_y), (0, 0, 255), 2) # right

  #   # cv2.circle(img, (left, top), 5, (0, 255, 255))
  #   # cv2.circle(img, (left, bottom), 5, (0, 255, 255))
  #   # cv2.circle(img, (right, top), 5, (0, 255, 255))
  #   # cv2.circle(img, (right, bottom), 5, (0, 255, 255))
  #   cv2.circle(img, (width/2, height/2), 10, (0, 255, 255))

  #   lines = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLengh)
  #   for i in range(0, len(lines)):
  #     for x1, y1, x2, y2 in lines[i]:
  #       cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

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






