#!/usr/bin/env python3
# Scorer
import cv2
import numpy as np
import os
import subprocess
import time
import enchant # install with 'sudo pip3 install PyEnchant'
import signal

# set use_picam to 1 to use camera, else use testcard.
use_picam = 1

# start picam if selected
if use_picam == 1:
   path = "raspistill -o /run/shm/test.jpg -n -t 0 -tl 0" 
   p = subprocess.Popen(path, shell=True, preexec_fn=os.setsid)
   time.sleep(1)

square = 67
board = int(square*15)

# variables
player = 0
p1_tot = 0
p2_tot = 0
z = 0
drawing = 0
total = 0
word = 0
l = 15
font = cv2.FONT_HERSHEY_SIMPLEX
letter = ["?","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?","?","?","?","?","?",]
score = [0,1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10,0,0,0,0,0,]

templates = []
if os.path.exists('templates.txt'):
   os.remove('templates.txt') 
path = "ls /home/pi/Templates/template_*.jpg >> templates.txt"
os.system (path)
time.sleep(1)
with open('templates.txt', 'r+') as f:
   for line in f.readlines():
      templates.append (line[0:len(line)-1])
      
global i
i = len(templates)
print (i)

def save_crop(event,x,y,flags,param):
   global x1,y1,x2,y2,i,frame,drawing,player,col
   # LEFT mouse button for PLAYER 1
   if event == cv2.EVENT_LBUTTONDOWN:
      if drawing == 0 and player == 0:
         drawing = 1
         player = 1
         col = (255,100,0)
         x1, y1 = x, y
         x1 = int(x1/square) * square
         y1 = int(y1/square) * square
      elif drawing == 1 and player == 1:
         x2, y2 = x, y
         x2 = (int(x2/square) + 1) * square
         y2 = (int(y2/square) + 1) * square
         drawing = 2
      elif drawing == 2 and player == 1:
         drawing = 3
         
      else:
         drawing = 0
         player = 0
         
   # RIGHT mouse button for PLAYER 2
   if event == cv2.EVENT_RBUTTONDOWN:
      if drawing == 0 and player == 0:
         drawing = 1
         player = 2
         col = (0,255,0)
         x1, y1 = x, y
         x1 = int(x1/square) * square
         y1 = int(y1/square) * square
      elif drawing == 1 and player == 2:
         x2, y2 = x, y
         x2 = (int(x2/square) + 1) * square
         y2 = (int(y2/square) + 1) * square
         drawing = 2
      elif drawing == 2 and player == 2:
         drawing = 3
         
      else:
         drawing = 0
         player = 0

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame',save_crop)

# board multipier values
boardm = [3,1,1,2,1,1,1,3,1,1,1,2,1,1,3,
          1,2,1,1,1,3,1,1,1,3,1,1,1,2,1,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          2,1,1,2,1,1,1,2,1,1,1,2,1,1,2,
          1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,
          1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          3,1,1,2,1,1,1,2,1,1,1,2,1,1,3,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,
          1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,
          2,1,1,2,1,1,1,2,1,1,1,2,1,1,2,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          1,2,1,1,1,3,1,1,1,3,1,1,1,2,1,
          3,1,1,2,1,1,1,3,1,1,1,2,1,1,3]

# board word(3) or letter(2) for multiplier
boardw = [3,1,1,2,1,1,1,3,1,1,1,2,1,1,3,
          1,3,1,1,1,2,1,1,1,2,1,1,1,3,1,
          1,1,3,1,1,1,2,1,2,1,1,1,3,1,1,
          2,1,1,3,1,1,1,2,1,1,1,3,1,1,2,
          1,1,1,1,3,1,1,1,1,1,3,1,1,1,1,
          1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          3,1,1,2,1,1,1,3,1,1,1,2,1,1,3,
          1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,
          1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,
          1,1,1,1,3,1,1,1,1,1,3,1,1,1,1,
          2,1,1,3,1,1,1,2,1,1,1,3,1,1,2,
          1,1,3,1,1,1,2,1,2,1,1,1,3,1,1,
          1,3,1,1,1,2,1,1,1,2,1,1,1,3,1,
          3,1,1,2,1,1,1,3,1,1,1,2,1,1,3]


score_board = np.zeros((15*square,400,3), np.uint8)
cv2.putText(score_board,("Press ESC to EXIT"), (1,l), font, .5, (0,0,255), 1)

