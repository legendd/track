import numpy as np
import argparse
import cv2
import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)

frame = None
roiPts = []
inputMode = False
rcv_flag = False
port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1.0)

roiPts_img = [(50, 50), (50, 60), (60, 50), (60, 60)]

camera = cv2.VideoCapture(0)
img = cv2.imread('red.png')
cv2.namedWindow("frame")

termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
roiBox = None

while True:
	rcv = port.read()
	if(rcv == 'z'):
		rcv_flag = True
		break
	else:
		rcv_flag = False

while rcv_flag==True:
	(grabbed, frame) = camera.read()
	if not grabbed:
		print "NOT GRABBED"
		break
	if roiBox is not None:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
		(r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
		pts = np.int0(cv2.boxPoints(r))
		pts_x = str((pts[0][0]+pts[1][0]+pts[2][0]+pts[3][0])/4)
		pts_y = str((pts[0][1]+pts[1][1]+pts[2][1]+pts[3][0])/4)
		if pts_x == '0' or pts_y == '0':
			print"aaaaa"
			GPIO.output(4,0)
		else:
			pts_xy = pts_x + pts_y
			print pts_xy
			GPIO.output(4,1)
		#input = np.array([pts_x_int, pts_y_int])
		#output = np.zeros((1,2))
		#output = cv2.undistortPoints(input, camera_matrix, dist_coeffs)
		
		# Serial Write
			port.write("s")
			port.write(pts_xy)
			port.write("q")
		cv2.polylines(frame, [pts], True, (255, 0, 0), 4)
	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if rcv_flag == True :
		inputMode = True
		orig = img.copy()
		cv2.imshow("frame", frame)

		tl = roiPts_img[0]
		br = roiPts_img[3]
		roi = orig[tl[1]:br[1], tl[0]:br[0]]
		roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
		roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
		roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
		roiBox = (tl[0], tl[1], br[0], br[1])
	if key == ord("q"):
		break
camera.release()
cv2.destoyAllWindows()

