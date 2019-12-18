#!/usr/bin/env python3
# Template Maker
import cv2
import numpy as np
import os,subprocess
import time
import signal

# set use_picam to 1 to use camera, else use testcard.
use_picam = 0

# set variables
square = 67
board = int(square*15)
font = cv2.FONT_HERSHEY_SIMPLEX
letters = ["-","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
out = 1

# start picam if selected
if use_picam == 1:
   path = "raspistill -o /run/shm/test.jpg -n -t 0 -tl 0" 
   p = subprocess.Popen(path, shell=True, preexec_fn=os.setsid)
   time.sleep(1)

# read mouse
    
def save_crop(event,x,y,flags,param):
   global x1,y1,x2,y2,i,frame,drawing,out
   if event == cv2.EVENT_LBUTTONDOWN:
      if drawing == 0:
         drawing = 1
         x1, y1 = x, y
      elif drawing == 1:
         drawing = 2
         x2, y2 = x, y
      elif drawing == 2:
         drawing = 3
      else:
         drawing = 0

   if event == cv2.EVENT_RBUTTONDOWN:
         if drawing > 0:
            drawing = 0
         else:
            out +=1
            if out > 26:
               out = 1

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame',save_crop)
drawing = 0

while True:
   # get frame form picam if selected
   if use_picam == 1:
       if not os.path.exists('/run/shm/test.jpg'):
           time.sleep(.1)
       c_frame = cv2.imread('/run/shm/test.jpg')
       e,f,g = c_frame.shape
       frame = c_frame[int(e/2)-int(board/2):(int(e/2)-int(board/2)) + board, int(f/2)-int(board/2):(int(f/2)-int(board/2)) + board]
   # else load testcard
   else:
       frame = cv2.imread('/home/pi/Templates/board.jpg')
   gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
   # show grids for aligning
   cv2.rectangle(frame, (0,0), (square,square), (0,255, 0), 1)
   cv2.rectangle(frame, (14*square,0), (15*square,square), (0,255, 0), 1)
   cv2.rectangle(frame, (0,14*square), (square,15*square), (0,255, 0), 1)
   cv2.rectangle(frame, (14*square,14*square), (15*square,15*square), (0,255, 0), 1)
   cv2.rectangle(frame, (7*square,7*square), (8*square,8*square), (0,255, 0), 1)
   cv2.rectangle(frame, (3*square,7*square), (4*square,8*square), (0,255, 0), 1)
   cv2.rectangle(frame, (7*square,3*square), (8*square,4*square), (0,255, 0), 1)
   cv2.rectangle(frame, (11*square,7*square), (12*square,8*square), (0,255, 0), 1)
   cv2.rectangle(frame, (7*square,0*square), (8*square,square), (0,255, 0), 1)
   cv2.rectangle(frame, (7*square,14*square), (8*square,15*square), (0,255, 0), 1)

   # saving templates
   if drawing == 0:
      cv2.rectangle(frame, (75,6), (925,65), (50,50, 50),cv2.FILLED)
      cv2.putText(frame,("Identify Letter: " + letters[out]), (90,25), font, .7, (0,255,0), 2)
      cv2.putText(frame,(" Click LEFT mouse to define TOP LEFT corner OR click RIGHT mouse for next LETTER.., ESC to exit"), (80,50), font, .5, (0,255,0), 2)
   elif drawing == 1:
      cv2.rectangle(frame, (75,6), (925,65), (50,50, 50),cv2.FILLED)
      cv2.putText(frame,("Identify Letter: " + letters[out]), (90,25), font, .7, (0,255,0), 2)
      cv2.rectangle(frame, (x1,y1), (x1-1,y1-1), (0,255, 0), 1)
      cv2.putText(frame,(" Click LEFT mouse to define BOTTOM RIGHT corner..., ESC to exit"), (80,50), font, .5, (0,255,255), 2)
   elif drawing == 2:
      cv2.rectangle(frame, (75,6), (925,65), (50,50, 50),cv2.FILLED)
      cv2.putText(frame,("Identify Letter: " + letters[out]), (90,25), font, .7, (0,255,0), 2)
      cv2.putText(frame,(" Click LEFT mouse to SAVE OR click RIGHT mouse to ABORT.., ESC to exit"), (80,50), font, .5, (0,0,255), 2)
      cv2.rectangle(frame, (x1-1,y1-1), (x2+1,y2+1), (0, 255, 0), 1)
   if drawing == 3:
      crop_img = frame[y1:y2, x1:x2]
      cv2.imwrite("/home/pi/Templates/template_" + str(out) + ".jpg", crop_img)
      drawing = 0
      
   # show frame
   cv2.imshow("Frame", frame)
   key = cv2.waitKey(1)
   # ESCAPE
   if key == 27:
      if use_picam == 1:
          os.killpg(p.pid, signal.SIGTERM)
      break

if use_picam == 1:
   os.killpg(p.pid, signal.SIGTERM)
cv2.destroyAllWindows()
