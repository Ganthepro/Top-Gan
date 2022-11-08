from PIL import Image, ImageDraw, ImageTk, ImageOps
import numpy as np
from stl import mesh

#change parameter here
filename = "HT19-C00514-NHU036814-2SAM_CARVE.tif" #file name as load
xscale=0.15 #x scale
yscale=0.15 #y scale
thickness=1#line thickness
bz=0.4#background thickness
pz=1 #pattern thickness

img = ImageOps.flip(Image.open(filename))
wx, hy = img.size
px = img.load()

print("file name :",filename)
print("picture size x:",wx,", y:",hy)

vec=[]
for y in reversed(range(hy)):
    for x in range(wx):   
        a=px[x,y]
        if y-1<0: 
            #vec.append([x,y,x+1,y]) #bottom frame
            b=-1
            c=px[x,y]       
        else: 
            b=px[x,y-1]
        if x+1==wx: 
            #vec.append([x+1,y,x+1,y+1]) #right frame
            d=-1
            c=px[x,y]
        else: 
            d=px[x+1,y] 

        if(y>0 and x+1!=wx): c=px[x+1,y-1]
        if x==0: vec.append([x,y,x,y+1]) #left frame 
        if y+1==hy: vec.append([x,y+1,x+1,y+1]) #top frame
    
        #line vector
        if a!=b: 
            vec.append([x ,y ,x+1,y]) #[prev,sx,sy,ex,eyo,next,status]            
        if a!=d:
            vec.append([x+1,y+1,x+1,y]) #[prev,sx,sy,ex,eyo,next,status]
           
# Define the 8 vertices of the cube
ver=[]
fac=[]
obj=0

print("scale x:",xscale,"mm, y:",yscale,"mm")
print("print scale x:",round(wx*xscale,2),"mm, y:",round(hy*yscale,2),"mm")
print("line tickness :",thickness,"mm")
print("background thickness :",bz,"mm")
print("pattern thickness:",pz,"mm")

for v in vec:
    if obj==0 and bz>0:
        #background
        x1=0; y1=0;
        x2=wx*xscale; y2=hy*yscale
        z=bz
        ver.append([x1,y1,z])
        ver.append([x1,y2,z]) 
        ver.append([x2,y2,z])
        ver.append([x2,y1,z])
        ver.append([x1,y1,0])
        ver.append([x1,y2,0]) 
        ver.append([x2,y2,0])
        ver.append([x2,y1,0])

        i=obj*8
        fac.append([i+0,i+3,i+1])
        fac.append([i+1,i+3,i+2])
        fac.append([i+0,i+4,i+7])
        fac.append([i+0,i+7,i+3])
        fac.append([i+4,i+5,i+6])
        fac.append([i+4,i+6,i+7])
        fac.append([i+5,i+1,i+2])
        fac.append([i+5,i+2,i+6])
        fac.append([i+2,i+3,i+6])
        fac.append([i+3,i+7,i+6])
        fac.append([i+0,i+1,i+5])
        fac.append([i+0,i+5,i+4])
        obj+=1

    #pattern
    # x1=v[0]*xscale; y1=v[1]*yscale
    # x2=v[2]*xscale; y2=v[3]*yscale
    #
    # if x1==x2:
    #     x2=x1+thickness
    #     if y1>y2:
    #         t=y1; y1=y2; y2=t
    # if y1==y2:
    #     y2=y1+thickness
    #     if x1>x2:
    #         t=x1; x1=x2; x2=t
    #
    # z=bz+pz
    # ver.append([x1,y1,z])
    # ver.append([x1,y2,z])
    # ver.append([x2,y2,z])
    # ver.append([x2,y1,z])
    # ver.append([x1,y1,0])
    # ver.append([x1,y2,0])
    # ver.append([x2,y2,0])
    # ver.append([x2,y1,0])
    #
    # i=obj*8
    # fac.append([i+0,i+3,i+1])
    # fac.append([i+1,i+3,i+2])
    # fac.append([i+0,i+4,i+7])
    # fac.append([i+0,i+7,i+3])
    # fac.append([i+4,i+5,i+6])
    # fac.append([i+4,i+6,i+7])
    # fac.append([i+5,i+1,i+2])
    # fac.append([i+5,i+2,i+6])
    # fac.append([i+2,i+3,i+6])
    # fac.append([i+3,i+7,i+6])
    # fac.append([i+0,i+1,i+5])
    # fac.append([i+0,i+5,i+4])
    # obj+=1

vertices = np.array(ver)
faces = np.array(fac)
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cube.stl"
cube.save('surface_test'+'.stl')
