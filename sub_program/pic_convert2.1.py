from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk, ImageOps


# import tkinter as tk

def fix_point(i):
    ap = len(fix)
    for j in range(ap):
        if vec[i][ex:4] == fix[j][ex:4]:
            return True
    return False


filename = "first.tif"
img = ImageOps.flip(Image.open(filename))
wx, hy = img.size
px = img.load()
print(wx, ",", hy)

# b|c
# a|d
# variable of status
stt_spl = 2;  # start poly line
stt_cpl = 0;  # continue poly line
stt_epl = 1;  # end poly line
stt_sgl = 3;  # single line
stt_eos = 4;  # end of sharp
stt_fix = 6;  # fix point
vec = []
fix = []
for y in reversed(range(hy)):
    for x in range(wx):
        a = px[x, y]
        if y - 1 < 0:
            vec.append([x, y, x + 1, y, stt_cpl])  # bottom frame
            b = c = px[x, y]
        else:
            b = px[x, y - 1]
        if x + 1 == wx:
            vec.append([x + 1, y, x + 1, y + 1, stt_cpl])  # right frame
            d = c = px[x, y]
        else:
            d = px[x + 1, y]
        if (y > 0 and x + 1 != wx): c = px[x + 1, y - 1]
        if x == 0: vec.append([x, y, x, y + 1, stt_cpl])  # left frame
        if y + 1 == hy: vec.append([x, y + 1, x + 1, y + 1, stt_cpl])  # top frame

        # find to fix line
        stt = stt_cpl
        if (a != d):
            if (d != c):
                if (a != b):
                    stt = stt_fix
                else:
                    if (b != c): stt = stt_fix
            else:
                if (b != c):
                    if (a != b): stt = stt_fix
        else:
            if (a != b):
                if (b != c):
                    if (c != d):
                        stt = stt_fix
        if (stt == stt_fix): fix.append([x + 1, y])

        # line vactor
        if a != b: vec.append([x, y, x + 1, y, stt_cpl])  # [prev,sx,sy,ex,eyo,next,status]
        if a != d: vec.append([x + 1, y + 1, x + 1, y, stt_cpl])  # [prev,sx,sy,ex,eyo,next,status]

sx, sy, ex, ey, status = 0, 1, 2, 3, 4

print("link line...")
vec_len = len(vec)
print(vec_len)
vec[0][status] = stt_spl;  # start poly line
start = True
for i in range(vec_len):
    # first scan x
    # if i%100==0: print(i/vec_len,end='\r')
    if start == True:
        # find point for start combine link (revert)
        for ii in range(vec_len):
            m = ii
            for j in range(ii + 1, vec_len):
                if vec[ii][sx:2] == vec[j][ex:4]:
                    m = j
                    break
                else:
                    if vec[ii][sx:2] == vec[j][sx:2]:
                        # swap point
                        t = vec[j][sx:2]
                        vec[j][sx:2] = vec[j][ex:4]
                        vec[j][ex:4] = t
                        m = j
                        break
            if m > ii + 1:
                # swap line
                t = vec[ii + 1]
                vec[ii + 1] = vec[m]
                vec[m] = t
            else:
                if m == ii:  # end not found
                    # swap line
                    t = vec[i]
                    vec[i] = vec[m]
                    vec[m] = t
                    break
        start = False
    # loop combine link (forward)
    m = i
    for j in range(i + 1, vec_len):
        if vec[m][ex:4] == vec[j][sx:2]:
            m = j
            break
        else:
            if vec[m][ex:4] == vec[j][ex:4]:
                # swap point
                t = vec[j][sx:2]
                vec[j][sx:2] = vec[j][ex:4]
                vec[j][ex:4] = t
                m = j
                break
    if m > i + 1:
        # swap line
        t = vec[i + 1]
        vec[i + 1] = vec[m]
        vec[m] = t
    else:
        if m == i:  # end not found
            vec[i][status] = vec[i][status] + stt_epl  # end poly line or single line
            if i + 1 < vec_len: vec[i + 1][status] = stt_spl  # start poly line
            start = True
    if fix_point(i) and vec[i][status] == 0: vec[i][status] = 6

"""
f = open("vec.csv","w")
f.write("sx,sy,ex,ey,status"+"\r")
for i in vec:
    f.write(str(i[sx])+","+str(i[sy])+","+str(i[ex])+","+str(i[ey])+","+str(i[status])+"\r")
f.close()

f = open("fix.csv","w")
f.write("ex,ey"+"\r")
for i in fix:
    f.write(str(i[0])+","+str(i[1])+"\r")
f.close()
"""

f = open("vec.dxf", "w")
f.write("0\nSECTION\n2\nENTITIES\n")  # header

scale = 0.266
id = 218
for i in vec:
    f.write("0\nLINE\n5\n" + str(id) + "\n330\n1F\n100\nAcDbEntity\n8\nBoundry\n100\nAcDbLine\n")
    f.write("10\n" + str(i[sx] * scale) + "\n20\n" + str(i[sy] * scale) + "\n30\n0\n")
    f.write("11\n" + str(i[ex] * scale) + "\n21\n" + str(i[ey] * scale) + "\n31\n0\n")
    id += 1

f.write("0\nENDSEC\n0\nEOF\n")  # footer
f.close()

window = Tk()
window.title("Pattern Matching")
window.minsize(300, 100)

im = Image.new('RGBA', (1000, 1000), (0, 0, 0, 255))
draw = ImageDraw.Draw(im)
xshift = 10
yshift = 130
scale = 3
for i in vec:
    draw.line(
        ((i[sx] * scale) + xshift,
         (i[sy] * scale) + yshift,
         (i[ex] * scale) + xshift,
         (i[ey] * scale) + yshift
         ), fill=(0, 255, 0, 255))
image = ImageTk.PhotoImage(im)
new_window = Toplevel(window)
panel1 = Label(new_window, image=image)
panel1.pack()

draw = ImageDraw.Draw(img)
xshift = 0
yshift = 0
scale = 1
for i in vec:
    draw.line(
        ((i[sx] * scale) + xshift,
         (i[sy] * scale) + yshift,
         (i[ex] * scale) + xshift,
         (i[ey] * scale) + yshift
         ), fill=(0, 255, 0, 255))
pic = ImageTk.PhotoImage(img)
panel = Label(window, image=pic)
panel.pack()

window.mainloop()

"""
for i in pic:  
    if x%4==0: print("--")
    print(i,"-",x)
    x+=1
"""