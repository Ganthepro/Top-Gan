from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

filename = "HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=-1
scale=10
im = Image.new('RGBA', (wx*scale, hy*scale), (255, 255, 255, 255))
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize_cv2 = cv2.resize(img_cv2,(wx*scale,hy*scale))
resize = img.resize((wx*scale,hy*scale))
n_wx, n_hy = resize.size
vec=[]
RGB=[]
colors=[]
idx=-1
previous = 1
for y in range(hy):
    for x in range(wx):
        if y-1<0:#บน
            b=px[x,y]
        else:
            b=px[x,y-1]
        if x+1==wx:#ขวา
            c=px[x,y]
        else:
            c=px[x+1,y]
        if y - 1 < 0:#บน
            d = px[x,y]
        else:
            d = px[x,y-1]
        if x - 1 < 0:#ซ้าย
            e=px[x,y]
        else:
            e=px[x-1,y]
        if y+1 >= hy:#ล่าง
            f=px[x,y]
        else:
            f=px[x,y+1]
        if y+1 == hy:
            g = px[x, y]
        elif x+1==wx:#ล่างขวา
            g=px[x,y]
        else:
            g=px[x+1,y+1]
        if y+1 == hy:
            h = px[x, y]
        elif x-1<0:#ล่างซ้าย
            h=px[x,y]
        else:
            h=px[x-1,y+1]
        if y-1 < 0:
            j = px[x, y]
        elif x+1==wx:#บนขวา
            j=px[x,y]
        else:
            j=px[x+1,y-1]
        if y-1 < 0:
            k = px[x, y]
        elif x-1<0:#บนซ้าย
            k=px[x,y]
        else:
            k=px[x-1,y-1]
        if px[x,y] != b and px[x,y] != c:
            idx += 1;
            vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        elif px[x,y] == e:
            if px[x,y] != b:
                idx += 1;
                vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        elif px[x, y] == b:
            if px[x, y] != c:
                if px[x, y] == j:
                    pass
                else:
                    idx += 1;
                    vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        if px[x,y] != b and px[x,y] != e:
            idx += 1;
            vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
            pass
        elif px[x, y] != f and px[x, y] != c:
            pass
        # elif px[x, y] != h:
        #     pass
        elif px[x, y] != e and px[x, y] == b:
            if px[x, y] == k:
                pass
            else:
                idx += 1;
                vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
            if px[x, y] == j:
                pass
            else:
                idx += 1;
                vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]

px_im = im.load()

draw = ImageDraw.Draw(im)

for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift*scale,
            (i[sy]*scale)+yshift*scale,
            (i[ex]*scale)+xshift*scale,
            (i[ey]*scale)+yshift*scale
        ), fill=(0, 255, 0, 255))
