import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import ezdxf as dxf
import svgwrite as svg
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageTk

window = tk.Tk()
window.title('Picture Converter')
window.minsize(width=600,height=600)

filename_history = ['']
bg_color = [0,0,1]

def import_pic():
    global image
    filename = filedialog.askopenfilename()
    img = Image.open(filename)
    wx, hy = img.size
    print(wx*hy)
    size = ['', '']
    if wx * hy < 160000:
        size[0] = wx // 1
        size[1] = hy // 1
        img = img.resize((size[0], size[1]))
    elif 160000 < wx * hy < 1960000:
        size[0] = wx // 3
        size[1] = hy // 3
        img = img.resize((size[0], size[1]))
    elif 1960000 < wx * hy < 4410000:
        size[0] = wx // 6
        size[1] = hy // 6
        img = img.resize((size[0], size[1]))
    elif wx * hy > 4410000:
        size[0] = wx // 9
        size[1] = hy // 9
        img = img.resize((size[0], size[1]))
    #print(size)
    if filename_history[0] == '':
        filename_history[0] = filename
        image = ImageTk.PhotoImage(img)
    elif filename_history[0] != '' and filename_history[0] != filename:
        filename_history[0] = filename
        image = ImageTk.PhotoImage(img)
        print('Selected:', filename)
    #image = ImageTk.PhotoImage(file=filename, width=size[0],height=size[1])
    image_lable = tk.Label(master=window, image=image)
    image_lable.place(x=100,y=70)

def sgv_convert():
    dwg = svg.Drawing(str(save_filename_entry.get()) + '.svg', profile='tiny')
    filename = filename_history[0]
    img = Image.open(filename)
    wx, hy = img.size
    px = img.load()
    img_cv2 = cv2.imread(filename)
    xshift = 0
    yshift = -1
    scale = int(scale_entry.get())
    im = Image.new('RGBA', (wx * scale, hy * scale), (bg_color[0], bg_color[1], bg_color[2], 255))
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
    if shape_line_cheak_box_var.get() == 1:
        for y in range(hy):
            for x in range(wx):
                blue = img_cv2[y, x, 0]
                green = img_cv2[y, x, 1]
                red = img_cv2[y, x, 2]
                if y - 1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x - 1, y]
                if y + 1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y + 1]
                if y + 1 == hy:
                    g = px[x, y]
                elif x + 1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x + 1, y + 1]
                if y + 1 == hy:
                    h = px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x - 1, y + 1]
                if y - 1 < 0:
                    j = px[x, y]
                elif x + 1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x + 1, y - 1]
                if y - 1 < 0:
                    k = px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x - 1, y - 1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1;
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1;
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1;
                            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                if px[x, y] != b and px[x, y] != e:
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
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
                dwg.add(dwg.rect((x * scale, y * scale), (0.05, 0.05), stroke=svg.rgb(red, green, blue, 'RGB')))
    else:
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
                dwg.add(dwg.rect((x * scale, y * scale), (0.05, 0.05), stroke=svg.rgb(red, green, blue, 'RGB')))
    px_im = im.load()
    draw = ImageDraw.Draw(im)
    print(len(colors))
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

    for i in vec:
        draw.line(
            ((i[sx] * scale) + xshift * scale,
             (i[sy] * scale) + yshift * scale,
             (i[ex] * scale) + xshift * scale,
             (i[ey] * scale) + yshift * scale
             ), fill=(0, 255, 1, 255))

    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (0, 255, 1, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    print('loading 50%')
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (0, 255, 1, 255):
                im.putpixel((x, y), (f[0], f[1], f[2]))

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
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (0, 255, 1, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (0, 255, 1, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] == (0, 255, 1, 255):
                # print(x, y)
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (0, 255, 1, 255):
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
    start_p_1 = [0, 0]
    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] != [bg_color[0], bg_color[1], bg_color[2]]:
                if px_im[x, y] == e:
                    id1 += 1
                elif px_im[x, y] != e:
                    # print(id1)
                    # print((0, y), ((0 + id1), y))
                    dwg.add(dwg.line((0, y), ((0 + id1), y),
                                     stroke=svg.rgb(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2], 'RGB'),
                                     stroke_width=2))
                    # pdf.line(0 / 10, y / 10, (0 + id1) / 10, y / 10)
                    # # print((start_p_1[0] + id1) / 10)
                    # pdf.set_line_width(0.2)
                    # pdf.set_draw_color(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                    id1 = 0
                    break
    id = 1
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
                    # print(id)
                elif px_im[x, y] != e:
                    # print('1.', start_p)
                    # print('2.', id)
                    # print((start_p[0], start_p[1]), ((start_p[0] + id), start_p[1]))
                    dwg.add(dwg.line((start_p[0], start_p[1]), ((start_p[0] + id), start_p[1]),
                                     stroke=svg.rgb(px_im[start_p[0], start_p[1]][0], px_im[start_p[0], start_p[1]][1],
                                                    px_im[start_p[0], start_p[1]][2], 'RGB'), stroke_width=2))
                    # pdf.line(start_p[0] / 10, start_p[1] / 10, (start_p[0] + id) / 10, start_p[1] / 10)
                    # pdf.set_line_width(0.23)
                    # pdf.set_draw_color(px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                    # print('3.',start_p[0]+id)
                    # print('4.',px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                    id = 1
                    start_p[0] = x
                    start_p[1] = y
    print('loading 75%')
    if drawing_lines_cheak_box_var.get() == 0:
        if shape_line_cheak_box_var.get() == 1:
            count_1 = 0
            for y in range(0, n_hy, scale):
                for x in range(0, n_wx, scale):
                    for i in vec:
                        if x == (i[ex] * scale) + xshift and y == (i[ey] - 1) * scale:
                            #print((((i[sx] * scale) + xshift, (i[sy] * scale))),((i[ex] * scale) + xshift, (i[ey] * scale)))
                            dwg.add(dwg.line(((i[sx] * scale) + 1 + xshift, (i[sy] - 1) * scale),
                                             ((i[ex] * scale) + 1 + xshift, (i[ey] - 1) * scale),
                                             stroke=svg.rgb(px_im[(i[ex] * scale) + xshift, i[ey] * scale - 1][0],
                                                            px_im[(i[ex] * scale) + xshift, i[ey] * scale - 1][1],
                                                            px_im[(i[ex] * scale) + xshift, i[ey] * scale - 1][2], 'RGB')))
                            count_1 += 1
                a_float = float(((25 * y) / n_hy) + 75)
                print('loading ', "{:.2f}".format(a_float),'%')
    else:
        for i in vec:
            #print(((i[sx] * scale) + xshift, (i[sy] * scale) + (yshift - 2)), ((i[ex] * scale) + xshift, (i[ey] * scale) + (yshift - 2)))
            dwg.add(dwg.line(((i[sx] * scale) + xshift + 1, (i[sy] * scale) + (yshift - 2)), ((i[ex] * scale) + xshift + 1, (i[ey] * scale) + (yshift - 2)),stroke=svg.rgb(0, 255, 0, 'RGB')))

    image_cv2 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    original_cv2 = cv2.imread(filename)
    cv2.imwrite('test.png', image_cv2)
    dwg.save()
    print('loading 100%')

