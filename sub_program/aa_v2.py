from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np

filename = "pic\HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=-1
scale=10
im = Image.new('RGBA', (wx*scale, hy*scale), (255, 255, 254, 255))
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize_cv2 = cv2.resize(img_cv2,(wx,hy))
resize = img.resize((wx,hy))
n_wx, n_hy = resize.size
vec=[]
RGB=[]
idx=-1
previous = 1
for y in range(hy):
    for x in range(wx):
        if y - 1 < 0:  # บน
            b = px[x, y]
        else:
            b = px[x, y - 1]
        if x + 1 == wx:  # ขวา
            c = px[x, y]
        else:
            c = px[x + 1, y]
        if y - 1 < 0:  # บน
            d = px[x, y]
        else:
            d = px[x, y - 1]
        if x - 1 < 0:  # ซ้าย
            e = px[x, y]
        else:
            e = px[x - 1, y]
        if y + 1 >= hy:  # ล่าง
            f = px[x, y]
        else:
            f = px[x, y + 1]
        if y + 1 == hy:
            g = px[x, y]
        elif x + 1 == wx:  # ล่างขวา
            g = px[x, y]
        else:
            g = px[x + 1, y + 1]
        if y + 1 == hy:
            h = px[x, y]
        elif x - 1 < 0:  # ล่างซ้าย
            h = px[x, y]
        else:
            h = px[x - 1, y + 1]
        if y - 1 < 0:
            j = px[x, y]
        elif x + 1 == wx:  # บนขวา
            j = px[x, y]
        else:
            j = px[x + 1, y - 1]
        if y - 1 < 0:
            k = px[x, y]
        elif x - 1 < 0:  # บนซ้าย
            k = px[x, y]
        else:
            k = px[x - 1, y - 1]
        # เปลื่ยนวิธีเช็กสีให้ถูก
        if px[x, y] != b and px[x, y] != c:
            idx += 1
            # [prev,sx,sy,ex,ey,next,status]
            vec.append([idx - 1, (x) * scale, (y) * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
        elif px[x, y] == e and px[x, y] != b:
            idx += 1
            # [prev,sx,sy,ex,ey,next,status]
            vec.append([idx - 1, x * scale, y * scale, (x + 1) * scale, y * scale, idx + 1, 0])
        elif px[x, y] == b:
            if px[x, y] != c:
                if px[x, y] == j:
                    pass
                else:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    # vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
        if px[x, y] != b and px[x, y] != e:
            idx += 1
            # [prev,sx,sy,ex,ey,next,status]
            vec.append([idx - 1, x * scale, (y + 1) * scale, (x + 1) * scale, y * scale, idx + 1, 0])
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
                idx += 1
                # [prev,sx,sy,ex,ey,next,status]
                # vec.append([idx - 1, x * scale, y * scale, x * scale, (y + 1) * scale, idx + 1, 0])
        elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
            if px[x, y] == j:
                pass
            else:
                idx += 1
                # [prev,sx,sy,ex,ey,next,status]
                # vec.append([idx - 1, (x + 1) * scale, y * scale,(x + 1) * scale, (y + 1) * scale, idx + 1, 0])
        elif px[x, y] == e and px[x, y] != f:
            idx += 1
            # [prev,sx,sy,ex,ey,next,status]
            vec.append([idx - 1, x * scale, y * scale, (x + 1) * scale, y * scale, idx + 1, 0])
                
px_im = im.load()
draw = ImageDraw.Draw(im)

for i in vec:
    draw.line(
        ((i[sx]),
         (i[sy]),
         (i[ex]),
         (i[ey])
         ), fill=(0, 255, 0, 255))

# image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
# original_cv2 = cv2.imread(filename)
im.show('test.png')
"""image = ImageTk.PhotoImage(im)
new_window = Toplevel(window)
panel1 = Label(new_window, image=image)
panel1.pack()"""
# cv2.imwrite('test.png',image_cv2)

# pic=ImageTk.PhotoImage(img)
# panel = Label(window, image=pic)
# panel.pack()

#window.mainloop()
