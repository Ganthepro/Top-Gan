from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
from stl import mesh
try:
    size_input = 5
    img = cv2.imread(r'project\cv2_test\Cat03.jpg', 0)
    original_img = cv2.imread(r'project\cv2_test\Cat03.jpg')
    if size_input % 2 != 1:
        size_input += 1
    resize = cv2.resize(img, (size_input*100, size_input*100))
    resize_original = cv2.resize(original_img, (size_input * 100, size_input * 100))
    adaptive = cv2.adaptiveThreshold(resize,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,7)
    color = cv2.cvtColor(adaptive,cv2.COLOR_BGR2RGB)
    color[np.where((color==[0, 0, 0]).all(axis=2))] = [0, 0, 255]
    color[np.where((color==[255, 255, 255]).all(axis=2))] = [0, 0, 0]
    #kernal = np.ones((1,2),np.uint8)
    #morpho = cv2.morphologyEx(color,cv2.MORPH_OPEN,kernal)
    # cv2.imshow('test',resize_original)
    # cv2.imshow('result',color)
    cv2.imwrite('test_cat.png',color)
    #cv2.imshow('morpho',morpho)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('test')
except Exception as e:
    print(e)

filename = "test_cat.png" #HT19-C00514-NHU036814-2SAM_CARVE.tif #H20-C00175-11S190500-04-sample.tif
img = Image.open(filename)
wx, hy = img.size
px = img.load()
img_cv2 = cv2.imread(filename)
xshift=0
yshift=-1
scale=1
bg_color = [0,0,1]
im = Image.new('RGBA', (wx*scale, hy*scale), (255, 255, 255, 255))
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
count = 0
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
        count += 1
    print("{:.2f}".format((count * 100) / (hy * wx)), ' %')
px_im = im.load()
draw = ImageDraw.Draw(im)
for i in vec:
    draw.line(
        (   (i[sx]*scale)+xshift*scale,
            (i[sy]*scale)+yshift*scale,
            (i[ex]*scale)+xshift*scale,
            (i[ey]*scale)+yshift*scale
        ), fill=(0, 0, 0, 255))
