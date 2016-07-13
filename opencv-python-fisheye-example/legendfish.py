import cv2
import numpy as np
import sys
import time
assert float(cv2.__version__.rsplit('.', 1)[0]) >= 3, 'OpenCV version 3 or newer required.'

#K = np.array([[  357.64,     0.  ,  285.71],
#              [    0.  ,   357.64,  226.71],
#              [    0.  ,     0.  ,    1.  ]])

K = np.array([[  220.8,     0.  ,  297.56],
              [    0.  ,   220.8,  228.39],
              [    0.  ,     0.  ,    1.  ]])
# zero distortion coefficients work well for this image
# D = np.array([-0.6258, 0.318, 0.0073, 0.00256])
D = np.array([-0.3696, 0.1389, 0.012445, 0.014345])

# use Knew to scale the output
Knew = K.copy()
Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]
input = sys.argv[1]
output = sys.argv[2]

img = cv2.imread(input)
w = int(640*1.5)
h = int(480*1.5)
newSize = (w, h)

start = time.time()
img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
end = time.time()
t = end - start
print t
cv2.imwrite(output, img_undistorted)
cv2.imshow('undistorted', img_undistorted)
cv2.waitKey()

