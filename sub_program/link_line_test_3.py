from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
import random

filename = r"C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=-1
scale=3
im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 0, 255))
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
        # if y - 1 < 0:
        #     b = px[x, y]
        # else:
        #     b = px[x, y - 1]
        # if x + 1 == wx:
        #     c = px[x, y]
        # else:
        #     c = px[x + 1, y]
        # if px[x, y] != b:
        #     idx += 1;
        #     vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
        # if px[x, y] != c:
        #     idx += 1;
        #     vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]

px_im = im.load()
draw = ImageDraw.Draw(im)
for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift*scale,
            (i[sy]*scale)+yshift*scale,
            (i[ex]*scale)+xshift*scale,
            (i[ey]*scale)+yshift*scale
        ), fill=(0, 255, 0, 255))
image_im_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
cv2.imwrite('test.png',image_im_cv2)
start_p = []
stop_p = []
line_vec = []
px2=im.load()
link_im = Image.new('RGBA',(n_wx,n_hy),(255,255,255,255))
px_link_im = link_im.load()
point = ['','']
origin_point = ['','']
start = ['','']
R_ran_list = []
G_ran_list = []
B_ran_list = []
ran_round = 0
for hy in range(n_hy):
    for wx in range(n_wx):
        ran = random.sample(range(255), 3)
        if px_im[wx,hy] == (0,255,0,255) and px_link_im[wx,hy] == (255,255,255,255):
            link_im.putpixel((wx, hy), (ran[0], ran[1], ran[2], 255))
            start_p.append([wx, hy])
            #print(start_p)
            point[0] = wx
            start[0] = wx
            point[1] = hy
            start[1] = hy
            round_1 = 0
            round_2 = 0
            point_c = []
            #print(start)
            #print(len(start_p))
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
                if round_1 > 1 or round_2 >= 1:
                    #print('round',round_1)
                    break
                positions = [[top, (x,y - 1), top_link], [right, (x + 1, y), right_link], [bottom, (x,y + 1), bottom_link],
                             [left, (x - 1, y), left_link], [bottom_right, (x + 1,y + 1), bottom_right_link],
                             [bottom_left, (x - 1,y + 1), bottom_left_link],[top_right, (x + 1,y - 1), top_right_link],
                            [top_left, (x - 1,y - 1), top_left_link]]
                n_positions = []
                if px_link_im[x, y] != (255, 255, 255, 255):
                    directions = 0
                    for position in positions:
                        if position[0] == (0, 255, 0, 255):
                            if position[2] == px_link_im[x, y]:
                                continue
                            else:
                                directions += 1
                                #print(directions)
                                if directions > 1:
                                    #print(directions)
                                    #print('no')
                                    directions = 0
                                    #print('yes')
                                    break
                                else:
                                    n_directions = 0
                                    origin_point[0] = point[0]
                                    origin_point[1] = point[1]
                                    #print('old ',origin_point)
                                    if position[1][0] > point[0]:
                                        point[0] += 1
                                    if position[1][0] < point[0]:
                                        point[0] -= 1
                                    if position[1][1] > point[1]:
                                        point[1] += 1
                                    if position[1][1] < point[1]:
                                        point[1] -= 1
                                    n_x = point[0];n_y = point[1]
                                    if n_y - 1 < 0:  # บน
                                        top = px_im[n_x, y]
                                        top_link = px_link_im[n_x, n_y]
                                    else:
                                        top = px_im[n_x, n_y - 1]
                                        top_link = px_link_im[n_x, n_y - 1]
                                    if n_x + 1 == n_wx:  # ขวา
                                        right = px_im[n_x, n_y]
                                        right_link = px_link_im[n_x, n_y]
                                    else:
                                        right = px_im[n_x + 1, n_y]
                                        right_link = px_link_im[n_x + 1, n_y]
                                    if n_x - 1 < 0:  # ซ้าย
                                        left = px_im[n_x, n_y]
                                        left_link = px_link_im[n_x, n_y]
                                    else:
                                        left = px_im[n_x - 1, n_y]
                                        left_link = px_link_im[n_x - 1, n_y]
                                    if n_y + 1 >= n_hy:  # ล่าง
                                        bottom = px_im[n_x, n_y]
                                        bottom_link = px_link_im[n_x, n_y]
                                    else:
                                        bottom = px_im[n_x, n_y + 1]
                                        bottom_link = px_link_im[n_x, n_y + 1]
                                    if n_y + 1 == n_hy:
                                        bottom_right = px_im[n_x, n_y]
                                        bottom_right_link = px_link_im[n_x, n_y]
                                    elif n_x + 1 == n_wx:  # ล่างขวา
                                        bottom_right = px_im[n_x, n_y]
                                        bottom_right_link = px_link_im[n_x, n_y]
                                    else:
                                        bottom_right = px_im[n_x + 1, n_y + 1]
                                        bottom_right_link = px_link_im[n_x + 1, n_y + 1]
                                    if n_y + 1 == n_hy:
                                        bottom_left = px_im[n_x, n_y]
                                        bottom_left_link = px_link_im[n_x, n_y]
                                    elif n_x - 1 < 0:  # ล่างซ้าย
                                        bottom_left = px_im[n_x, n_y]
                                        bottom_left_link = px_link_im[n_x, n_y]
                                    else:
                                        bottom_left = px_im[n_x - 1, n_y + 1]
                                        bottom_left_link = px_link_im[n_x - 1, n_y + 1]
                                    if n_y - 1 < 0:
                                        top_right = px_im[n_x, n_y]
                                        top_right_link = px_link_im[n_x, n_y]
                                    elif n_x + 1 == n_wx:  # บนขวา
                                        top_right = px_im[n_x, y]
                                        top_right_link = px_link_im[n_x, n_y]
                                    else:
                                        top_right = px_im[n_x + 1, n_y - 1]
                                        top_right_link = px_link_im[n_x + 1, n_y - 1]
                                    if y - 1 < 0:
                                        top_left = px_im[n_x, n_y]
                                        top_left_link = px_link_im[n_x, n_y]
                                    elif n_x - 1 < 0:  # บนซ้าย
                                        top_left = px_im[n_x, n_y]
                                        top_left_link = px_link_im[n_x, n_y]
                                    else:
                                        top_left = px_im[n_x - 1, n_y - 1]
                                        top_left_link = px_link_im[n_x - 1, n_y - 1]
                                    p_positions = [[top, (n_x, n_y - 1), top_link], [right, (n_x + 1, n_y), right_link],
                                                 [bottom, (n_x, n_y + 1), bottom_link],
                                                 [left, (n_x - 1, n_y), left_link],
                                                 [bottom_right, (n_x + 1, n_y + 1), bottom_right_link],
                                                 [bottom_left, (n_x - 1, n_y + 1), bottom_left_link],
                                                 [top_right, (n_x + 1, n_y - 1), top_right_link],
                                                 [top_left, (n_x - 1, n_y - 1), top_left_link]]
                                    p_direction = 0
                                    for p_position in p_positions:
                                        if p_position[2] == px_link_im[x, y]:
                                            continue
                                        elif p_position[0] == (0,255,0,255) and p_position[2] == (255,255,255,255):
                                            p_direction += 1
                                    if p_direction > 1 and y > 2:
                                        link_im.putpixel(position[1], (0,0,0,255))
                                        #print(point);#link_im.show('test_link.png')
                                        round_2 += 1;print(p_direction);break
                                    else:
                                        link_im.putpixel(position[1], px_link_im[x, y])
                                        if (point[0] == 284 and point[1] == 864):
                                            #round_1 += 1
                                            #im.show()
                                            link_im.show('test_link.png')
                                            #pass
                                        if point[0] == 0 or point[1] == 0 or point[0] == n_wx + (yshift) or point[1] == n_hy - scale:
                                            #print('point 1 ',point)
                                            round_1 += 1
                                            #print(point)
                                            #link_im.show('test_link.png')
                                        elif (point[0] + 1 == start[0] or point[0] - 1 == start[0]) and (point[1] + 1 == start[1] or point[1] - 1 == start[1]):
                                            #print('point 2 ',point)
                                            round_1 += 1
                                            #link_im.show('test_link.png')
                                        elif (point[0] + 1 == start[0] or point[0] - 1 == start[0]) and (point[1] == start[1]):
                                            #print('point 2 ',point)
                                            round_1 += 1
                                            #link_im.show('test_link.png')
                                        elif (point[1] + 1 == start[1] or point[1] - 1 == start[1]) and (point[0] == start[0]):
                                            #print('point 2 ',point)
                                            round_1 += 1
                                            #link_im.show('test_link.png')
                                        else:
                                            """Nexus Event!!!"""
                                            for n_position in positions:
                                                if n_position[0] == (0, 255, 0, 255):
                                                    n_x = point[0]
                                                    n_y = point[1]
                                                    if n_position[2] == px_link_im[n_x, n_y]:
                                                        continue
                                                    elif n_position[1] != (n_x,n_y):
                                                        n_directions += 1
                                                        if n_directions == 2:
                                                            round_2 += 1
                                                            #link_im.show('test_link.png')
                                                            break
                                    print(point)
                                    #print('start',start)
