import cv2

img = cv2.imread(r"pic\0_RdPUay-F2l6VIIFV.jpg")
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert_img = cv2.bitwise_not(grey_img)
blur_img=cv2.GaussianBlur(invert_img, (111,111),0)
invblur_img=cv2.bitwise_not(blur_img)
sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)
blackandwhite = cv2.cvtColor(sketch_img,cv2.COLOR_)
adaptive = cv2.adaptiveThreshold(sketch_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 9)
cv2.imshow("Test", adaptive)
cv2.waitKey(0)
cv2.destroyAllWindows()
# sdf