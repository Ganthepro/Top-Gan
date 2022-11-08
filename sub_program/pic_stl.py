import numpy as np
from stl import mesh
from PIL import Image, ImageDraw, ImageTk, ImageOps

filename = "HT19-C00514-NHU036814-2SAM_CARVE.tif"
img = ImageOps.flip(Image.open(filename)).convert("RGB")
colors=img.getcolors()
wx, hy = img.size
px = img.load()
print(wx,",",hy)
co=len(colors)
print("colors:",co)

vec=[]
fac=[]
obj=0
x,y = 0,0
xs=0.5
ys=0.5
zs=10

for y in reversed(range(hy)):
    print(round((y/hy)*100,0),"%       ",end='\r')
    for x in range(wx):   
        a=px[x,y]
        i=0
        for c in colors:
            if a==c[1]:
                break
            i+=1
       
        z=(i/co)*zs

        x1=x*xs
        x2=x1+xs
        y1=y*ys
        y2=y1+ys
        vec.append([x1,y1,z])
        vec.append([x1,y2,z]) 
        vec.append([x2,y2,z])
        vec.append([x2,y1,z])
        vec.append([x1,y1,0])
        vec.append([x1,y2,0]) 
        vec.append([x2,y2,0])
        vec.append([x2,y1,0])

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


vertices = np.array(vec)
faces = np.array(fac)

print("Create the mesh...Please waiting...")

cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cube.stl"
cube.save('cube.stl')