R_ran_list = []
G_ran_list = []
B_ran_list = []
ran_round = 0

for wx in range(n_wx):
    hy = n_hy - scale
    R_ran = random.randrange(0, 255, 1)
    G_ran = random.randrange(0, 255, 1)
    B_ran = random.randrange(0, 255, 1)
    # hy = 0
    if px_im[wx, hy] == (0, 255, 0, 255):
        link_im.putpixel((wx, hy), (R_ran, G_ran, B_ran, 255))
        start_p.append([wx, hy])
        # print(start_p)
        point[0] = wx
        start[0] = wx
        point[1] = hy
        start[1] = hy
        round_1 = 0
        round_2 = 0
        point_c = []
        # print(start)
        # print(len(start_p))
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
            if round_1 > 1 or round_2 == 1:
                # print('round',round_1)
                break
            positions = [[top, (x, y - 1), top_link], [right, (x + 1, y), right_link],
                         [bottom, (x, y + 1), bottom_link],
                         [left, (x - 1, y), left_link], [bottom_right, (x + 1, y + 1), bottom_right_link],
                         [bottom_left, (x - 1, y + 1), bottom_left_link], [top_right, (x + 1, y - 1), top_right_link],
                         [top_left, (x - 1, y - 1), top_left_link]]
            n_position = []
            if px_link_im[x, y] != (255, 255, 255, 255):
                directions = 0
                for position in positions:
                    if position[0] == (0, 255, 0, 255):
                        if position[2] == px_link_im[x, y]:
                            continue
                        else:
                            directions += 1
                            # print(directions)
                            if directions > 1:
                                # print(directions)
                                # print('no')
                                directions = 0
                                # print('yes')
                                break
                            else:
                                link_im.putpixel(position[1], px_link_im[x, y])
                                if position[1][0] > point[0]:
                                    point[0] += 1
                                if position[1][0] < point[0]:
                                    point[0] -= 1
                                if position[1][1] > point[1]:
                                    point[1] += 1
                                if position[1][1] < point[1]:
                                    point[1] -= 1
                                if (point[0] == 1274 and point[1] == 626):
                                    pass
                                    # round_1 += 1
                                    # link_im.show('test_link.png')
                                if point[0] == 1 or point[1] == 1 or point[0] == n_wx + (yshift) or point[
                                    1] == n_hy - scale:
                                    # print('point 1 ',point)
                                    round_1 += 1
                                    # link_im.show('test_link.png')
                                elif (point[0] + 4 == start[0] or point[0] - 4 == start[0]) and (
                                        point[1] + 6 == start[1] or point[1] - 6 == start[1]):
                                    # print('point 2 ',point)
                                    round_1 += 1
                                elif (point[0] + 1 == start[0] or point[0] - 1 == start[0]) and (
                                        point[1] + 1 == start[1] or point[1] - 1 == start[1]):
                                    # print('point 2 ',point)
                                    round_1 += 1
                                elif (point[0] + 1 == start[0] or point[0] - 1 == start[0]) and (point[1] == start[1]):
                                    # print('point 2 ',point)
                                    round_1 += 1
                                    # link_im.show('test_link.png')
                                # print(point)
                                # print('start',start)

#1274, 626
# for x in range(n_wx):
#     for y in range(n_hy):
#          pass

image_cv2 = cv2.cvtColor(np.array(link_im),cv2.COLOR_RGB2BGR)
original_cv2 = cv2.imread(filename)
link_im.show('test_link.png')
cv2.imwrite('test_link.png',image_cv2)

# pic=ImageTk.PhotoImage(img)
# panel = Label(window, image=pic)
# panel.pack()

#window.mainloop()