im.show()
im.save('test.png')
# image_cv2 = cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
# original_cv2 = cv2.imread(filename)
# #print(vec)
# multi_vertices = []
# multi_faces = []
# faces = []
# loop = 0
# z = 3
# height = 1
# width_x = 0.75
# width_y = 0.75
# count = 0
# for i in vec:
#     if i[sy] == i[ey]:
#         p1 = [i[sx] * scale / 1 * 0.35 + 20, i[sy] * scale / 1 * 0.35 + 20, z]  # ---
#         p2 = [i[ex] * scale / 1 * 0.35 + 20, i[ey] * scale / 1 * 0.35 + 20, z]  # +--
#         p3 = [i[ex] * scale / 1 * 0.35 + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z]  # ++-
#         p4 = [i[sx] * scale / 1 * 0.35 + 20, (i[sy] * scale / 1) * 0.35 + width_y + 20, z]  # -+-
#         p5 = [i[sx] * scale / 1 * 0.35 + 20, i[sy] * scale / 1 * 0.35 + 20, z + height]  # --+
#         p6 = [i[ex] * scale / 1 * 0.35 + 20, i[ey] * scale / 1 * 0.35 + 20, z + height]  # +-+
#         p7 = [i[ex] * scale / 1 * 0.35 + 20, (i[ey] * scale / 1 * 0.35) + width_y + 20, z + height]  # +++
#         p8 = [i[sx] * scale / 1 * 0.35 + 20, (i[sy] * scale / 1 * 0.35) + width_y + 20, z + height]  # -++
#         vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
#         face1_1 = np.array([p1, p4, p2]);
#         face1_2 = np.array([p2, p4, p3])
#         face2_1 = np.array([p1, p5, p8]);
#         face2_2 = np.array([p1, p8, p4])
#         face3_1 = np.array([p5, p6, p7]);
#         face3_2 = np.array([p5, p7, p8])
#         face4_1 = np.array([p6, p2, p3]);
#         face4_2 = np.array([p6, p3, p7])
#         face5_1 = np.array([p3, p4, p7]);
#         face5_2 = np.array([p4, p8, p7])
#         face6_1 = np.array([p1, p2, p6]);
#         face6_2 = np.array([p1, p6, p5])
#         multi_vertices.append(vertices)
#         faces.append(face1_1);faces.append(face1_2)
#         faces.append(face2_1);faces.append(face2_2)
#         faces.append(face3_1);faces.append(face3_2)
#         faces.append(face4_1);faces.append(face4_2)
#         faces.append(face5_1);faces.append(face5_2)
#         faces.append(face6_1);faces.append(face6_2)
#         loop += 1
#         vec.pop(vec.index(i))
#         print("{:.2f}".format(25 + ((count * 50) / len(vec))), ' %')
#     count += 1
# count = 0
# for i in vec:
#     #pass
#     if i[sx] == i[ex]:
#         p1 = [(i[sx] * scale / 1) * 0.35 + 20, (i[sy] * scale / 1) * 0.35 + 20, z]  # ---
#         p2 = [(i[sx] * scale / 1) * 0.35 + width_x + 20, (i[sy] * scale / 1) * 0.35 + 20, z]  # +--
#         p3 = [(i[ex] * scale / 1) * 0.35 + width_x + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z]  # ++-
#         p4 = [(i[ex] * scale / 1) * 0.35 + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z]  # -+-
#         p5 = [(i[sx] * scale / 1) * 0.35 + 20, (i[sy] * scale / 1) * 0.35 + 20, z + height]  # --+
#         p6 = [(i[sx] * scale / 1) * 0.35 + width_x + 20, (i[sy] * scale / 1) * 0.35 + 20, z + height]  # +-+
#         p7 = [(i[ex] * scale / 1) * 0.35 + width_x + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z + height]  # +++
#         p8 = [(i[ex] * scale / 1) * 0.35 + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z + height]  # -++
#         vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
#         face1_1 = np.array([p1, p4, p2]);
#         face1_2 = np.array([p2, p4, p3])
#         face2_1 = np.array([p1, p5, p8]);
#         face2_2 = np.array([p1, p8, p4])
#         face3_1 = np.array([p5, p6, p7]);
#         face3_2 = np.array([p5, p7, p8])
#         face4_1 = np.array([p6, p2, p3]);
#         face4_2 = np.array([p6, p3, p7])
#         face5_1 = np.array([p3, p4, p7]);
#         face5_2 = np.array([p4, p8, p7])
#         face6_1 = np.array([p1, p2, p6]);
#         face6_2 = np.array([p1, p6, p5])
#         multi_vertices.append(vertices)
#         faces.append(face1_1);
#         faces.append(face1_2)
#         faces.append(face2_1);
#         faces.append(face2_2)
#         faces.append(face3_1);
#         faces.append(face3_2)
#         faces.append(face4_1);
#         faces.append(face4_2)
#         faces.append(face5_1);
#         faces.append(face5_2)
#         faces.append(face6_1);
#         faces.append(face6_2)
#     else:
#         p1 = [i[sx] * scale / 1 * 0.35 + 20, i[sy] * scale / 1 * 0.35 + 20, z]  # ---
#         p2 = [i[ex] * scale / 1 * 0.35 + 20, i[ey] * scale / 1 * 0.35 + 20, z]  # +--
#         p3 = [i[ex] * scale / 1 * 0.35 + 20, (i[ey] * scale / 1) * 0.35 + width_y + 20, z]  # ++-
#         p4 = [i[sx] * scale / 1 * 0.35 + 20, (i[sy] * scale / 1) * 0.35 + width_y + 20, z]  # -+-
#         p5 = [i[sx] * scale / 1 * 0.35 + 20, i[sy] * scale / 1 * 0.35 + 20, z + height]  # --+
#         p6 = [i[ex] * scale / 1 * 0.35 + 20, i[ey] * scale / 1 * 0.35 + 20, z + height]  # +-+
#         p7 = [i[ex] * scale / 1 * 0.35 + 20, (i[ey] * scale / 1 * 0.35) + width_y + 20, z + height]  # +++
#         p8 = [i[sx] * scale / 1 * 0.35 + 20, (i[sy] * scale / 1 * 0.35) + width_y + 20, z + height]  # -++
#         vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
#         face1_1 = np.array([p1, p4, p2]);
#         face1_2 = np.array([p2, p4, p3])
#         face2_1 = np.array([p1, p5, p8]);
#         face2_2 = np.array([p1, p8, p4])
#         face3_1 = np.array([p5, p6, p7]);
#         face3_2 = np.array([p5, p7, p8])
#         face4_1 = np.array([p6, p2, p3]);
#         face4_2 = np.array([p6, p3, p7])
#         face5_1 = np.array([p3, p4, p7]);
#         face5_2 = np.array([p4, p8, p7])
#         face6_1 = np.array([p1, p2, p6]);
#         face6_2 = np.array([p1, p6, p5])
#         multi_vertices.append(vertices)
#         faces.append(face1_1);
#         faces.append(face1_2)
#         faces.append(face2_1);
#         faces.append(face2_2)
#         faces.append(face3_1);
#         faces.append(face3_2)
#         faces.append(face4_1);
#         faces.append(face4_2)
#         faces.append(face5_1);
#         faces.append(face5_2)
#         faces.append(face6_1);
#         faces.append(face6_2)
#         loop += 1
#     count += 1
#     print("{:.2f}".format(50 + ((count * 50) / len(vec))), ' %')
# #for i in vec:
# p1 = [19, 20, 0]#---
# p2 = [(n_wx * 0.35) + 20, 20, 0]#+--
# p3 = [(n_wx * 0.35) + 20, (n_hy * 0.35) + 21, 0]#++-
# p4 = [19, (n_hy * 0.35) + 21, 0]#-+-
# p5 = [19, 20, z]#--+
# p6 = [(n_wx * 0.35) + 20, 20, z]#+-+
# p7 = [(n_wx * 0.35) + 20, (n_hy * 0.35) + 21, z]#+++
# p8 = [19, (n_hy * 0.35) + 21, z]#-++
# face1_1 = np.array([p1, p4, p2]);
# face1_2 = np.array([p2, p4, p3])
# face2_1 = np.array([p1, p5, p8]);
# face2_2 = np.array([p1, p8, p4])
# face3_1 = np.array([p5, p6, p7]);
# face3_2 = np.array([p5, p7, p8])
# face4_1 = np.array([p6, p2, p3]);
# face4_2 = np.array([p6, p3, p7])
# face5_1 = np.array([p3, p4, p7]);
# face5_2 = np.array([p4, p8, p7])
# face6_1 = np.array([p1, p2, p6]);
# face6_2 = np.array([p1, p6, p5])
# faces.append(face1_1);faces.append(face1_2)
# faces.append(face2_1);faces.append(face2_2)
# faces.append(face3_1);faces.append(face3_2)
# faces.append(face4_1);faces.append(face4_2)
# faces.append(face5_1);faces.append(face5_2)
# faces.append(face6_1);faces.append(face6_2)
# print(x,y)

# print('vec : ',len(vec))
# print('loop1 : ',loop)
# loop = 0
# multi_vertices_np = np.array(faces)
# cube = mesh.Mesh(np.zeros(multi_vertices_np.shape[0], dtype=mesh.Mesh.dtype))
# for i, f in enumerate(faces):
#     for j in range(3):
#         cube.vectors[i][j] = multi_vertices_np[i][j]
#         #print(multi_vertices_np[i][j])
# cube.save('surface_test1.stl')