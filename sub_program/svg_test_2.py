import svgwrite as svg
from PIL import Image, ImageDraw
import cv2
import numpy as np

dwg = svg.Drawing('test_svg.svg', profile='tiny')
filename = r"C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
xshift=0
yshift=-1
scale=3
im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 1, 255))
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize_cv2 = cv2.resize(img_cv2,(wx*scale,hy*scale))
resize = img.resize((wx*scale,hy*scale))
n_wx, n_hy = resize.size
vec=[]
RGB=[]
colors=[]
idx=-1
bg_color = [0,0,1]
previous = 1

for y in range(hy):
    for x in range(wx):
        blue = img_cv2[y, x, 0]
        green = img_cv2[y, x, 1]
        red = img_cv2[y, x, 2]
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
        RGB.append([red, green, blue])
        im.putpixel((x * scale, y * scale), (red, green, blue))
        #dwg.add(dwg.rect((x * scale,y * scale),(0.05,0.05),stroke=svg.rgb(red,green,blue,'RGB')))

px_im = im.load()
draw = ImageDraw.Draw(im)
print(len(colors))

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x,y]
        colors.append(color)
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x,y] == (0, 0, 1,255) and px_im[x,y] != e:
            im.putpixel((x,y), (e[0],e[1],e[2]))

for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift*scale,
            (i[sy]*scale)+yshift*scale,
            (i[ex]*scale)+xshift*scale,
            (i[ey]*scale)+yshift*scale
        ), fill=(0, 255, 0, 255))

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x,y]
        colors.append(color)
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x,y] == (0, 0, 1,255) and px_im[x,y] != b and b != (0, 255, 0, 255):
            im.putpixel((x, y), (b[0], b[1], b[2]))

for y in reversed(range(n_hy)):
    for x in range(n_wx):
        if y+1 >= n_hy:#ล่าง
            f=px_im[x,y]
        else:
            f=px_im[x,y+1]
        if px_im[x,y] == (0, 0, 1,255) and px_im[x,y] != f and f != (0, 255, 0, 255):
            im.putpixel((x, y), (f[0], f[1], f[2]))

for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != e and e != (0, 255, 0, 255):
            im.putpixel((x, y), (e[0], e[1], e[2]))

for y in range(n_hy):
    for x in reversed(range(n_wx)):
        if x+1==n_wx:#ขวา
            c=px_im[x,y]
        else:
            c=px_im[x+1,y]
        if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != c and c != (0, 255, 0, 255):
            im.putpixel((x, y), (c[0], c[1], c[2]))
print(len(vec))
for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] == (0, 255, 0, 255):
            # print(x, y)
            im.putpixel((x, y), (e[0], e[1], e[2]))

for y in range(n_hy):
    for x in range(n_wx):
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x, y] == (0, 255, 0, 255):
            im.putpixel((x, y), (b[0], b[1], b[2]))

for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] == (0, 0, 1, 255):
            # print(x, y)
            im.putpixel((x, y), (e[0], e[1], e[2]))
# im.show()
# exit()
# count_1 = 0
# for i in vec:
#     #print(((i[sx] * scale) + xshift, (i[sy] * scale) + (yshift - 2)), ((i[ex] * scale) + xshift, (i[ey] * scale) + (yshift - 2)))
#     dwg.add(dwg.line(((i[sx] * scale) + xshift, (i[sy] * scale) + (yshift - 2)), ((i[ex] * scale) + xshift, (i[ey] * scale) + (yshift - 2)),stroke=svg.rgb(0, 255, 0, 'RGB')))
#     count_1 += 1
# print('count_1 ',count_1)

id1 = 0
start_p_1 = [0, 0]
for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] != [bg_color[0], bg_color[1], bg_color[2]]:
            if px_im[x, y] == e:
                id1 += 1
            elif px_im[x, y] != e:
                #print(id1)
                #print((0, y), ((0 + id1), y))
                dwg.add(dwg.line((0, y), ((0 + id1), y),stroke=svg.rgb(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2], 'RGB'),stroke_width=2))
                # pdf.line(0 / 10, y / 10, (0 + id1) / 10, y / 10)
                # # print((start_p_1[0] + id1) / 10)
                # pdf.set_line_width(0.2)
                # pdf.set_draw_color(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                id1 = 0
                break

id = 1
line_vec = []
start_p = [0, 0]
for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] != [bg_color[0], bg_color[1], bg_color[2]]:
            if px_im[x, y] == e:
                if start_p[0] + id > n_wx:
                    continue
                else:
                    id += 1
                #print(id)
            elif px_im[x, y] != e:
                #print('1.', start_p)
                #print('2.', id)
                #print((start_p[0], start_p[1]), ((start_p[0] + id), start_p[1]))
                dwg.add(dwg.line((start_p[0], start_p[1]), ((start_p[0] + id), start_p[1]),stroke=svg.rgb(px_im[start_p[0], start_p[1]][0], px_im[start_p[0], start_p[1]][1], px_im[start_p[0], start_p[1]][2], 'RGB'),stroke_width=2))
                 # pdf.line(start_p[0] / 10, start_p[1] / 10, (start_p[0] + id) / 10, start_p[1] / 10)
                 # pdf.set_line_width(0.23)
                 # pdf.set_draw_color(px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                #print('3.',start_p[0]+id)
                #print('4.',px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                id = 1
                start_p[0] = x
                start_p[1] = y
count_1 = 0
for y in range(0,n_hy,scale):
    for x in range(0,n_wx,scale):
        for i in vec:
            if x == (i[ex] * scale) + xshift and y == (i[ey] - 1) * scale:
                # print((((i[sx] * scale) + xshift, (i[sy] * scale))), ((i[ex] * scale) + xshift, (i[ey] * scale)))
                dwg.add(dwg.line(((i[sx] * scale) + 1 + xshift, (i[sy] - 1) * scale), ((i[ex] * scale) + 1 + xshift, (i[ey] - 1) * scale),
                                 stroke=svg.rgb(px_im[(i[ex] * scale) + xshift, i[ey] * scale - 1][0], px_im[(i[ex] * scale) + xshift, i[ey] * scale - 1][1], px_im[(i[ex] * scale) + xshift,  i[ey] * scale - 1][2], 'RGB')))
                count_1 += 1
# print('count_1 ',count_1)


image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
original_cv2 = cv2.imread(filename)
cv2.imwrite('test.png',image_cv2)
dwg.save()