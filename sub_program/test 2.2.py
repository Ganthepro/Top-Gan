from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
import math

filename = r"C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\H1042-16-SAM1.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=-1
scale=1
bg_color = [0,0,1]
im = Image.new('RGBA', (wx*scale, hy*scale), (bg_color[0], bg_color[1], bg_color[2], 255))
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize_cv2 = cv2.resize(img_cv2,(wx*scale,hy*scale))
resize = img.resize((wx*scale,hy*scale))
n_wx, n_hy = resize.size
path = 'Desktop'
vec=[]
RGB=[]
colors=[]
idx=-1
previous = 1
for y in range(hy):
    for x in range(wx):
        # if y - 1 < 0:  # บน
        #     b = px[x, y]
        # else:
        #     b = px[x, y - 1]
        # if x + 1 == wx:  # ขวา
        #     c = px[x, y]
        # else:
        #     c = px[x + 1, y]
        # if y - 1 < 0:  # บน
        #     d = px[x, y]
        # else:
        #     d = px[x, y - 1]
        # if x - 1 < 0:  # ซ้าย
        #     e = px[x, y]
        # else:
        #     e = px[x - 1, y]
        # if y + 1 >= hy:  # ล่าง
        #     f = px[x, y]
        # else:
        #     f = px[x, y + 1]
        # if y + 1 == hy:
        #     g = px[x, y]
        # elif x + 1 == wx:  # ล่างขวา
        #     g = px[x, y]
        # else:
        #     g = px[x + 1, y + 1]
        # if y + 1 == hy:
        #     h = px[x, y]
        # elif x - 1 < 0:  # ล่างซ้าย
        #     h = px[x, y]
        # else:
        #     h = px[x - 1, y + 1]
        # if y - 1 < 0:
        #     j = px[x, y]
        # elif x + 1 == wx:  # บนขวา
        #     j = px[x, y]
        # else:
        #     j = px[x + 1, y - 1]
        # if y - 1 < 0:
        #     k = px[x, y]
        # elif x - 1 < 0:  # บนซ้าย
        #     k = px[x, y]
        # else:
        #     k = px[x - 1, y - 1]
        # if px[x, y] != b and px[x, y] != c:
        #     idx += 1;
        #     vec.append([idx - 1, x * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] == e:
        #     if px[x, y] != b:
        #         idx += 1;
        #         vec.append([idx - 1, x * scale, y * scale, (x + 1) * scale, y * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] == b:
        #     if px[x, y] != c:
        #         if px[x, y] == j:
        #             pass
        #         else:
        #             idx += 1;
        #             vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # if px[x, y] != b and px[x, y] != e:
        #     idx += 1;
        #     vec.append([idx - 1, x * scale, (y + 1) * scale, (x + 1) * scale, y * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
        #     pass
        # elif px[x, y] != f and px[x, y] != c:
        #     pass
        # # elif px[x, y] != h:
        # #     pass
        # elif px[x, y] != e and px[x, y] == b:
        #     if px[x, y] == k:
        #         pass
        #     else:
        #         idx += 1;
        #         vec.append([idx - 1, x * scale, y * scale, x * scale, (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
        #     if px[x, y] == j:
        #         pass
        #     else:
        #         idx += 1;
        #         vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
            
        if y - 1 < 0:
            b = px[x, y]
        else:
            b = px[x, y - 1]
        if x + 1 == wx:
            c = px[x, y]
        else:
            c = px[x + 1, y]
        if px[x, y] != b:
            idx += 1;
            vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
        if px[x, y] != c:
            idx += 1;
            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
        RGB.append([red,green,blue])
        im.putpixel((x * scale, y * scale), (red,green,blue))

px_im = im.load()

