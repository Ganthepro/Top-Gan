import ezdxf as dxf
from PIL import Image

doc = dxf.new('R2010')
msp = doc.modelspace()

filename = "CS 268-19 - 12S190321-02map.tif" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()

vec=[]
idx=-1
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
            h=px[x,y]
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

sx,sy,ex,ey = 1,2,3,4

for i in vec:
    msp.add_line((i[sx], i[sy]), (i[ex], i[ey]))

doc.saveas('line.dxf')