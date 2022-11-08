from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
from stl import mesh

filename = "pngtree-golden-and-green-thai-pattern-background-png-image_5868435.bmp" #HT19-C00514-NHU036814-2SAM_CARVE.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
xshift=0
yshift=-1
scale=1
bg_color = [0,0,1]
im = Image.new('RGBA', (wx*scale, hy*scale), (bg_color[0], bg_color[1], bg_color[2], 255))
sx,sy,ex,ey = 1,2,3,4
r,g,b = 2,1,0
resize_cv2 = cv2.resize(img_cv2,(wx*scale,hy*scale))
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
        # blue = img_cv2[y, x, 0]
        # green = img_cv2[y, x, 1]
        # red = img_cv2[y, x, 2]
        # if y-1<0:#บน
        #     b=px[x,y]
        # else:
        #     b=px[x,y-1]
        # if x+1==wx:#ขวา
        #     c=px[x,y]
        # else:
        #     c=px[x+1,y]
        # if y - 1 < 0:#บน
        #     d = px[x,y]
        # else:
        #     d = px[x,y-1]
        # if x - 1 < 0:#ซ้าย
        #     e=px[x,y]
        # else:
        #     e=px[x-1,y]
        # if y+1 >= hy:#ล่าง
        #     f=px[x,y]
        # else:
        #     f=px[x,y+1]
        # if y+1 == hy:
        #     g = px[x, y]
        # elif x+1==wx:#ล่างขวา
        #     g=px[x,y]
        # else:
        #     g=px[x+1,y+1]
        # if y+1 == hy:
        #     h = px[x, y]
        # elif x-1<0:#ล่างซ้าย
        #     h=px[x,y]
        # else:
        #     h=px[x-1,y+1]
        # if y-1 < 0:
        #     j = px[x, y]
        # elif x+1==wx:#บนขวา
        #     j=px[x,y]
        # else:
        #     j=px[x+1,y-1]
        # if y-1 < 0:
        #     k = px[x, y]
        # elif x-1<0:#บนซ้าย
        #     k=px[x,y]
        # else:
        #     k=px[x-1,y-1]
        # if px[x,y] != b and px[x,y] != c:
        #     idx += 1;
        #     vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x,y] == e:
        #     if px[x,y] != b:
        #         idx += 1;
        #         vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] == b:
        #     if px[x, y] != c:
        #         if px[x, y] == j:
        #             pass
        #         else:
        #             idx += 1;
        #             vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # if px[x,y] != b and px[x,y] != e:
        #     idx += 1;
        #     vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
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
        #         vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
        # elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
        #     if px[x, y] == j:
        #         pass
        #     else:
        #         idx += 1;
        #         vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
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
px_im = im.load()
draw = ImageDraw.Draw(im)
for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift*scale,
            (i[sy]*scale)+yshift*scale,
            (i[ex]*scale)+xshift*scale,
            (i[ey]*scale)+yshift*scale
        ), fill=(0, 255, 0, 255))
