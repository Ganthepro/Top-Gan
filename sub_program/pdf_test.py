from fpdf import FPDF
from PIL import Image,ImageDraw
import cv2


filename = "HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()

pdf = FPDF()
pdf.add_page()
sx,sy,ex,ey = 1,2,3,4
xshift=15
pic_xshift=0
yshift=0
pic_yshift=-1
scale=10
vec=[]
RGB=[]
bg_color = [0,0,1]
img_cv2 = cv2.imread(filename)
idx=-1
resize = img.resize((wx*scale,hy*scale))
n_wx, n_hy = resize.size
im = Image.new('RGBA', (wx*scale, hy*scale), (bg_color[0], bg_color[1], bg_color[2], 255))
colors=[]
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
        RGB.append([red, green, blue])
        im.putpixel((x * scale, y * scale), (red, green, blue))
px_im = im.load()
#print(vec)
im.show()
h_point = []
for i in vec:
    #print(vec)
    if i[ey] - 1 > 5:
        break
    pdf.line(i[sx],i[sy] - 1,i[ex],i[ey] - 1)
    pdf.set_draw_color(px_im[i[sx] * 10,(i[sy] - 1) * 10][0],px_im[i[sx] * 10,(i[sy] - 1) * 10][1],px_im[i[sx] * 10,(i[sy] - 1) * 10][2])
    #h_point.append()
    print(i[sx],i[sy] - 1,i[ex],i[ey] - 1)
    print(px_im[i[sx] * 10,(i[sy] - 1) * 10])
pdf.output("hello_world2.pdf")
exit()
for_len = 0
print(len(RGB))

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
        (   (i[sx]*scale)+pic_xshift*scale,
            (i[sy]*scale)+pic_yshift*scale,
            (i[ex]*scale)+pic_xshift*scale,
            (i[ey]*scale)+pic_yshift*scale
        ), fill=(0, 255, 0, 255))

print('loading 25%')

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x,y]
        colors.append(color)
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x,y] == (bg_color[0], bg_color[1], bg_color[2],255) and px_im[x,y] != b and b != (0, 255, 0, 255):
            im.putpixel((x, y), (b[0], b[1], b[2]))
print('loading 45%')
for y in reversed(range(n_hy)):
    for x in range(n_wx):
        if y+1 >= n_hy:#ล่าง
            f=px_im[x,y]
        else:
            f=px_im[x,y+1]
        if px_im[x,y] == (bg_color[0], bg_color[1], bg_color[2],255) and px_im[x,y] != f and f != (0, 255, 0, 255):
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
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (0, 255, 0, 255):
            im.putpixel((x, y), (e[0], e[1], e[2]))
print('loading 75%')
for y in range(n_hy):
    for x in reversed(range(n_wx)):
        if x+1==n_wx:#ขวา
            c=px_im[x,y]
        else:
            c=px_im[x+1,y]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (0, 255, 0, 255):
            im.putpixel((x, y), (c[0], c[1], c[2]))
print('loading 85%')
for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x,y] == (0,255,0,255):
            #print(x, y)
            im.putpixel((x, y), (e[0], e[1], e[2]))

for y in range(n_hy):
    for x in range(n_wx):
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x,y] == (0,255,0,255):
            im.putpixel((x, y), (b[0], b[1], b[2]))

for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x,y] == (0,0,1,255):
            #print(x, y)
            im.putpixel((x, y), (e[0], e[1], e[2]))

id1 = 0
start_p_1 = [0,0]
for y in range(n_hy):
    for x in range(1,n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] != [bg_color[0], bg_color[1], bg_color[2]]:
            if px_im[x, y] == e:
                id1 += 1
            elif px_im[x, y] != e:
                #print(id1)
                pdf.line(0 / 10, y/ 10, (0 + id1) / 10, y / 10)
                #print((start_p_1[0] + id1) / 10)
                pdf.set_line_width(0.2)
                pdf.set_draw_color(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                id1 = 0
                break

id = 0
line_vec = []
start_p = [0,0]
for y in range(n_hy):
    for x in range(n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x,y] != [bg_color[0],bg_color[1],bg_color[2]]:
            if px_im[x,y] == e:
                if start_p[0] + id > n_wx - 2:
                    continue
                else:
                    id += 1
            elif px_im[x,y] != e:
                #print('1.', start_p)
                #print('2.', id)
                pdf.line(start_p[0]/10, start_p[1]/10, (start_p[0]+id)/10, start_p[1]/10)
                pdf.set_line_width(0.23)
                pdf.set_draw_color(px_im[x,y][0], px_im[x,y][1], px_im[x,y][2])
                #print('3.',start_p[0]+id)
                id = 0
                start_p[0] = x
                start_p[1] = y
        #print(id)
        # pdf.line(x/10, y/10, (x+id)/10, y/10)
        # pdf.set_line_width(0.1)
        # pdf.set_draw_color(px_im[x,y][0], px_im[x,y][1], px_im[x,y][2])

print('loading 100%')

#im.show()
#pdf.set_fill_color(255,255,0)
#im.show('test.png')
pdf.output("hello_world2.pdf")
