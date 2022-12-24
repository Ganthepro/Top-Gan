from ssl import VERIFY_X509_PARTIAL_CHAIN
import numpy as np
from PIL import Image, ImageDraw
import cv2
import math

img = Image.open(r"G:\My Drive\Top_Gan Project\ตัวอย่างรูปภาพเพื่อใช้กับโปรแกรม\5.tif")
img = img.convert('RGBA')
wx, hy = img.size
px = img.load()
cv_img = np.array(img)
img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
# window = Tk()
# window.title("Pattern Matching")
xshift = 0
yshift = 0
#scale = int(scale_entry.get())
scale = 1
im = Image.new('RGBA', (wx * scale, hy * scale), (255, 255, 255, 255))
sx, sy, ex, ey = 1, 2, 3, 4
r, g, b = 2, 1, 0
resize_cv2 = cv2.resize(img_cv2, (wx * scale, hy * scale))
resize = img.resize((wx * scale, hy * scale))
n_wx, n_hy = resize.size
vec = []
RGB = []
colors = []
idx = -1
previous = 1

def shape_line(wx,hy,px,idx):
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


shape_line(wx,hy,px,idx)

# n_vec = []
# semi_vec = []
# for k,n in enumerate(vec):
#     for i in vec:
#         if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
#             # n_vec.append(n)/
#             # n_vec.append(i)\
#             semi_vec.append(n)
#             semi_vec.append(i)
#             n_vec.append([n[0],n[sx],n[sy],n[ex] - math.ceil(scale / 2),n[ey] + math.ceil(scale / 2)])
#             n_vec.append([i[0],i[sx] + math.ceil(scale / 2),i[sy]  + math.ceil(scale / 2),i[ex],i[ey]])  
#     print('loading ' + "{:.2f}".format(0 + ((k * 100) / len(vec))) + ' %')
#             # print(n,i)

# for i in vec:
#     if i in semi_vec:pass
#     else:n_vec.append(i)
    
# vec = n_vec

draw = ImageDraw.Draw(im)
for i in vec:
    draw.line(
        ((i[sx]) + xshift ,
         (i[sy]) + yshift,
         (i[ex]) + xshift,
         (i[ey]) + yshift
         ), fill=(0, 0, 1, 255))
cv_img = np.array(img)
image_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
im.show()
im.save('test' + '.png')