im.show()
image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
original_cv2 = cv2.imread(filename)
#print(vec)
multi_vertices = []
multi_faces = []
faces = []
loop = 0
z = 3
height = 7
width_x = 0.5
width_y = 0.5
for i in vec:
    if (i[sy] > i[ey] or i[sy] < i[ey]) and i[sx] == i[ex]:
        p1 = [(i[sx] * scale / 1) * 0.27 + 20, (i[sy] * scale / 1) * 0.27 + 20, z]
        p2 = [(i[sx] * scale / 1) * 0.27 - width_x + 20, (i[sy] * scale / 1) * 0.27 + 20, z]
        p3 = [(i[ex] * scale / 1) * 0.27 - width_x + 20, (i[ey] * scale / 1) * 0.27 + width_y + 20, z]
        p4 = [(i[ex] * scale / 1) * 0.27 + 20, ((i[ey] * scale / 1) * 0.27 + width_y) + 20, z]
        p5 = [(i[sx] * scale / 1) * 0.27 + 20, (i[sy] * scale / 1) * 0.27 + 20, z + height]
        p6 = [((i[sx] * scale / 1) * 0.27 - width_x) + 20, (i[sy] * scale / 1) * 0.27 + 20, z + height]
        p7 = [((i[ex] * scale / 1) * 0.27 - width_x) + 20, ((i[ey] * scale / 1) * 0.27 + width_y) + 20, z + height]
        p8 = [(i[ex] * scale / 1) * 0.27 + 20, ((i[ey] * scale / 1) * 0.27 + width_y) + 20, z + height]
        vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
        top_face1 = np.array([p2, p1, p4]);top_face2 = np.array([p2, p3, p4])
        right_face1 = np.array([p1,p5,p4]);right_face2 = np.array([p4,p8,p5])
        left_face1 = np.array([p2, p6, p3]);left_face2 = np.array([p3, p7, p6])
        front_face1 = np.array([p1,p5,p2]);front_face2 = np.array([p2,p6,p5])
        back_face1 = np.array([p3,p7,p4]);back_face2 = np.array([p4,p8,p7])
        bottom_face1 = np.array([p6, p5, p8]);bottom_face2 = np.array([p6, p7, p8])
    else:
        p1 = [i[sx] * scale / 1 * 0.27 + 20, i[sy] * scale / 1 * 0.27 + 20, z]
        p2 = [i[sx] * scale / 1 * 0.27 + 20, (i[sy] * scale / 1) * 0.27 + width_y + 20, z]
        p3 = [i[ex] * scale / 1 * 0.27 + 20, (i[ey] * scale / 1) * 0.27 + width_y + 20, z]
        p4 = [i[ex] * scale / 1 * 0.27 + 20, i[ey] * scale / 1 * 0.27 + 20, z]
        p5 = [i[sx] * scale / 1 * 0.27 + 20, i[sy] * scale / 1 * 0.27 + 20, z + height]
        p6 = [i[sx] * scale / 1 * 0.27 + 20, (i[sy] * scale / 1 * 0.27) + width_y + 20, z + height]
        p7 = [i[ex] * scale / 1 * 0.27 + 20, (i[ey] * scale / 1 * 0.27) + width_y + 20, z + height]
        p8 = [i[ex] * scale / 1 * 0.27 + 20, i[ey] * scale / 1 * 0.27 + 20, z + height]
        vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
        top_face1 = np.array([p1, p2, p3]);top_face2 = np.array([p1, p4, p3])
        right_face1 = np.array([p4, p8, p5]);right_face2 = np.array([p4, p1, p5])
        left_face1 = np.array([p2, p6, p3]);left_face2 = np.array([p3, p7, p6])
        front_face1 = np.array([p1,p5,p2]);front_face2 = np.array([p2, p6, p5])
        back_face1 = np.array([p3,p7,p4]);back_face2 = np.array([p4,p8,p7])
        bottom_face1 = np.array([p5, p6, p7]);bottom_face2 = np.array([p5, p8, p7])
    multi_vertices.append(vertices)
    faces.append(top_face1);faces.append(top_face2)
    faces.append(right_face1);faces.append(right_face2)
    faces.append(left_face1);faces.append(left_face2)
    faces.append(front_face1);faces.append(front_face2)
    faces.append(back_face1);faces.append(back_face2)
    faces.append(bottom_face1);faces.append(bottom_face2)
    loop += 1

#for i in vec:
p1 = [19, 20, 0]
p2 = [19, (n_hy * 0.27) + 21, 0]
p3 = [(n_wx * 0.27) + 20, 20, 0]#
p4 = [(n_wx * 0.27) + 20, (n_hy * 0.27) + 21, 0]#
p5 = [19, 20, z]
p6 = [19, (n_hy * 0.27) + 21, z]
p7 = [(n_wx * 0.27) + 20, 20, z]
p8 = [(n_wx * 0.27) + 20, (n_hy * 0.27) + 21, z]#
# p1 = [n_wx * 0.27 + 20, n_hy * 0.27 + 20, 0]
# p2 = [n_wx * 0.27 + 20, (n_hy + 1) * 0.27 + 20, 0]
# p3 = [(n_wx + 1) * 0.27 + 20, n_hy * 0.27 + 20, 0]
# p4 = [(n_wx + 1) * 0.27 + 20, (n_hy + 1) * 0.27 + 20, 0]
# p5 = [n_wx * 0.27 + 20, n_hy * 0.27 + 20, z]
# p6 = [n_wx * 0.27 + 20, (n_hy + 1) * 0.27 + 20, z]
# p7 = [(n_wx + 1) * 0.27 + 20, n_hy * 0.27 + 20, z]
# p8 = [(n_wx + 1) * 0.27 + 20, (n_hy + 1) * 0.27 + 20, z]
face1_1 = np.array([p8, p6, p5]);face1_2 = np.array([p8, p7, p5])
face2_1 = np.array([p4, p8, p6]);face2_2 = np.array([p4, p2, p6])
face1_1 = np.array([p3, p7, p5]);left_face2 = np.array([p3, p1, p5])
face1_1 = np.array([p3, p7, p8]);front_face2 = np.array([p3, p4, p8])
face1_1 = np.array([p2, p6, p5]);back_face2 = np.array([p2, p1, p5])
face1_1 = np.array([p2, p1, p3]);bottom_face2 = np.array([p2, p4, p3])
faces.append(top_face1);faces.append(top_face2)
faces.append(right_face1);faces.append(right_face2)
faces.append(left_face1);faces.append(left_face2)
faces.append(front_face1);faces.append(front_face2)
faces.append(back_face1);faces.append(back_face2)
faces.append(bottom_face1);faces.append(bottom_face2)
print(x,y)

print('vec : ',len(vec))
print('loop1 : ',loop)
loop = 0
multi_vertices_np = np.array(faces)
cube = mesh.Mesh(np.zeros(multi_vertices_np.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = multi_vertices_np[i][j]
        #print(multi_vertices_np[i][j])
cube.save('surface_test.stl')

