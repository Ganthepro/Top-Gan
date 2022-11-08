from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np

filename = "HT19-C00514-NHU036814-2SAM_CARVE.tif"
img = Image.open(filename)
#pic = ImageTk.PhotoImage(im)
wx, hy = img.size
px = img.load()
print(wx,",",hy)

vec=[]
idx=-1
for y in reversed(range(hy)):
    for x in range(wx):
        if y-1<0: b=px[x,y]
        else: b=px[x,y-1]
        if x+1==wx: c=px[x,y]
        else: c=px[x+1,y]
        if px[x,y]!=b:
            idx+=1; vec.append([idx-1,x,y,x+1,y,idx+1,0]) #[prev,sx,sy,ex,eyo,next,status]
        if px[x,y]!=c:
            idx+=1; vec.append([idx-1,x+1,y,x+1,y+1,idx+1,0]) #[prev,sx,sy,ex,eyo,next,status]


sx,sy,ex,ey = 1,2,3,4


f = open("../myproject/vec.csv", "w")
for i in vec:
    #print(idx,i[sx],i[sy],i[ex],i[ey])
    f.write(str(idx)+","+str(i[sx])+","+str(i[sy])+","+str(i[ex])+","+str(i[ey])+"\r")
    idx+=1
f.close()


window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=0
scale=3
im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 0, 255))
draw = ImageDraw.Draw(im)
print(vec)
for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift,
            (i[sy]*scale)+yshift,
            (i[ex]*scale)+xshift,
            (i[ey]*scale)+yshift
        ), fill=(255, 0, 0, 255))

image_cv2 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
# im.show('test.png')
"""
image = ImageTk.PhotoImage(im)
new_window = Toplevel(window)
panel1 = Label(new_window, image=image)
panel1.pack()
cv2.imwrite('test.png',image_cv2)
"""

pic=ImageTk.PhotoImage(img)
panel = Label(window, image=pic)
panel.pack()

window.mainloop()

"""
for i in pic:  
    if x%4==0: print("--")
    print(i,"-",x)
    x+=1
"""