for_len = 0
#print(len(RGB))
#print(vec)
n_vec = []
semi_vec = []
for k,n in enumerate(vec):
    for i in vec:
        if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
            # n_vec.append(n)/
            # n_vec.append(i)\
            semi_vec.append(n)
            semi_vec.append(i)
            n_vec.append([n[0],n[sx],n[sy],n[ex] - math.ceil(scale / 2),n[ey] + math.ceil(scale / 2)])
            n_vec.append([i[0],i[sx] + math.ceil(scale / 2),i[sy]  + math.ceil(scale / 2),i[ex],i[ey]])  
    print('loading ' + "{:.2f}".format(0 + ((k * 100) / len(vec))) + ' %')
            # print(n,i)

for i in vec:
    if i in semi_vec:pass
    else:n_vec.append(i)
    
vec = n_vec

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x,y]
        colors.append(color)
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x,y] == (bg_color[0], bg_color[1], bg_color[2],255) and px_im[x,y] != e:
            im.putpixel((x, y), (e[0], e[1], e[2]))

#print(RGB)
draw = ImageDraw.Draw(im)

for i in vec:
    draw.line(
        (   (i[sx])+xshift,
            (i[sy])+yshift,
            (i[ex])+xshift,
            (i[ey])+yshift
        ), fill=(255, 0, 0, 255))

print('loading 25%')

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x,y]
        colors.append(color)
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x,y] == (bg_color[0], bg_color[1], bg_color[2],255) and px_im[x,y] != b and b != (255, 0, 0, 255):
            im.putpixel((x, y), (b[0], b[1], b[2]))
print('loading 45%')
for y in reversed(range(n_hy)):
    for x in range(n_wx):
        if y+1 >= n_hy:#ล่าง
            f=px_im[x,y]
        else:
            f=px_im[x,y+1]
        if px_im[x,y] == (bg_color[0], bg_color[1], bg_color[2],255) and px_im[x,y] != f and f != (255, 0, 0, 255):
            im.putpixel((x, y), (f[0], f[1], f[2]))
print('loading 60%')
for y in range(n_hy):
    for x in range(n_wx):
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (255, 0, 0, 255):
            im.putpixel((x, y), (e[0], e[1], e[2]))
print('loading 75%')
for y in range(n_hy):
    for x in reversed(range(n_wx)):
        if x+1==n_wx:#ขวา
            c=px_im[x,y]
        else:
            c=px_im[x+1,y]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (255, 0, 0, 255):
            im.putpixel((x, y), (c[0], c[1], c[2]))
print('loading 85%')
# for y in range(n_hy):
#     for x in range(n_wx):
#         if x - 1 < 0:  # ซ้าย
#             e = px_im[x, y]
#         else:
#             e = px_im[x - 1, y]
#         if px_im[x,y] == (0,255,0,255):
#             print(x, y)
#             im.putpixel((x, y), (e[0], e[1], e[2]))
#
# for y in range(n_hy):
#     for x in range(n_wx):
#         if y - 1 < 0:  # บน
#             b = px_im[x, y]
#         else:
#             b = px_im[x, y - 1]
#         if px_im[x,y] == (0,255,0,255):
#             im.putpixel((x, y), (b[0], b[1], b[2]))
#
# for y in range(n_hy):
#     for x in range(n_wx):
#         if x - 1 < 0:  # ซ้าย
#             e = px_im[x, y]
#         else:
#             e = px_im[x - 1, y]
#         if px_im[x,y] == (0,0,1,255):
#             #print(x, y)
#             im.putpixel((x, y), (e[0], e[1], e[2]))

print('loading 100%')
px2=im.load()

image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
original_cv2 = cv2.imread(filename)
im.show()
im.save('test4'+'.png')
"""image = ImageTk.PhotoImage(im)
new_window = Toplevel(window)
panel1 = Label(new_window, image=image)
panel1.pack()"""
#cv2.imwrite(os.path.join(path,'test1.png'),image_cv2)
#cv2.waitKey(0)
# pic=ImageTk.PhotoImage(img)
# panel = Label(window, image=pic)
# panel.pack()

# window.mainloop()