# delete old crop
if os.path.exists("/home/pi/crop.jpg"):
       os.remove("/home/pi/crop.jpg")
       
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
       frame = cv2.imread('/home/pi/Templates/scboard7.jpg')
       
   det_word = []
   if os.path.exists("/home/pi/crop.jpg"):
      # check each tile in turn
       if y2-y1 > 0:
          j = 0
          k = y2-y1
          m = square
       else:
          j = (y1-y2) + square
          k = 0 - square
          m = 0 - square
       if x2-x1 > 0:
          n = 0
          o = x2-x1
          p = square
       else:
          n = (x1-x2) + square
          o = 0 - square
          p = 0 - square
       for y in range(j,k,m):
          for x in range(n,o,p):
              crop = cv2.imread("/home/pi/crop.jpg")
              crop_img = crop[y:y+square, x:x+square]
              gray_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
              word = 1
              temp_con = 0
              temp_zpos = 0
              temp_z = 0
              temp_letter = "-"
              # compare against all letter templates
              for z in range(1,i + 1):
                  s = "/home/pi/Templates/template_" + str(z) + ".jpg"
                  template = cv2.imread(s, cv2.IMREAD_GRAYSCALE)
                  # check against rotated letters
                  for ang in range(0,4):
                      template=cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
                      res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
                      _, confidence, _, _ = cv2.minMaxLoc(res)
                      loc = np.where(res >= 0.6)
                      # calculate letter position
                      for pt in zip(*loc[::-1]):
                          if x2 > x1 :
                             xpos = int((x + pt[0])/square) + int(x1/square)
                          else:
                             xpos = (int((x + pt[0])/square) + int(x1/square)) - (int((x1-x2)/square)+1)
                          if y2 > y1:   
                             ypos = int((y + pt[1])/square) + int(y1/square)
                          else:
                             ypos = (int((y + pt[1])/square) + int(y1/square)) - (int((y1-y2)/square)+1)
                          zpos = (ypos * 15) + xpos
                          # store highest confidence result
                          if confidence > temp_con:
                              temp_con = confidence
                              temp_zpos = zpos
                              temp_z = z
 
              det_word.append(temp_zpos)
              det_word.append(temp_z)
       out_word = ""
       
       # calculate word score
       for c in range(0,len(det_word),2):
              val = score[det_word[c + 1]]
              out_word += letter[det_word[c+1]]
              # double or treble letter
              if boardw[det_word[c]] == 2:
                 val = val * boardm[det_word[c]]
              total = total + val
              # double or treble word
              if boardw[det_word[c]] == 3 and word == 1:
                 word = boardm[det_word[c]]
              elif boardw[det_word[c]] == 3 and word > 1:
                 word = word * boardm[det_word[c]]
       # calculate double or treble word       
       if word > 1:
          total = total * word
       # confirm word with PyEnchant
       l += 15
       if out_word !="":
           d = enchant.Dict("en_UK")
           if d.check(out_word) == False:
               total = 0
               cv2.putText(score_board,("Player: " + str(player) + " Word: " + str(out_word) +  " INCORRECT"), (1,l), font, .5, (0,0,255), 1)
           else:
               cv2.putText(score_board,("Player: " + str(player) + " Word: " + str(out_word) +  " Score: " + str(total)), (1,l), font, .5, col, 1)
       else:
           total = 0
           cv2.putText(score_board,("Player: " + str(player) + " Word: ??? " +  " INCORRECT"), (1,l), font, .5, (0,0,255), 1)
       # add to player totals
       if player == 1:
          p1_tot +=total
       if player == 2:
          p2_tot +=total
       l += 15
       cv2.putText(score_board,("TOTALS: Player 1: " + str(p1_tot) + " Player 2: " + str(p2_tot)), (1,l), font, .5, (0,255,255), 1)
       player = 0
       if os.path.exists("/home/pi/crop.jpg") :
          os.remove("/home/pi/crop.jpg")
 
   # saving cropped word
   if drawing == 1:
      cv2.rectangle(frame, (x1,y1), (x1-1,y1-1), col, 2)
   elif drawing == 2:
      if x2>x1 and y2>y1:
         cv2.rectangle(frame, (x1-1,y1-1), (x2+1,y2+1), col, 2)
      elif x1>x2 and y2>y1:
         cv2.rectangle(frame, (x2-1-square,y1-1), (x1+1+ square,y2+1), col, 2)
      elif x2>x1 and y1>y2:
         cv2.rectangle(frame, (x1-1,y2-1-square), (x2+1,y1+1+square), col, 2)
   elif drawing == 3:
      if x2>x1 and y2>y1:
         crop_img = frame[y1:y2, x1:x2]
      elif x1>x2 and y2>y1:
         crop_img = frame[y1:y2, x2-square:x1+square]
      elif x2>x1 and y1>y2:
         crop_img = frame[y2-square:y1+square, x1:x2]
         
      cv2.imwrite("crop.jpg", crop_img)
      time.sleep(1)
      drawing = 0
  
   # show frame
   numpy_horizontal = np.hstack((frame,score_board))
   cv2.imshow("Frame", numpy_horizontal)
   if os.path.exists("/home/pi/crop.jpg") and z > 0:
       os.remove("/home/pi/crop.jpg")
       
   # reset total
   total = 0
   z = 0
   key = cv2.waitKey(1)
   # check for ESC key
   if key == 27:
      if use_picam == 1:
          os.killpg(p.pid, signal.SIGTERM)
      break

if use_picam == 1:
   os.killpg(p.pid, signal.SIGTERM)
cv2.destroyAllWindows()