def pdf_convert():
    filename = filename_history[0]
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
    scale = int(scale_entry.get())
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
    if shape_line_cheak_box_var.get() == 1:
        for y in range(hy):
            for x in range(wx):
                blue = img_cv2[y, x, 0]
                green = img_cv2[y, x, 1]
                red = img_cv2[y, x, 2]
                if y - 1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x - 1, y]
                if y + 1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y + 1]
                if y + 1 == hy:
                    g = px[x, y]
                elif x + 1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x + 1, y + 1]
                if y + 1 == hy:
                    h = px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x - 1, y + 1]
                if y - 1 < 0:
                    j = px[x, y]
                elif x + 1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x + 1, y - 1]
                if y - 1 < 0:
                    k = px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x - 1, y - 1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1;
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1;
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1;
                            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                if px[x, y] != b and px[x, y] != e:
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
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
    else:
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
    for_len = 0
    print(len(RGB))
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
    draw = ImageDraw.Draw(im)
    for i in vec:
        draw.line(
            ((i[sx] * scale) + pic_xshift * scale,
             (i[sy] * scale) + pic_yshift * scale,
             (i[ex] * scale) + pic_xshift * scale,
             (i[ey] * scale) + pic_yshift * scale
             ), fill=(0, 255, 1, 255))
    print('loading 25%')
    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (
            0, 255, 1, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    print('loading 45%')
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (
            0, 255, 1, 255):
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
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (
            0, 255, 1, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))
    print('loading 75%')
    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (
            0, 255, 1, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))
    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] == (0, 255, 1, 255):
                # print(x, y)
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (0, 255, 1, 255):
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
    print('loading 85%')
    id1 = 0
    start_p_1 = [0, 0]
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
                    # print((start_p_1[0] + id1) / 10)
                    pdf.set_line_width(0.2)
                    pdf.set_draw_color(px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                    id1 = 0
                    break
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
                    if start_p[0] + id > n_wx - 2:
                        continue
                    else:
                        id += 1
                elif px_im[x, y] != e:
                    # print('1.', start_p)
                    # print('2.', id)
                    pdf.line(start_p[0] / 10, start_p[1] / 10, (start_p[0] + id) / 10, start_p[1] / 10)
                    pdf.set_line_width(0.23)
                    pdf.set_draw_color(px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                    # print('3.',start_p[0]+id)
                    id = 0
                    start_p[0] = x
                    start_p[1] = y
    print('loading 100%')
    if drawing_lines_cheak_box_var.get() == 1:
        for i in vec:
            line = pdf.line(i[sx], i[sy] - 1, i[ex], i[ey] - 1)
            pdf.set_draw_color(0, 255, 0)
    # im.show()
    # pdf.set_fill_color(255,255,0)
    # im.show('test.png')
    pdf.output(str(save_filename_entry.get()) + ".pdf")

def dxf_convert():
    doc = dxf.new('R2010')
    msp = doc.modelspace()
    filename = filename_history[0]
    img = Image.open(filename)
    wx, hy = img.size
    px = img.load()
    vec = []
    idx = -1
    if shape_line_cheak_box_var.get() == 0:
        for y in range(hy):
            for x in range(wx):
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
    else:
        for y in range(hy):
            for x in range(wx):
                if y - 1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x - 1, y]
                if y + 1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y + 1]
                if y + 1 == hy:
                    g = px[x, y]
                elif x + 1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x + 1, y + 1]
                if y + 1 == hy:
                    h = px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x - 1, y + 1]
                if y - 1 < 0:
                    j = px[x, y]
                elif x + 1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x + 1, y - 1]
                if y - 1 < 0:
                    k = px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x - 1, y - 1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1;
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1;
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1;
                            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                if px[x, y] != b and px[x, y] != e:
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
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
    print('loading 50%')
    sx, sy, ex, ey = 1, 2, 3, 4

    for i in vec:
        msp.add_line((i[sx], i[sy]), (i[ex], i[ey]))
    doc.saveas(str(save_filename_entry.get()) + '.dxf')
    print('loading 100%')

