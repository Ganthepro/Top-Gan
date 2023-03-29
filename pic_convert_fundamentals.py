from tkinter import *
from PIL import Image, ImageDraw, ImageTk

def xy(x1, y1):
    return x1 + (y1 * my)

pic = [1, 0, 0, 0, 1,
       0, 0, 0, 0, 0,
       0, 0, 1, 0, 0,
       0, 0, 0, 0, 0,
       1, 0, 0, 0, 1]

mx, my = 5, 5
vec = []
idx = -1
x, y = 0, 0
for y in range(my):
    for x in range(mx):
        if y-1 < 0:  # บน
            b = pic[xy(x, y)]
        else:
            b = pic[xy(x, y-1)]
        if x+1 == mx:  # ซ้าย
            c = pic[xy(x, y)]
        else:
            c = pic[xy(x+1, y)]
        if pic[xy(x, y)] != b:
            idx += 1
            vec.append([idx-1, x, y, x+1, y, idx+1, 0]) # [prev,sx,sy,ex,ey,next,status]
        if pic[xy(x, y)] != c:
            idx += 1
            vec.append([idx-1, x+1, y, x+1, y+1, idx+1, 0]) # [prev,sx,sy,ex,ey,next,status]

sx, sy, ex, ey = 1, 2, 3, 4

window = Tk()
window.title("Fundamentals")
xshift = 0
yshift = 0
scale = 100
im = Image.new('RGBA', (mx*scale, my*scale), (0, 0, 0, 255))
draw = ImageDraw.Draw(im)
for i in vec:
    print(i)
    draw.line(
        ((i[sx]*scale)+xshift,
            (i[sy]*scale)+yshift,
            (i[ex]*scale)+xshift,
            (i[ey]*scale)+yshift
         ), fill=(255, 0, 0, 255))
image = ImageTk.PhotoImage(im)
panel = Label(window, image=image)
panel.image = image
panel.pack()

window.mainloop()