import os
from tkinter import N, W
from PIL import Image, ImageDraw
import cv2

filename = r"C:\Users\gan_z\Desktop\My-Project\Ganthepro\project\pic\HT19-C00514-NHU036814-2SAM_CARVE.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif #H20-C00175-11S190500-04-sample.tif
img = Image.open(filename)
wx, hy = img.size
print(img.size)
px = img.load()
img_cv2 = cv2.imread(filename)
xshift=0
yshift=-1
scale=2
im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 1, 255))
bg_color = [0,0,1]
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize = img.resize((wx*scale,hy*scale))
n_wx, n_hy = resize.size
path = 'Desktop'
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
        elif px[x, y] != e and px[x, y] == b:
            if px[x, y] == k:
                pass
            else:
                idx += 1;
                vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0]) # [prev,sx,sy,ex,ey,next,status]
        elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
            if px[x, y] == j:
                pass
            else:
                idx += 1;
                vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0]) # [prev,sx,sy,ex,ey,next,status]
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
print('loading 25%')
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
print('loading 50%')
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
for n in vec:
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
print('loading 75%')
# for i in small_vec:
#     print(i)
# exit()
semi_vec.clear()
semi_vec1 = []
# for v in end_vec:
#     print(v)
#exit()
#print(len(end_vec))
for v in end_vec:
    for i in small_vec:
        #print(v, i[1])
        if v == i[1]:
            semi_vec.append(i)
    #print(semi_vec)
    if len(semi_vec) == 0:semi_vec1.append(v)
    else:
        #print([semi_vec[len(semi_vec) - 1][0][0],semi_vec[len(semi_vec) - 1][0][sx],semi_vec[len(semi_vec) - 1][0][sy],semi_vec[len(semi_vec) - 1][1][ex],semi_vec[len(semi_vec) - 1][1][ey],semi_vec[len(semi_vec) - 1][0][5],semi_vec[len(semi_vec) - 1][0][6]])
        n_vec.append([semi_vec[len(semi_vec) - 1][0][0],semi_vec[len(semi_vec) - 1][0][sx],semi_vec[len(semi_vec) - 1][0][sy],semi_vec[len(semi_vec) - 1][1][ex],semi_vec[len(semi_vec) - 1][1][ey],semi_vec[len(semi_vec) - 1][0][5],semi_vec[len(semi_vec) - 1][0][6]])
    semi_vec.clear()
#print(len(semi_vec1))
for i in semi_vec1:
    n_vec.append(i)
#exit()
width = [7] #wall thickness
wid = i
semi_vec.clear()
print(len(n_vec))
semi_vec1.clear()
if width[0] > 1:
    num_minus = [0,0] 
    num_plus = [0,0]
    for v in range(width[0]):
        if v % 2 == 0:
            num_plus[0] += 1;num_plus[1] += 0.2
            for k,i in enumerate(n_vec):
                if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                    semi_vec.append([k,(i[sx]*scale)*scale+num_plus[0],(i[sy]*scale)*scale,(i[ex]*scale)*scale+num_plus[0],(i[ey]*scale)*scale])
                    semi_vec1.append([k,i[sx]+num_plus[1],i[sy],i[ex]+num_plus[1],i[ey]])
                elif (i[sx] != i[ex] and i[sy] == i[ey]):
                    semi_vec.append([k,(i[sx]*scale)*scale,(i[sy]*scale)*scale+num_plus[0],(i[ex]*scale)*scale,(i[ey]*scale)*scale+num_plus[0]])
                    semi_vec1.append([k,i[sx],i[sy]-num_plus[1],i[ex],i[ey]-num_plus[1]])
        else:
            num_minus[0] -= 1;num_minus[1] -= 0.2
            for k,i in enumerate(n_vec):
                if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                    semi_vec.append([k,(i[sx]*scale)*scale+num_minus[0],(i[sy]*scale)*scale,(i[ex]*scale)*scale+num_minus[0],(i[ey]*scale)*scale])
                    semi_vec1.append([k,i[sx]+num_minus[1],i[sy],i[ex]+num_minus[1],i[ey]])
                elif (i[sx] != i[ex] and i[sy] == i[ey]):
                    semi_vec.append([k,(i[sx]*scale)*scale,(i[sy]*scale)*scale+num_minus[0],(i[ex]*scale)*scale,(i[ey]*scale)*scale+num_minus[0]])
                    semi_vec1.append([k,i[sx],i[sy]-num_minus[1],i[ex],i[ey]-num_minus[1]])
print(len(n_vec))
draw = ImageDraw.Draw(im)
for k,i in enumerate(n_vec):
    #print(k)
    draw.line(
            (   (i[sx]*scale)*scale,
                (i[sy]*scale)*scale,
                (i[ex]*scale)*scale,
                (i[ey]*scale)*scale
            ), fill=(0, 255, 0, 255))