def Upscale_line():
    img = Image.open(filename_history[0])
    wx, hy = img.size
    px = img.load()
    img_cv2 = cv2.imread(filename_history[0])
    # window = Tk()
    # window.title("Pattern Matching")
    xshift = 0
    yshift = -1
    scale = int(scale_entry.get())
    im = Image.new('RGBA', (wx * scale, hy * scale), (bg_color[0], bg_color[1], bg_color[2], 255))
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
    if shape_line_cheak_box_var.get() == 0:
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
    else:
        for y in range(hy):
            for x in range(wx):
                blue = img_cv2[y, x, 0]
                green = img_cv2[y, x, 1]
                red = img_cv2[y, x, 2]
                if y - 1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x - 1, y]
                if y + 1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y + 1]
                if y + 1 == hy:
                    g = px[x, y]
                elif x + 1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x + 1, y + 1]
                if y + 1 == hy:
                    h = px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x - 1, y + 1]
                if y - 1 < 0:
                    j = px[x, y]
                elif x + 1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x + 1, y - 1]
                if y - 1 < 0:
                    k = px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x - 1, y - 1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1;
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1;
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1;
                            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                if px[x, y] != b and px[x, y] != e:
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
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
    print('loading 50%')
    draw = ImageDraw.Draw(im)
    for i in vec:
        draw.line(
            ((i[sx] * scale) + xshift * scale,
             (i[sy] * scale) + yshift * scale,
             (i[ex] * scale) + xshift * scale,
             (i[ey] * scale) + yshift * scale
             ), fill=(0, 255, 1, 255))
    print('loading 100%')
    image_cv2 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    original_cv2 = cv2.imread(filename_history[0])
    im.show(str(save_filename_entry.get()) + '.png')
    cv2.imwrite(str(save_filename_entry.get()) + '.png', image_cv2)

