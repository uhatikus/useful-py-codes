import numpy as np
import cv2
import matplotlib.pyplot as plt
%matplotlib inline 



img_1 = cv2.imread('image/H1_ex1.png')

img_1_g=cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
img_1_g=img_1
img_2=cv2.imread('image/H1_ex2.png')
img_2_g=cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
img_2_g=img_2

surf = cv2.xfeatures2d.SURF_create()
keypoints_surf_1, descriptors_1 = surf.detectAndCompute(img_1_g, None)
keypoints_surf_2, descriptors_2 = surf.detectAndCompute(img_2_g, None)

#bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)

# Match descriptors.
matches = bf.match(descriptors_1,descriptors_2)
matches = sorted(matches, key = lambda x:x.distance)


src_pts = np.float32([keypoints_surf_1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints_surf_2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)



img_2_pred = cv2.warpPerspective(img_1_g, M, (img_2_g.shape[1], img_2_g.shape[0]))


C = np.dstack((img_2_pred,img_2_g,img_2_pred))
cv2.imshow("Linear Blend",C)
cv2.waitKey(0)
cv2.destroyAllWindows()