start_stop_p = []
line_vec = []
px2=im.load()
link_im = Image.new('RGBA',(n_wx,n_hy),(255,255,255,255))
px_link_im = link_im.load()
point = ['','']
for wx in range(n_wx):
    R_ran = random.randrange(0, 255, 1)
    G_ran = random.randrange(0, 255, 1)
    B_ran = random.randrange(0, 255, 1)
    hy = 0
    if px_im[wx,hy] == (0,255,0,255) and px_link_im[wx,hy] == (255,255,255,255):
        link_im.putpixel((wx, hy), (R_ran, G_ran, B_ran, 255))
        start_stop_p.append([wx, hy])
        #print(start_stop_p)
        point[0] = wx
        point[1] = hy
        round_1 = 0
        #print(len(start_stop_p))
        while point[0] <= n_wx and point[1] <= n_hy:
            x = point[0]
            y = point[1]
            r = 0
            if y - 1 < 0:  # บน
                top = px_im[x, y]
                top_link = px_link_im[x, y]
            else:
                top = px_im[x, y - 1]
                top_link = px_link_im[x, y - 1]
            if x + 1 == n_wx:  # ขวา
                right = px_im[x, y]
                right_link = px_link_im[x, y]
            else:
                right = px_im[x + 1, y]
                right_link = px_link_im[x + 1, y]
            if x - 1 < 0:  # ซ้าย
                left = px_im[x, y]
                left_link = px_link_im[x, y]
            else:
                left = px_im[x - 1, y]
                left_link = px_link_im[x - 1, y]
            if y + 1 >= n_hy:  # ล่าง
                bottom = px_im[x, y]
                bottom_link = px_link_im[x, y]
            else:
                bottom = px_im[x, y + 1]
                bottom_link = px_link_im[x, y + 1]
            if y + 1 == n_hy:
                bottom_right = px_im[x, y]
                bottom_right_link = px_link_im[x, y]
            elif x + 1 == n_wx:  # ล่างขวา
                bottom_right = px_im[x, y]
                bottom_right_link = px_link_im[x, y]
            else:
                bottom_right = px_im[x + 1, y + 1]
                bottom_right_link = px_link_im[x + 1, y + 1]
            if y + 1 == n_hy:
                bottom_left = px_im[x, y]
                bottom_left_link = px_link_im[x, y]
            elif x - 1 < 0:  # ล่างซ้าย
                bottom_left = px_im[x, y]
                bottom_left_link = px_link_im[x, y]
            else:
                bottom_left = px_im[x - 1, y + 1]
                bottom_left_link = px_link_im[x - 1, y + 1]
            if y - 1 < 0:
                top_right = px_im[x, y]
                top_right_link = px_link_im[x, y]
            elif x + 1 == n_wx:  # บนขวา
                top_right = px_im[x, y]
                top_right_link = px_link_im[x, y]
            else:
                top_right = px_im[x + 1, y - 1]
                top_right_link = px_link_im[x + 1, y - 1]
            if y - 1 < 0:
                top_left = px_im[x, y]
                top_left_link = px_link_im[x, y]
            elif x - 1 < 0:  # บนซ้าย
                top_left = px_im[x, y]
                top_left_link = px_link_im[x, y]
            else:
                top_left = px_im[x - 1, y - 1]
                top_left_link = px_link_im[x - 1, y - 1]
            if round_1 > 1:
                break
            positions = [[top, (x,y - 1), top_link], [right, (x + 1, y), right_link], [bottom, (x,y + 1), bottom_link],
                         [left, (x - 1, y), left_link], [top_right, (x + 1,y - 1), top_right_link],
                         [top_left, (x - 1,y - 1), top_left_link], [bottom_right, (x + 1,y + 1), bottom_right_link],
                         [bottom_left, (x - 1,y + 1), bottom_left_link]]
            if px_link_im[x, y] != (255, 255, 255, 255):
                direction = 0
                for position in positions:
                    if position[0] == (0, 255, 0, 255):
                        if position[1][1] <= -2 or position[1][0] <= -2 or position[1][1] >= n_hy or position[1][0] >= n_wx or position[1][0] == r or position[1][1] == r:
                            print(position[1])
                            pass
                        elif position[2] == px_link_im[x, y]:
                            continue
                        else:
                            direction += 1
                            if direction == 2:
                                direction = 0
                                break
                            link_im.putpixel(position[1], px_link_im[x, y])
                            if position[1][0] > point[0]:
                                point[0] += 1
                            if position[1][0] < point[0]:
                                point[0] -= 1
                            if position[1][1] > point[1]:
                                point[1] += 1
                            if position[1][1] < point[1]:
                                point[1] -= 1
                            if point[0] == 1 or point[1] == 1 or point[0] == n_wx + yshift or point[1] == n_hy - scale:
                                round_1 += 1
                                #print(round_1)
                            #print(point)

#print(start_stop_p)


image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
image_link_cv2 = cv2.cvtColor(np.array(link_im),cv2.COLOR_RGB2BGR)
original_cv2 = cv2.imread(filename)
link_im.show('test_link.png')
"""image = ImageTk.PhotoImage(im)
new_window = Toplevel(window)
panel1 = Label(new_window, image=image)
panel1.pack()"""
cv2.imwrite('test_link.png',image_link_cv2)
plt.imshow(image_cv2)
plt.show()

# pic=ImageTk.PhotoImage(img)
# panel = Label(window, image=pic)
# panel.pack()

#window.mainloop()
