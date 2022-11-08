from fpdf import FPDF
from PIL import Image, ImageDraw
import cv2
filename = r"C:\Users\gan_z\Desktop\My-Project\pythonProject\pic\HT19-C00514-NHU036814-2SAM_CARVE.tif"  # HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
pdf = FPDF()
pdf.add_page('L')
sx, sy, ex, ey = 1, 2, 3, 4
xshift = 15
pic_xshift = 0
yshift = 0
pic_yshift = -1
scale = 4
vec = []
RGB = []
bg_color = [0, 0, 1]
img_cv2 = cv2.imread(filename)
idx = -1
resize = img.resize((wx * scale, hy * scale))
n_wx, n_hy = resize.size
im = Image.new('RGBA', (wx * scale, hy * scale), (bg_color[0], bg_color[1], bg_color[2], 255))
colors = []
previous = 1
for y in range(hy):
    for x in range(wx):
        blue = img_cv2[y, x, 0]
        green = img_cv2[y, x, 1]
        red = img_cv2[y, x, 2]
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
        RGB.append([red, green, blue])
        im.putpixel((x * scale, y * scale), (red, green, blue))
px_im = im.load()
for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x, y]
        colors.append(color)
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e:
            im.putpixel((x, y), (e[0], e[1], e[2]))

# print(RGB)
draw = ImageDraw.Draw(im)

for i in vec:
    draw.line(
        ((i[sx] * scale) + pic_xshift * scale,
         (i[sy] * scale) + pic_yshift * scale,
         (i[ex] * scale) + pic_xshift * scale,
         (i[ey] * scale) + pic_yshift * scale
         ), fill=(0, 255, 0, 255))

print('loading 25%')

for y in range(n_hy):
    for x in range(n_wx):
        color = px_im[x, y]
        colors.append(color)
        if y - 1 < 0:  # บน
            b = px_im[x, y]
        else:
            b = px_im[x, y - 1]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (0, 255, 0, 255):
            im.putpixel((x, y), (b[0], b[1], b[2]))
print('loading 45%')
for y in reversed(range(n_hy)):
    for x in range(n_wx):
        if y + 1 >= n_hy:  # ล่าง
            f = px_im[x, y]
        else:
            f = px_im[x, y + 1]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (0, 255, 0, 255):
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
        if x + 1 == n_wx:  # ขวา
            c = px_im[x, y]
        else:
            c = px_im[x + 1, y]
        if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (0, 255, 0, 255):
            im.putpixel((x, y), (c[0], c[1], c[2]))
print('loading 85%')
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

id1 = 0
for y in range(n_hy):
    for x in range(1, n_wx):
        if x - 1 < 0:  # ซ้าย
            e = px_im[x, y]
        else:
            e = px_im[x - 1, y]
        if px_im[x, y] != [bg_color[0], bg_color[1], bg_color[2]]:
            if px_im[x, y] == e:
                id1 += 1
            elif px_im[x, y] != e:
                #print(id1)
                pdf.line(0 / 10, y / 10, (0 + id1) / 10, y / 10)
                # pdf.line(0 / 10, y, (0 + id1), y)
                # print((start_p_1[0] + id1) / 10)
                pdf.set_line_width(0.2)
                pdf.set_draw_color(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                id1 = 0
                break
print(wx, hy);print(n_wx,n_hy)
id = 0
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
            elif px_im[x, y] != e:
                # print('1.', start_p)
                # print('2.', id)
                pdf.line(start_p[0] / 10, start_p[1] / 10, (start_p[0] + id) / 10, start_p[1] / 10)
                # pdf.line(start_p[0], start_p[1], (start_p[0] + id), start_p[1])
                pdf.set_line_width(0.23)
                pdf.set_draw_color(px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                # print('3.',start_p[0]+id)
                id = 0
                start_p[0] = x
                start_p[1] = y

for i in vec:
    pdf.line((i[sx] * scale) / 10, ((i[sy] - 1) * scale) / 10, (i[ex] * scale) / 10, ((i[ey] - 1) * scale) / 10)
    pdf.set_draw_color(0,255,0)

print('loading 100%')
# im.show()
pdf.output("test.pdf")
