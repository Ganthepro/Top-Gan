from tkinter import *
from PIL import Image, ImageDraw
import cv2

filename = r"C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
window = Tk()
window.title("Pattern Matching")
xshift=0
yshift=-1
scale=1
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
print(len(vec))
n_vec = []
semi_vec = []
semi_vec = []
semi_vec = []
small_vec = []
sx,sy,ex,ey = 1,2,3,4
draw = ImageDraw.Draw(im)  
end_vec = ['','']
for i in vec:
    o_sx,o_sy = i[sx] - 1,i[sy]
    n_sx_r,n_sy_r = i[sx],i[sy]
    for n in vec:
        if (o_sx + 1 == n_sx_r and n_sx_r == n[sx]) and (o_sy == n_sy_r and n_sy_r == n[sy]) and n[sy] == n[ey]: #X เปลื่ยน Y เท่า
            o_sx += 1;
            n_sx_r += 1;
            #n_vec.append(n)
            #print(n)
            if len(semi_vec) == 0:semi_vec.append(n)
            elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] == semi_vec[len(semi_vec) - 1][ey] and n[sy] == semi_vec[len(semi_vec) - 1][sy]:
                #print(n , semi_vec[len(semi_vec) - 1]);
                semi_vec.append(n)
            else:
                if semi_vec[len(semi_vec) - 1][3] == end_vec[0] and semi_vec[len(semi_vec) - 1][4] == end_vec[1]:pass
                else:
                    n_vec.append([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                    end_vec[0] = semi_vec[len(semi_vec) - 1][3];end_vec[1] = semi_vec[len(semi_vec) - 1][4]
                #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                small_vec.clear();semi_vec.clear();semi_vec.append(n)
            #vec.remove(n)
#exit()
small_vec.clear();semi_vec.clear()
end_vec = []
for i in vec:
    o_sx,o_sy = i[sx],i[sy] - 1
    n_sx_d,n_sy_d = i[sx],i[sy]
    for n in vec:
        if (o_sx == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] == n[ex]: #X เท่า Y เปลื่ยน
            o_sy += 1;
            n_sy_d += 1;
            #vec.remove(n)
            #print(n)
            if len(semi_vec) == 0:semi_vec.append(n)
            elif n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1 and n[ex] == semi_vec[len(semi_vec) - 1][ex] and n[sx] == semi_vec[len(semi_vec) - 1][sx]:
                #print(n , semi_vec[len(semi_vec) - 1]);
                semi_vec.append(n)
            else:
                for v in end_vec:
                    if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:break
                else:
                    n_vec.append([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                    #print(semi_vec)
                    end_vec.append([semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4]])
                #print(semi_vec)
                #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                small_vec.clear();semi_vec.clear();semi_vec.append(n)
end_vec.clear()
semi_vec.clear()
for i in vec:
    o_sx,o_sy = i[sx] - 1,i[sy] - 1
    n_sx_d,n_sy_d = i[sx],i[sy]
    for n in vec: # แก้ต่อ
        if (o_sx + 1 == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] < n[ex] and n[sy] < n[ey]:
            o_sx += 1;o_sy += 1
            n_sx_d += 1;n_sy_d += 1
            #vec.remove(n)
            #print(n)
            if len(semi_vec) == 0:semi_vec.append(n)
            elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1:
                #print(n , semi_vec[len(semi_vec) - 1]);
                semi_vec.append(n)
            else:
                for v in end_vec:
                    if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:break
                else:
                    n_vec.append([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                    #print(semi_vec)
                    end_vec.append([semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4]])
                #print(semi_vec)
                #n_vec.append([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                small_vec.clear();semi_vec.clear();semi_vec.append(n)
semi_vec.clear()
small_vec.clear()
break_point = [0]
end_vec.clear()
draw = ImageDraw.Draw(im)
for i in n_vec:
    draw.line(
        (   (i[sx]*scale)*scale,
            (i[sy]*scale)*scale,
            (i[ex]*scale)*scale,
            (i[ey]*scale)*scale
        ), fill=(0, 255, 0, 255))
im.show()
exit()
for n in vec: # แก้ต่อ
    #if n[sx] == 82 and n[sy] == 34 and n[ex] == 83 and n[ey] == 33:print(n)
    if n[sx] < n[ex] and n[sy] > n[ey]:
        if len(semi_vec) == 0:semi_vec.append(n)
        elif len(semi_vec) > 0:
            while True:
                for e in vec:
                    if e[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and semi_vec[len(semi_vec) - 1][sy] - e[sy] == 1 and e[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and semi_vec[len(semi_vec) - 1][ey] - e[ey] == 1:
                        #print(e , semi_vec[len(semi_vec) - 1]);
                        semi_vec.append(e)
                        #print(break_point)
                        break_point[0] = 0
                        break
                    #print('break_point')
                    break_point[0] = 1
                if break_point[0] == 1:
                    break
                #elif break_point[0] == 0:print('else')
                #else:break
            #print(semi_vec)
            if len(semi_vec) == 1:end_vec.append(semi_vec[0]);#print(semi_vec[0])
            else:
                for v in end_vec: # แก้ต่อ
                    if v in semi_vec:
                        small_vec.append([semi_vec[0],v,len(semi_vec)])
                        #print([semi_vec[0],v])
            semi_vec.clear();semi_vec.append(n)
# for i in small_vec:
#     print(i)
# exit()
semi_vec.clear()
semi_vec1 = []
# for v in end_vec:
#     print(v)
#exit()
print(len(end_vec))
for v in end_vec:
    for i in small_vec:
        #print(v, i[1])
        if v == i[1]:
            semi_vec.append(i)
            #print(i)
    #print(semi_vec)
    if len(semi_vec) == 0:semi_vec1.append(v)
    else:n_vec.append([semi_vec[len(semi_vec) - 1][0][0],semi_vec[len(semi_vec) - 1][0][sx],semi_vec[len(semi_vec) - 1][0][sy],semi_vec[len(semi_vec) - 1][1][ex],semi_vec[len(semi_vec) - 1][1][ey],semi_vec[len(semi_vec) - 1][0][5],semi_vec[len(semi_vec) - 1][0][6]])
    semi_vec.clear()
print(len(semi_vec1))
# for j in end_vec:
#     for i in semi_vec1:
#         if i == j:
#             pass
#         else:semi_vec2.append(j);break
#print(len(semi_vec2))
for i in semi_vec1:
    n_vec.append(i)
print(len(vec))
draw = ImageDraw.Draw(im)
for i in n_vec:
    draw.line(
        (   (i[sx]*scale)*scale,
            (i[sy]*scale)*scale,
            (i[ex]*scale)*scale,
            (i[ey]*scale)*scale
        ), fill=(0, 255, 0, 255))
im.show()
                
    
    
