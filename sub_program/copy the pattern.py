import cv2
import numpy as np
try:
    size_input = int(input('Size : '))
    img = cv2.imread(r'C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\34344.png', 0)
    original_img = cv2.imread(r'C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\34344.png')
    if size_input % 2 != 1:
        size_input += 1
    resize = cv2.resize(img, (size_input*100, size_input*100))
    resize_original = cv2.resize(original_img, (size_input * 100, size_input * 100))
    adaptive = cv2.adaptiveThreshold(resize,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,35,7)
    color = cv2.cvtColor(adaptive,cv2.COLOR_BGR2RGB)
    color[np.where((color==[0, 0, 0]).all(axis=2))] = [0, 255, 255] # color""""""
    color[np.where((color==[255, 255, 255]).all(axis=2))] = [0, 0, 0]
    #kernal = np.ones((1,2),np.uint8)
    #morpho = cv2.morphologyEx(color,cv2.MORPH_OPEN,kernal)
    #cv2.imshow('test',resize_original)
    cv2.imshow('result',color)
    cv2.imwrite('test_cat.png',color)
    #cv2.imshow('morpho',morpho)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print(e)