def Upscale_color():
    print(filename_history[0])
    img = Image.open(filename_history[0])
    wx, hy = img.size
    px = img.load()
    img_cv2 = cv2.imread(filename_history[0])
    #window = Tk()
    #window.title("Pattern Matching")
    xshift = 0
    yshift = -1
    scale = int(scale_entry.get())
    im = Image.new('RGBA', (wx * scale, hy * scale), (bg_color[0], bg_color[1], bg_color[2], 255))
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
    if shape_line_cheak_box_var.get() == 0:
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
    else:
        for y in range(hy):
            for x in range(wx):
                blue = img_cv2[y, x, 0]
                green = img_cv2[y, x, 1]
                red = img_cv2[y, x, 2]
                if y - 1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x - 1, y]
                if y + 1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y + 1]
                if y + 1 == hy:
                    g = px[x, y]
                elif x + 1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x + 1, y + 1]
                if y + 1 == hy:
                    h = px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x - 1, y + 1]
                if y - 1 < 0:
                    j = px[x, y]
                elif x + 1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x + 1, y - 1]
                if y - 1 < 0:
                    k = px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x - 1, y - 1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1;
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1;
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1;
                            vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                if px[x, y] != b and px[x, y] != e:
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
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
    px_im = im.load()

    for_len = 0
    #print(len(RGB))

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
            ((i[sx] * scale) + xshift * scale,
             (i[sy] * scale) + yshift * scale,
             (i[ex] * scale) + xshift * scale,
             (i[ey] * scale) + yshift * scale
             ), fill=(0, 255, 1, 255))

    print('loading 25%')

    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (
                    0, 255, 1, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    print('loading 45%')
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (
                    0, 255, 1, 255):
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
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (
                    0, 255, 1, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))
    print('loading 75%')
    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (
                    0, 255, 1, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))
    print('loading 85%')
    if drawing_lines_cheak_box_var.get() == 0:
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] == (0, 255, 1, 255):
                    #print(x, y)
                    im.putpixel((x, y), (e[0], e[1], e[2]))

        for y in range(n_hy):
            for x in range(n_wx):
                if y - 1 < 0:  # บน
                    b = px_im[x, y]
                else:
                    b = px_im[x, y - 1]
                if px_im[x, y] == (0, 255, 1, 255):
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

    print('loading 100%')
    px2 = im.load()

    image_cv2 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    original_cv2 = cv2.imread(filename_history[0])
    im.show(str(save_filename_entry.get()) + '.png')
    cv2.imwrite(str(save_filename_entry.get()) + '.png', image_cv2)

def stl_convert():
    pass

shape_line_cheak_box_var = tk.IntVar()
drawing_lines_cheak_box_var = tk.IntVar()
title_lable = tk.Label(master=window,text='Import Picture',font=('Bold',20))
title_lable.pack()
import_pic_button = tk.Button(master=window,text='Upload',command=import_pic)
import_pic_button.pack()
scale_lable = tk.Label(master=window,text='Scale :')
scale_lable.place(x=120,y=440)
shape_line_cheak_box = tk.Checkbutton(master=window,text='Shape Line',variable=shape_line_cheak_box_var)
shape_line_cheak_box.place(x=170,y=460)
drawing_lines_cheak_box = tk.Checkbutton(master=window,text='Drawing Line(For Upscale(Color),To SGV and To PDF)',variable=drawing_lines_cheak_box_var)
drawing_lines_cheak_box.place(x=260,y=460)
scale_entry = tk.Entry(master=window)
scale_entry.place(x=160,y=440)
save_filename_lable = tk.Label(master=window,text='Filename :')
save_filename_lable.place(x=290,y=440)
save_filename_entry = tk.Entry(master=window)
save_filename_entry.place(x=350,y=440)
stl_convert_button = tk.Button(master=window,text='To STL(3D)',command=stl_convert,width=12,height=7)
stl_convert_button.place(x=600 - 110,y=483)
sgv_convert_button = tk.Button(master=window,text='To SVG',command=sgv_convert,width=12,height=7)
sgv_convert_button.place(x=505 - 110,y=483)
pdf_convert_button = tk.Button(master=window,text='To PDF',command=pdf_convert,width=12,height=7)
pdf_convert_button.place(x=410 - 110,y=483)
dxf_convert_button = tk.Button(master=window,text='To DXF',command=dxf_convert,width=12,height=7)
dxf_convert_button.place(x=315 - 110,y=483)
up_scale_line_convert_button = tk.Button(master=window,text='Upscale' + '\n' + '(Line Only)',command=Upscale_line,width=12,height=7)
up_scale_line_convert_button.place(x=220 - 110,y=483)
up_scale_color_convert_button = tk.Button(master=window,text='Upscale(Color)',command=Upscale_color,width=12,height=7)
up_scale_color_convert_button.place(x=125 - 110,y=483)

window.mainloop()