for k,i in enumerate(semi_vec):
    #n_vec.append(i)
    draw.line(
            (   (i[sx]),#*scale)*scale,
                (i[sy]),#*scale)*scale,
                (i[ex]),#*scale)*scale,
                (i[ey])#*scale)*scale
            ), fill=(0, 255, 0, 255))
for i in semi_vec1:n_vec.append(i)
im.show() 
print('loading 100%')     
eshift = [0.03320]
scale = 1 #scale
print(wx*scale, hy*scale)
with open('test.gcode', 'w') as f:
    f.write('M140 S60\n')
    f.write('M105\n')
    f.write('M190 S60\n')
    f.write('M104 S200\n')
    f.write('M105\n')
    f.write('M109 S200\n')
    f.write('M82\n')
    f.write('M201 X500.00 Y500.00 Z100.00 E5000.00\n')
    f.write('M203 X500.00 Y500.00 Z10.00 E50.00\n')
    f.write('M204 P500.00 R1000.00 T500.00\n')
    f.write('M205 X8.00 Y8.00 Z0.20 E5.00\n')
    f.write('M220 S100\n')
    f.write('M221 S100\n')
    f.write('G28\n')
    f.write('G92 E0\n')
    f.write('G1 Z2.0\n')
    rect_num = [1,2,3,4]
    corner = [[wx*scale + 30,hy*scale + 30],[30,hy*scale + 30],[30,30],[wx*scale + 30,30]]
    z = [0.28]
    for i in range(3): #แก้การลากฐานให้เป็นจากบนลงล่าง
        while corner[0][0] - corner[1][0] > 0 and corner[3][0] - corner[2][0] > 0:
            f.write('G1 X'+str(corner[0][0])+' Y'+str(corner[0][1])+' Z'+str(z[0])+' F5000.0\n') #บนขวา
            f.write('G1 X'+str(corner[1][0])+' Y'+str(corner[1][1])+' Z'+str(z[0])+' F1500.0 E'+str(rect_num[0])+'\n')
            f.write('G1 X'+str(corner[1][0])+' Y'+str(corner[1][1])+' Z'+str(z[0])+' F5000.0\n') #บนซ้าย
            f.write('G1 X'+str(corner[2][0])+' Y'+str(corner[2][1])+' Z'+str(z[0])+' F1500.0 E'+str(rect_num[1])+'\n')
            f.write('G1 X'+str(corner[2][0])+' Y'+str(corner[2][1])+' Z'+str(z[0])+' F5000.0\n') #ล่างซ้าย
            f.write('G1 X'+str(corner[3][0])+' Y'+str(corner[3][1])+' Z'+str(z[0])+' F1500.0 E'+str(rect_num[2])+'\n')
            f.write('G1 X'+str(corner[3][0])+' Y'+str(corner[3][1])+' Z'+str(z[0])+' F5000.0\n') #ล่างขวา
            f.write('G1 X'+str(corner[0][0])+' Y'+str(corner[0][1])+' Z'+str(z[0])+' F1500.0 E'+ str(rect_num[3])+'\n')
            corner[0][0] -= 0.2 * 0.5;corner[0][1] -= 0.2 * 0.5
            corner[1][0] += 0.2 * 0.5;corner[1][1] -= 0.2 * 0.5
            corner[2][0] += 0.2 * 0.5;corner[2][1] += 0.2 * 0.5
            corner[3][0] -= 0.2 * 0.5;corner[3][1] += 0.2 * 0.5
            f.write('G0 X'+str(corner[0][0])+' Y'+str(corner[0][1])+' Z'+str(z[0])+' F5000.0\n')
            for r in range(len(rect_num)):
                rect_num[r] += 4
        corner = [[wx*scale + 30,hy*scale + 30],[30,hy*scale + 30],[30,30],[wx*scale + 30,30]]
        z[0] += 0.28  
    for i in range(3):
        for k,i in enumerate(n_vec):
            #print(vec[k])
            f.write('G1 X' + str(i[sx] * scale + 30) + ' ' + 'Y' + str(i[sy] * scale  + 30) + ' Z' +str(z[0])+' F5000.0'+'\n')
            f.write('G1 X' + str(i[ex] * scale  + 30) + ' ' + 'Y' + str(i[ey] * scale  + 30) + ' Z' +str(z[0])+' F1500.0 ' + 'E' + str(rect_num[0] + k) + '\n')
        z[0] += 0.28  
    f.write('M140 S0\n')
    f.write('M107\n')
    f.write('G91\n') 
    f.write('G1 E-2 F2700\n') 
    f.write('G1 E-2 Z0.2 F2400\n') 
    f.write('G1 X5 Y5 F3000\n') 
    f.write('G1 Z10\n') 
    f.write('G90\n') 
    f.write('G1 X0 Y235\n') 
    f.write('M106 S0\n') 
    f.write('M104 S0\n') 
    f.write('M140 S0\n')
    f.write('M84 X Y E\n') 
    f.write('M82\n') 
    f.write('M104 S0')