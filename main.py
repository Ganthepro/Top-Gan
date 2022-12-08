"""COPYRIGHT © Tamtikorn 2022. All Right Reserved."""
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import ezdxf as dxf
import svgwrite as svg
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageTk
from stl import mesh
import os
import math

window = tk.Tk()
window.title('Top Gan')
window.minsize(width=600, height=600)
window.maxsize(width=600, height=600)

filename_history = ['']
bg_color = [255, 255, 254]
for_return = [False]


def status(*loading):
    title_lable.configure(text=str(loading))


def stop():
    for_return[0] = True


def import_pic():
    global image
    filename = filedialog.askopenfilename()
    try:
        img = Image.open(filename)
    except:
        return
    img = img.convert('RGBA')
    wx, hy = img.size
    print(wx*hy)
    img = img.resize((300, 300))
    if filename_history[0] == '':
        filename_history[0] = filename
        image = ImageTk.PhotoImage(img)
    elif filename_history[0] != '' and filename_history[0] != filename:
        filename_history[0] = filename
        image = ImageTk.PhotoImage(img)
        print('Selected:', filename)
    #image = ImageTk.PhotoImage(file=filename, width=size[0],wall_height=size[1])
    image_lable = tk.Label(master=window, image=image)
    image_lable.place(x=150, y=80)
    
def sgv_convert():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_apply.place_forget()
    gcode_apply.place_forget()
    stl_base_wall_height.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_convert_button.configure(command=stl_convert1)
    dwg = svg.Drawing(str(save_filename_entry.get()) + '.svg', profile='tiny')
    filename = filename_history[0]
    try:
        img = Image.open(filename)
    except:
        return
    img = img.convert('RGBA')
    cv_img = np.array(img)
    img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    wx, hy = img.size
    px = img.load()
    xshift = 0
    yshift = -1
    #scale = int(scale_entry.get())
    scale = math.ceil(float(scale_entry.get()))
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    im = Image.new('RGBA', (wx * scale, hy * scale),
                   (bg_color[0], bg_color[1], bg_color[2], 255))
    sx, sy, ex, ey = 1, 2, 3, 4
    r, g, b = 2, 1, 0
    resize = img.resize((wx * scale, hy * scale))
    n_wx, n_hy = resize.size
    vec = []
    RGB = []
    colors = []
    idx = -1
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
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, y * scale, (x + 1)
                               * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append([idx - 1, (x + 1) * scale, y * scale,
                                       (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, (y + 1) * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                    pass
                elif px[x, y] != f and px[x, y] != c:
                    pass
                elif px[x, y] != e and px[x, y] == b:
                    if px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   x * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, (x + 1) * scale, y * scale,
                                   (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
                dwg.add(dwg.rect((x * scale, y * scale), (0.05, 0.05),
                        stroke=svg.rgb(red, green, blue, 'RGB')))
        n_vec = []
        semi_vec = []
        for k,n in enumerate(vec):
            for i in vec:
                if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
                    semi_vec.append(n)
                    semi_vec.append(i)
                    n_vec.append(
                        [n[0], n[sx], n[sy], n[ex] - math.ceil(scale / 2), n[ey] + math.ceil(scale / 2)])
                    n_vec.append([i[0], i[sx] + math.ceil(scale / 2),
                                 i[sy] + math.ceil(scale / 2), i[ex], i[ey]])
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(text = 'loading ' + "{:.2f}".format(0 + ((k * 25) / len(vec))) + ' %')
            window.update()
        for i in vec:
            if i in semi_vec:
                pass
            else:
                n_vec.append(i)
        vec = n_vec
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x * scale, y * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale,
                               (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
                dwg.add(dwg.rect((x * scale, y * scale), (0.05, 0.05),
                        stroke=svg.rgb(red, green, blue, 'RGB')))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 25%')
    window.update()
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
        draw.line(((i[sx]), (i[sy]) + yshift * scale, (i[ex]),
                  (i[ey]) + yshift * scale), fill=(0,0,1, 255))
    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (0,0,1, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 50%')
    window.update()
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (0,0,1, 255):
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
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (0,0,1, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (0,0,1, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] == (0,0,1, 255):
                # print(x, y)
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (0,0,1, 255):
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
    # im.show()
    id1 = 0
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
                    dwg.add(dwg.line((0, y), ((0 + id1), y), stroke=svg.rgb(
                        px_im[0, y][0], px_im[0, y][1], px_im[0, y][2], 'RGB'), stroke_width=2))
                    #print((start_p_1[0] + id1) / 10)
                    id1 = 0
                    # จะมีต่ำแหน่งที่ไม่มีสีอยู่ให้ใช้ pass
    id = 1
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
                    dwg.add(dwg.line((start_p[0], start_p[1]), ((start_p[0] + id), start_p[1]),
                                     stroke=svg.rgb(px_im[start_p[0], start_p[1]][0], px_im[start_p[0], start_p[1]][1],
                                                    px_im[start_p[0], start_p[1]][2], 'RGB'), stroke_width=2))
                    id = 1
                    start_p[0] = x
                    start_p[1] = y
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 75%')
    window.update()
    """สร้างปุ่มยกเลิกระหว่างทำงาน"""
    if drawing_lines_cheak_box_var.get() == 0:
        if shape_line_cheak_box_var.get() == 1:
            count_1 = 0
            for y in range(0, n_hy):
                for x in range(0, n_wx):
                    for i in vec:
                        if x == (i[ex]) + xshift and y == (i[ey] - 1):
                            # print((((i[sx] * scale) + xshift, (i[sy] * scale))), ((i[ex] * scale) + xshift, (i[ey] * scale)))
                            dwg.add(dwg.line(((i[sx]), (i[sy] - (1 * scale))), ((i[ex]), (i[ey] - (1 * scale))),
                                             stroke=svg.rgb(px_im[(i[ex]), i[ey] - 1][0], px_im[(i[ex]), i[ey] - 1][1], px_im[(i[ex]) + xshift,  i[ey] - 1][2], 'RGB'), stroke_width=2.5))
                            count_1 += 1
                a_float = float(((25 * y) / n_hy) + 75)
                if for_return[0] == True:
                    title_lable.configure(text='Import Picture')
                    stop_button.place_forget()
                    for_return[0] = False
                    return
                title_lable.configure(
                    text='loading ' + "{:.2f}".format(a_float) + '%')
                window.update()
    else:
        for i in vec:
            #print(((i[sx] * scale) + xshift, (i[sy] * scale) + (yshift - 2)), ((i[ex] * scale) + xshift, (i[ey] * scale) + (yshift - 2)))
            dwg.add(dwg.line(((i[sx]) + xshift + 1, (i[sy]) + (yshift - scale)), ((i[ex]) + xshift +
                    1, (i[ey]) + (yshift - scale)), stroke=svg.rgb(0, 255, 0, 'RGB'), stroke_width=1.5))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    cv_img = np.array(img)
    image_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    #cv2.imwrite('test.png', image_cv2)
    dwg.save()
    title_lable.configure(text='Import Picture')
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def pdf_convert():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_apply.place_forget()
    gcode_apply.place_forget()
    stl_base_wall_height.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_convert_button.configure(command=stl_convert1)
    filename = filename_history[0]
    try:
        img = Image.open(filename)
    except:
        return
    img = img.convert('RGBA')
    cv_img = np.array(img)
    img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    wx, hy = img.size
    px = img.load()
    pdf = FPDF()
    pdf.add_page('L')
    sx, sy, ex, ey = 1, 2, 3, 4
    pic_xshift = 0
    pic_yshift = -1
    #scale = int(scale_entry.get())
    scale = math.ceil(float(scale_entry.get()))
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    vec = []
    RGB = []
    bg_color = [0, 0, 1]
    idx = -1
    resize = img.resize((wx * scale, hy * scale))
    n_wx, n_hy = resize.size
    im = Image.new('RGBA', (wx * scale, hy * scale),
                   (bg_color[0], bg_color[1], bg_color[2], 255))
    colors = []
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
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
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
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append(
                            [idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
    px_im = im.load()
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
        draw.line(((i[sx] * scale) + pic_xshift * scale, (i[sy] * scale) + pic_yshift * scale, (i[ex]
                  * scale) + pic_xshift * scale, (i[ey] * scale) + pic_yshift * scale), fill=(0, 255, 0, 255))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return  # แก้ต่อ
    title_lable.configure(text='loading 25%')
    window.update()
    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (0, 255, 0, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 45%')
    window.update()
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (0, 255, 0, 255):
                im.putpixel((x, y), (f[0], f[1], f[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 60%')
    window.update()
    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != e and e != (0, 255, 0, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 75%')
    window.update()
    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (0, 255, 0, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 85%')
    window.update()
    for y in range(n_hy):
        for x in range(n_wx):
            if x - 1 < 0:  # ซ้าย
                e = px_im[x, y]
            else:
                e = px_im[x - 1, y]
            if px_im[x, y] == (0, 255, 0, 255):
                # print(x, y)
                im.putpixel((x, y), (e[0], e[1], e[2]))

    for y in range(n_hy):
        for x in range(n_wx):
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (0, 255, 0, 255):
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
                    # print(id1)
                    pdf.line(0 / 10, y / 10, (0 + id1) / 10, y / 10)
                    # pdf.line(0 / 10, y, (0 + id1), y)
                    # print((start_p_1[0] + id1) / 10)
                    pdf.set_line_width(0.2)
                    pdf.set_draw_color(
                        px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                    id1 = 0
                    break
    print(wx, hy)
    print(n_wx, n_hy)
    id = 0
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
                elif px_im[x, y] != e:
                    # print('1.', start_p)
                    # print('2.', id)
                    pdf.line(start_p[0] / 10, start_p[1] / 10,
                             (start_p[0] + id) / 10, start_p[1] / 10)
                    # pdf.line(start_p[0], start_p[1], (start_p[0] + id), start_p[1])
                    pdf.set_line_width(0.23)
                    pdf.set_draw_color(
                        px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                    # print('3.',start_p[0]+id)
                    id = 0
                    start_p[0] = x
                    start_p[1] = y
    if drawing_lines_cheak_box_var.get() == 1:
        if shape_line_cheak_box_var.get() == 1:
            vec2 = []
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
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec2.append(
                            [idx - 1, x * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                    elif px[x, y] == e:
                        if px[x, y] != b:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec2.append(
                                [idx - 1, x * scale, y * scale, (x + 1) * scale, y * scale, idx + 1, 0])
                    elif px[x, y] == b:
                        if px[x, y] != c:
                            if px[x, y] == j:
                                pass
                            else:
                                idx += 1
                                # [prev,sx,sy,ex,ey,next,status]
                                vec2.append(
                                    [idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                    if px[x, y] != b and px[x, y] != e:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec2.append(
                            [idx - 1, x * scale, (y + 1) * scale, (x + 1) * scale, y * scale, idx + 1, 0])
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
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec2.append(
                                [idx - 1, x * scale, y * scale, x * scale, (y + 1) * scale, idx + 1, 0])
                    elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec2.append([idx - 1, (x + 1) * scale, y * scale,
                                        (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
            n_vec = []
            semi_vec = []
            for k,n in enumerate(vec2):
                for i in vec2:
                    if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
                        # n_vec.append(n)/
                        # n_vec.append(i)\
                        semi_vec.append(n)
                        semi_vec.append(i)
                        n_vec.append(
                            [n[0], n[sx], n[sy], n[ex] - math.ceil(scale / 2), n[ey] + math.ceil(scale / 2)])
                        n_vec.append(
                            [i[0], i[sx] + math.ceil(scale / 2), i[sy] + math.ceil(scale / 2), i[ex], i[ey]])
                if for_return[0] == True:
                    title_lable.configure(text='Import Picture')
                    stop_button.place_forget()
                    for_return[0] = False
                    return
                title_lable.configure(text = 'loading ' + "{:.2f}".format(85 + ((k * 15) / len(vec2))) + ' %')
                window.update()
            for i in vec2:
                if i in semi_vec:
                    pass
                else:
                    n_vec.append(i)
            vec2 = n_vec
            for i in vec2:
                pdf.line((i[sx]) / 10, ((i[sy] - scale)) / 10,
                         (i[ex]) / 10, ((i[ey] - scale)) / 10)
                pdf.set_draw_color(0, 255, 0)
        else:
            for i in vec:
                pdf.line((i[sx] * scale) / 10, ((i[sy] - 1) * scale) /
                         10, (i[ex] * scale) / 10, ((i[ey] - 1) * scale) / 10)
                pdf.set_draw_color(0, 255, 0)
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    # im.show()
    # pdf.set_fill_color(255,255,0)
    # im.show('test.png')
    pdf.output(str(save_filename_entry.get()) + ".pdf")
    title_lable.configure(text='Import Picture')
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def dxf_convert():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_apply.place_forget()
    gcode_apply.place_forget()
    stl_base_wall_height.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_convert_button.configure(command=stl_convert1)
    doc = dxf.new('R2010')
    msp = doc.modelspace()
    filename = filename_history[0]
    if scale_entry.get() == '' or save_filename_entry.get() == '':return
    try:
        img = Image.open(filename)
    except:
        return
    img = img.convert('RGBA')
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
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
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
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
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(text = 'loading ' + "{:.2f}".format(0 + ((y * 50) / hy)) + ' %');window.update() 
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 50%')
    window.update()
    sx, sy, ex, ey = 1, 2, 3, 4

    for i in vec:
        msp.add_line((i[sx], i[sy]), (i[ex], i[ey]))
    doc.saveas(str(save_filename_entry.get()) + '.dxf')
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    title_lable.configure(text='Import Picture')
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def Upscale_line():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_apply.place_forget()
    gcode_apply.place_forget()
    stl_base_wall_height.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_convert_button.configure(command=stl_convert1)

    img = Image.open(filename_history[0])
    img = img.convert('RGBA')
    print(scale_entry.get(), save_filename_entry.get())
    wx, hy = img.size
    px = img.load()
    cv_img = np.array(img)
    img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    # window = Tk()
    xshift = 0
    yshift = -1
    #scale = int(scale_entry.get())
    scale = math.ceil(float(scale_entry.get()))
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    im = Image.new('RGBA', (wx * scale, hy * scale),
                   (bg_color[0], bg_color[1], bg_color[2], 255))
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
                if y - 1 < 0:
                    b = px[x, y]
                else:
                    b = px[x, y - 1]
                if x + 1 == wx:
                    c = px[x, y]
                else:
                    c = px[x + 1, y]
                if px[x, y] != b:
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x * scale, y * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale,
                               (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
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
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, y * scale, (x + 1)
                               * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append([idx - 1, (x + 1) * scale, y * scale,
                                       (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, (y + 1) * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                    pass
                elif px[x, y] != f and px[x, y] != c:
                    pass
                elif px[x, y] != e and px[x, y] == b:
                    if px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   x * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, (x + 1) * scale, y * scale,
                                   (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
        n_vec = []
        semi_vec = []
        for k,n in enumerate(vec):
            for i in vec:
                if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
                    semi_vec.append(n)
                    semi_vec.append(i)
                    n_vec.append(
                        [n[0], n[sx], n[sy], n[ex] - math.ceil(scale / 2), n[ey] + math.ceil(scale / 2)])
                    n_vec.append([i[0], i[sx] + math.ceil(scale / 2),
                                 i[sy] + math.ceil(scale / 2), i[ex], i[ey]])
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(text = 'loading ' + "{:.2f}".format(0 + ((k * 100) / len(vec))) + ' %')
            window.update()
        for i in vec:
            if i in semi_vec:
                pass
            else:
                n_vec.append(i)
        vec = n_vec
    title_lable.configure(text='loading 50%')
    draw = ImageDraw.Draw(im)
    for i in vec:
        draw.line(((i[sx]), (i[sy]), (i[ex]), (i[ey])), fill=(0,0,1, 255))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    cv_img = np.array(img)
    image_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    im.show(str(save_filename_entry.get()) + '.png')
    im.save(str(save_filename_entry.get()) + '.png')
    #cv2.imwrite(str(save_filename_entry.get()) + '.png', image_cv2)
    title_lable.configure(text='Import Picture')
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def Upscale_color():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_apply.place_forget()
    gcode_apply.place_forget()
    stl_base_wall_height.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_convert_button.configure(command=stl_convert1)
    print(filename_history[0])
    img = Image.open(filename_history[0])
    img = img.convert('RGBA')
    wx, hy = img.size
    px = img.load()
    cv_img = np.array(img)
    img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    xshift = 0
    yshift = -1
    #scale = int(scale_entry.get())
    scale = math.ceil(float(scale_entry.get()))
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    im = Image.new('RGBA', (wx * scale, hy * scale),
                   (bg_color[0], bg_color[1], bg_color[2], 255))
    sx, sy, ex, ey = 1, 2, 3, 4
    r, g, b = 2, 1, 0
    resize = img.resize((wx * scale, hy * scale))
    n_wx, n_hy = resize.size
    vec = []
    RGB = []
    colors = []
    idx = -1
    n_vec = []
    semi_vec = []
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x * scale, y * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    vec.append([idx - 1, (x + 1) * scale, y * scale, (x + 1) * scale,
                               (y + 1) * scale, idx + 1, 0])  # [prev,sx,sy,ex,eyo,next,status]
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
    elif shape_line_cheak_box_var.get() == 1:
        """แก้ต่อ"""
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
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, y * scale, (x + 1)
                               * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append([idx - 1, (x + 1) * scale, y * scale,
                                       (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x * scale, (y + 1) * scale,
                               (x + 1) * scale, y * scale, idx + 1, 0])
                elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                    pass
                elif px[x, y] != f and px[x, y] != c:
                    pass
                elif px[x, y] != e and px[x, y] == b:
                    if px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x * scale, y * scale,
                                   x * scale, (y + 1) * scale, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, (x + 1) * scale, y * scale,
                                   (x + 1) * scale, (y + 1) * scale, idx + 1, 0])
                RGB.append([red, green, blue])
                im.putpixel((x * scale, y * scale), (red, green, blue))
        for k,n in enumerate(vec):
            for i in vec:
                if n[sx] == i[sx] and n[sy] - i[sy] == scale and n[ex] == i[ex] and i[ey] - n[ey] == scale:
                    semi_vec.append(n)  # /
                    semi_vec.append(i)  # \
                    n_vec.append(
                        [n[0], n[sx], n[sy], n[ex] - math.ceil(scale / 2), n[ey] + math.ceil(scale / 2)])
                    n_vec.append([i[0], i[sx] + math.ceil(scale / 2),
                                 i[sy] + math.ceil(scale / 2), i[ex], i[ey]])
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(text = 'loading ' + "{:.2f}".format(0 + ((k * 25) / len(vec))) + ' %')
            window.update()
        for i in vec:
            if i in semi_vec:
                pass
            else:
                n_vec.append(i)
        vec = n_vec
    px_im = im.load()
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
        draw.line(((i[sx]), (i[sy]) + (yshift * scale), (i[ex]),
                  (i[ey]) + (yshift * scale)), fill=(0,0,1, 255))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 25%')
    window.update()
    for y in range(n_hy):
        for x in range(n_wx):
            color = px_im[x, y]
            colors.append(color)
            if y - 1 < 0:  # บน
                b = px_im[x, y]
            else:
                b = px_im[x, y - 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != b and b != (
                    0, 0, 1, 255):
                im.putpixel((x, y), (b[0], b[1], b[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 45%')
    window.update()
    for y in reversed(range(n_hy)):
        for x in range(n_wx):
            if y + 1 >= n_hy:  # ล่าง
                f = px_im[x, y]
            else:
                f = px_im[x, y + 1]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != f and f != (
                    0,0,1, 255):
                im.putpixel((x, y), (f[0], f[1], f[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 60%')
    window.update()
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
                    0,0,1, 255):
                im.putpixel((x, y), (e[0], e[1], e[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 75%')
    window.update()
    for y in range(n_hy):
        for x in reversed(range(n_wx)):
            if x + 1 == n_wx:  # ขวา
                c = px_im[x, y]
            else:
                c = px_im[x + 1, y]
            if px_im[x, y] == (bg_color[0], bg_color[1], bg_color[2], 255) and px_im[x, y] != c and c != (
                    0,0,1, 255):
                im.putpixel((x, y), (c[0], c[1], c[2]))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 85%')
    window.update()
    if drawing_lines_cheak_box_var.get() == 0:
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] == (0,0,1, 255):
                    #print(x, y)
                    im.putpixel((x, y), (e[0], e[1], e[2]))

        for y in range(n_hy):
            for x in range(n_wx):
                if y - 1 < 0:  # บน
                    b = px_im[x, y]
                else:
                    b = px_im[x, y - 1]
                if px_im[x, y] == (0,0,1, 255):
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
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    cv_img = np.array(img)
    image_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    im.show(str(save_filename_entry.get()) + '.png')
    im.save(str(save_filename_entry.get()) + '.png')
    #cv2.imwrite(str(save_filename_entry.get()) + '.png', image_cv2)
    title_lable.configure(text='Import Picture')
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def stl_convert_2():
    # HT19-C00514-NHU036814-2SAM_CARVE.tif #H20-C00175-11S190500-04-sample.tif
    filename = filename_history[0]
    try:
        img = Image.open(filename)
    except:
        return
    img = img.convert('RGBA')
    wx, hy = img.size
    px = img.load()
    scale = 1
    sx, sy, ex, ey = 1, 2, 3, 4
    r, g, b = 2, 1, 0
    resize = img.resize((wx * scale, hy * scale))
    n_wx, n_hy = resize.size
    vec = []
    idx = -1
    stl_scale = float(scale_entry.get())
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    im = Image.new('RGBA', (wx*scale, hy*scale),
                   (bg_color[0], bg_color[1], bg_color[2], 255))
    if int(shape_line_cheak_box_var.get()) == 1:
        for y in range(hy):
            for x in range(wx):
                if y-1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y-1]
                if x+1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x+1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y-1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x-1, y]
                if y+1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y+1]
                if y+1 == hy:
                    g = px[x, y]
                elif x+1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x+1, y+1]
                if y+1 == hy:
                    h = px[x, y]
                elif x-1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x-1, y+1]
                if y-1 < 0:
                    j = px[x, y]
                elif x+1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x+1, y-1]
                if y-1 < 0:
                    k = px[x, y]
                elif x-1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x-1, y-1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
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
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
    elif int(shape_line_cheak_box_var.get()) == 0:
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
    draw = ImageDraw.Draw(im)
    for i in vec:
        draw.line(((i[sx]*scale)+0*scale, (i[sy]*scale)+0*scale, (i[ex]
                  * scale)+0*scale, (i[ey]*scale)+0*scale), fill=(0, 255, 0, 255))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 25%')
    window.update()
    multi_vertices = []
    faces = []
    loop = 0
    base_wall_height = float(stl_base_wall_height.get())
    wall_wall_height = float(stl_wall_height.get())
    wall_thickness = float(stl_width.get())
    for k, i in enumerate(vec):
        if i[sy] == i[ey]:
            p1 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] *
                  scale / 1 * stl_scale + 20, base_wall_height]  # ---
            p2 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] *
                  scale / 1 * stl_scale + 20, base_wall_height]  # +--
            p3 = [i[ex] * scale / 1 * stl_scale + 20, (i[ey] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height]  # ++-
            p4 = [i[sx] * scale / 1 * stl_scale + 20, (i[sy] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height]  # -+-
            p5 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] * scale / 1 * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # --+
            p6 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] * scale / 1 * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # +-+
            p7 = [i[ex] * scale / 1 * stl_scale + 20, (i[ey] * scale / 1 * stl_scale) + wall_thickness + 20,
                  base_wall_height + wall_wall_height]  # +++
            p8 = [i[sx] * scale / 1 * stl_scale + 20, (i[sy] * scale / 1 * stl_scale) + wall_thickness + 20,
                  base_wall_height + wall_wall_height]  # -++
            vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
            face1_1 = np.array([p1, p4, p2])
            face1_2 = np.array([p2, p4, p3])
            face2_1 = np.array([p1, p5, p8])
            face2_2 = np.array([p1, p8, p4])
            face3_1 = np.array([p5, p6, p7])
            face3_2 = np.array([p5, p7, p8])
            face4_1 = np.array([p6, p2, p3])
            face4_2 = np.array([p6, p3, p7])
            face5_1 = np.array([p3, p4, p7])
            face5_2 = np.array([p4, p8, p7])
            face6_1 = np.array([p1, p2, p6])
            face6_2 = np.array([p1, p6, p5])
            multi_vertices.append(vertices)
            faces.append(face1_1)
            faces.append(face1_2)
            faces.append(face2_1)
            faces.append(face2_2)
            faces.append(face3_1)
            faces.append(face3_2)
            faces.append(face4_1)
            faces.append(face4_2)
            faces.append(face5_1)
            faces.append(face5_2)
            faces.append(face6_1)
            faces.append(face6_2)
            loop += 1
            vec.pop(vec.index(i))
            e = float(25 + ((k / len(vec)) * 25))
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(text='loading ' + '{:.2f}'.format(e) + '%')
            window.update()
    for k, i in enumerate(vec):
        if i[sx] == i[ex]:
            p1 = [(i[sx] * scale / 1) * stl_scale + 20, (i[sy] * scale / 1) * stl_scale + 20,
                  base_wall_height]  # ---
            p2 = [(i[sx] * scale / 1) * stl_scale + wall_thickness + 20, (i[sy] * scale / 1) * stl_scale + 20,
                  base_wall_height]  # +--
            p3 = [(i[ex] * scale / 1) * stl_scale + wall_thickness + 20,
                  (i[ey] * scale / 1) * stl_scale + wall_thickness + 20, base_wall_height]  # ++-
            p4 = [(i[ex] * scale / 1) * stl_scale + 20, (i[ey] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height]  # -+-
            p5 = [(i[sx] * scale / 1) * stl_scale + 20, (i[sy] * scale / 1) * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # --+
            p6 = [(i[sx] * scale / 1) * stl_scale + wall_thickness + 20, (i[sy] * scale / 1) * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # +-+
            p7 = [(i[ex] * scale / 1) * stl_scale + wall_thickness + 20,
                  (i[ey] * scale / 1) * stl_scale + wall_thickness + 20, base_wall_height + wall_wall_height]  # +++
            p8 = [(i[ex] * scale / 1) * stl_scale + 20, (i[ey] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height + wall_wall_height]  # -++
            vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
            face1_1 = np.array([p1, p4, p2])
            face1_2 = np.array([p2, p4, p3])
            face2_1 = np.array([p1, p5, p8])
            face2_2 = np.array([p1, p8, p4])
            face3_1 = np.array([p5, p6, p7])
            face3_2 = np.array([p5, p7, p8])
            face4_1 = np.array([p6, p2, p3])
            face4_2 = np.array([p6, p3, p7])
            face5_1 = np.array([p3, p4, p7])
            face5_2 = np.array([p4, p8, p7])
            face6_1 = np.array([p1, p2, p6])
            face6_2 = np.array([p1, p6, p5])
            multi_vertices.append(vertices)
            faces.append(face1_1)
            faces.append(face1_2)
            faces.append(face2_1)
            faces.append(face2_2)
            faces.append(face3_1)
            faces.append(face3_2)
            faces.append(face4_1)
            faces.append(face4_2)
            faces.append(face5_1)
            faces.append(face5_2)
            faces.append(face6_1)
            faces.append(face6_2)
        else:
            p1 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] *
                  scale / 1 * stl_scale + 20, base_wall_height]  # ---
            p2 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] *
                  scale / 1 * stl_scale + 20, base_wall_height]  # +--
            p3 = [i[ex] * scale / 1 * stl_scale + 20, (i[ey] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height]  # ++-
            p4 = [i[sx] * scale / 1 * stl_scale + 20, (i[sy] * scale / 1) * stl_scale + wall_thickness + 20,
                  base_wall_height]  # -+-
            p5 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] * scale / 1 * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # --+
            p6 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] * scale / 1 * stl_scale + 20,
                  base_wall_height + wall_wall_height]  # +-+
            p7 = [i[ex] * scale / 1 * stl_scale + 20, (i[ey] * scale / 1 * stl_scale) + wall_thickness + 20,
                  base_wall_height + wall_wall_height]  # +++
            p8 = [i[sx] * scale / 1 * stl_scale + 20, (i[sy] * scale / 1 * stl_scale) + wall_thickness + 20,
                  base_wall_height + wall_wall_height]  # -++
            vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
            face1_1 = np.array([p1, p4, p2])
            face1_2 = np.array([p2, p4, p3])
            face2_1 = np.array([p1, p5, p8])
            face2_2 = np.array([p1, p8, p4])
            face3_1 = np.array([p5, p6, p7])
            face3_2 = np.array([p5, p7, p8])
            face4_1 = np.array([p6, p2, p3])
            face4_2 = np.array([p6, p3, p7])
            face5_1 = np.array([p3, p4, p7])
            face5_2 = np.array([p4, p8, p7])
            face6_1 = np.array([p1, p2, p6])
            face6_2 = np.array([p1, p6, p5])
            multi_vertices.append(vertices)
            faces.append(face1_1)
            faces.append(face1_2)
            faces.append(face2_1)
            faces.append(face2_2)
            faces.append(face3_1)
            faces.append(face3_2)
            faces.append(face4_1)
            faces.append(face4_2)
            faces.append(face5_1)
            faces.append(face5_2)
            faces.append(face6_1)
            faces.append(face6_2)
            loop += 1
            e = float(50 + ((k / len(vec)) * 25))
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='loading ' + '{:.2f}'.format(e) + '%')
        window.update()
    p1 = [19, 20, 0]  # ---
    p2 = [(n_wx * stl_scale) + 20, 20, 0]  # +--
    p3 = [(n_wx * stl_scale) + 20, (n_hy * stl_scale) + 21, 0]  # ++-
    p4 = [19, (n_hy * stl_scale) + 21, 0]  # -+-
    p5 = [19, 20, base_wall_height]  # --+
    p6 = [(n_wx * stl_scale) + 20, 20, base_wall_height]  # +-+
    p7 = [(n_wx * stl_scale) + 20, (n_hy * stl_scale) +
          21, base_wall_height]  # +++
    p8 = [19, (n_hy * stl_scale) + 21, base_wall_height]  # -++
    face1_1 = np.array([p1, p4, p2])
    face1_2 = np.array([p2, p4, p3])
    face2_1 = np.array([p1, p5, p8])
    face2_2 = np.array([p1, p8, p4])
    face3_1 = np.array([p5, p6, p7])
    face3_2 = np.array([p5, p7, p8])
    face4_1 = np.array([p6, p2, p3])
    face4_2 = np.array([p6, p3, p7])
    face5_1 = np.array([p3, p4, p7])
    face5_2 = np.array([p4, p8, p7])
    face6_1 = np.array([p1, p2, p6])
    face6_2 = np.array([p1, p6, p5])
    faces.append(face1_1)
    faces.append(face1_2)
    faces.append(face2_1)
    faces.append(face2_2)
    faces.append(face3_1)
    faces.append(face3_2)
    faces.append(face4_1)
    faces.append(face4_2)
    faces.append(face5_1)
    faces.append(face5_2)
    faces.append(face6_1)
    faces.append(face6_2)
    print(wx, hy)
    print('vec : ', len(vec))
    print('loop1 : ', loop)
    loop = 0
    multi_vertices_np = np.array(faces)
    surface = mesh.Mesh(
        np.zeros(multi_vertices_np.shape[0], dtype=mesh.Mesh.dtype))
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    for i, f in enumerate(faces):
        for j in range(3):
            surface.vectors[i][j] = multi_vertices_np[i][j]
            # print(multi_vertices_np[i][j])
    im.show()
    surface.save(str(save_filename_entry.get()) + '.stl')
    title_lable.configure(text='Import Picture')
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_base_wall_height.place_forget()
    stl_apply.place_forget()
    gcode_apply.place_forget()
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stop_button.place_forget()


def real_pic_stl2():
    try:
        size_input = 5
        img = Image.open(filename_history[0])
        if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
            stop_button.place(x=400, y=20)
        else:
            return
        img = img.convert('RGBA')
        cv_img = np.array(img)
        img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        if size_input % 2 != 1:
            size_input += 1
        resize = cv2.resize(img, (size_input*100, size_input*100))
        gray = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, int(threshold_entry.get()), 3)
        color = cv2.cvtColor(adaptive, cv2.COLOR_BGR2RGB)
        color[np.where((color == [0, 0, 0]).all(axis=2))] = [0, 0, 255]
        color[np.where((color == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
        pil = Image.fromarray(color)
        bg_color = [0, 0, 1]
        img = pil
        wx, hy = img.size
        px = img.load()
        scale = 1
        sx, sy, ex, ey = 1, 2, 3, 4
        r, g, b = 2, 1, 0
        resize = img.resize((wx*scale, hy*scale))
        n_wx, n_hy = resize.size
        vec = []
        idx = -1
        im = Image.new('RGBA', (wx*scale, hy*scale),
                       (bg_color[0], bg_color[1], bg_color[2], 255))
        count = 0
        for y in range(hy):
            for x in range(wx):
                if y-1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y-1]
                if x+1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x+1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y-1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x-1, y]
                if y+1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y+1]
                if y+1 == hy:
                    g = px[x, y]
                elif x+1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x+1, y+1]
                if y+1 == hy:
                    h = px[x, y]
                elif x-1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x-1, y+1]
                if y-1 < 0:
                    j = px[x, y]
                elif x+1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x+1, y-1]
                if y-1 < 0:
                    k = px[x, y]
                elif x-1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x-1, y-1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
                elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                    pass
                elif px[x, y] != f and px[x, y] != c:
                    pass
                elif px[x, y] != e and px[x, y] == b:
                    if px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
                count += 1
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format((count * 25) / (hy * wx)) + ' %')
            window.update()
        draw = ImageDraw.Draw(im)
        for i in vec:
            draw.line(((i[sx]*scale)+0*scale, (i[sy]*scale)+0*scale, (i[ex]
                      * scale)+0*scale, (i[ey]*scale)+0*scale), fill=(0, 255, 0, 255))
        multi_vertices = []
        faces = []
        loop = 0
        base_height = float(stl_base_wall_height.get())
        wall_height = float(stl_wall_height.get())
        wall_thickness = float(stl_width.get())
        stl_scale = float(scale_entry.get())
        count = 0
        for i in vec:
            if i[sy] == i[ey]:
                p1 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] *
                      scale / 1 * stl_scale + 20, base_height]  # ---
                p2 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] *
                      scale / 1 * stl_scale + 20, base_height]  # +--
                p3 = [i[ex] * scale / 1 * stl_scale + 20,
                      (i[ey] * scale / 1) * stl_scale + wall_thickness + 20, base_height]  # ++-
                p4 = [i[sx] * scale / 1 * stl_scale + 20,
                      (i[sy] * scale / 1) * stl_scale + wall_thickness + 20, base_height]  # -+-
                p5 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] * scale /
                      1 * stl_scale + 20, base_height + wall_height]  # --+
                p6 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] * scale /
                      1 * stl_scale + 20, base_height + wall_height]  # +-+
                p7 = [i[ex] * scale / 1 * stl_scale + 20,
                      (i[ey] * scale / 1 * stl_scale) + wall_thickness + 20, base_height + wall_height]  # +++
                p8 = [i[sx] * scale / 1 * stl_scale + 20,
                      (i[sy] * scale / 1 * stl_scale) + wall_thickness + 20, base_height + wall_height]  # -++
                vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
                face1_1 = np.array([p1, p4, p2])
                face1_2 = np.array([p2, p4, p3])
                face2_1 = np.array([p1, p5, p8])
                face2_2 = np.array([p1, p8, p4])
                face3_1 = np.array([p5, p6, p7])
                face3_2 = np.array([p5, p7, p8])
                face4_1 = np.array([p6, p2, p3])
                face4_2 = np.array([p6, p3, p7])
                face5_1 = np.array([p3, p4, p7])
                face5_2 = np.array([p4, p8, p7])
                face6_1 = np.array([p1, p2, p6])
                face6_2 = np.array([p1, p6, p5])
                multi_vertices.append(vertices)
                faces.append(face1_1)
                faces.append(face1_2)
                faces.append(face2_1)
                faces.append(face2_2)
                faces.append(face3_1)
                faces.append(face3_2)
                faces.append(face4_1)
                faces.append(face4_2)
                faces.append(face5_1)
                faces.append(face5_2)
                faces.append(face6_1)
                faces.append(face6_2)
                loop += 1
                vec.pop(vec.index(i))
                if for_return[0] == True:
                    title_lable.configure(text='Import Picture')
                    stop_button.place_forget()
                    for_return[0] = False
                    return
                title_lable.configure(
                    text='loading ' + "{:.2f}".format(25 + ((count * 25) / len(vec))) + ' %')
                window.update()
            count += 1
        count = 0
        for i in vec:
            if i[sx] == i[ex]:
                p1 = [(i[sx] * scale / 1) * stl_scale + 20, (i[sy] *
                                                             scale / 1) * stl_scale + 20, base_height]  # ---
                p2 = [(i[sx] * scale / 1) * stl_scale + wall_thickness + 20,
                      (i[sy] * scale / 1) * stl_scale + 20, base_height]  # +--
                p3 = [(i[ex] * scale / 1) * stl_scale + wall_thickness + 20, (i[ey]
                                                                              * scale / 1) * stl_scale + wall_thickness + 20, base_height]  # ++-
                p4 = [(i[ex] * scale / 1) * stl_scale + 20, (i[ey] * scale / 1)
                      * stl_scale + wall_thickness + 20, base_height]  # -+-
                p5 = [(i[sx] * scale / 1) * stl_scale + 20, (i[sy] * scale / 1)
                      * stl_scale + 20, base_height + wall_height]  # --+
                p6 = [(i[sx] * scale / 1) * stl_scale + wall_thickness + 20, (i[sy]
                                                                              * scale / 1) * stl_scale + 20, base_height + wall_height]  # +-+
                p7 = [(i[ex] * scale / 1) * stl_scale + wall_thickness + 20, (i[ey] * scale / 1)
                      * stl_scale + wall_thickness + 20, base_height + wall_height]  # +++
                p8 = [(i[ex] * scale / 1) * stl_scale + 20, (i[ey] * scale / 1) *
                      stl_scale + wall_thickness + 20, base_height + wall_height]  # -++
                vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
                face1_1 = np.array([p1, p4, p2])
                face1_2 = np.array([p2, p4, p3])
                face2_1 = np.array([p1, p5, p8])
                face2_2 = np.array([p1, p8, p4])
                face3_1 = np.array([p5, p6, p7])
                face3_2 = np.array([p5, p7, p8])
                face4_1 = np.array([p6, p2, p3])
                face4_2 = np.array([p6, p3, p7])
                face5_1 = np.array([p3, p4, p7])
                face5_2 = np.array([p4, p8, p7])
                face6_1 = np.array([p1, p2, p6])
                face6_2 = np.array([p1, p6, p5])
                multi_vertices.append(vertices)
                faces.append(face1_1)
                faces.append(face1_2)
                faces.append(face2_1)
                faces.append(face2_2)
                faces.append(face3_1)
                faces.append(face3_2)
                faces.append(face4_1)
                faces.append(face4_2)
                faces.append(face5_1)
                faces.append(face5_2)
                faces.append(face6_1)
                faces.append(face6_2)
            else:
                p1 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] *
                      scale / 1 * stl_scale + 20, base_height]  # ---
                p2 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] *
                      scale / 1 * stl_scale + 20, base_height]  # +--
                p3 = [i[ex] * scale / 1 * stl_scale + 20,
                      (i[ey] * scale / 1) * stl_scale + wall_thickness + 20, base_height]  # ++-
                p4 = [i[sx] * scale / 1 * stl_scale + 20,
                      (i[sy] * scale / 1) * stl_scale + wall_thickness + 20, base_height]  # -+-
                p5 = [i[sx] * scale / 1 * stl_scale + 20, i[sy] * scale /
                      1 * stl_scale + 20, base_height + wall_height]  # --+
                p6 = [i[ex] * scale / 1 * stl_scale + 20, i[ey] * scale /
                      1 * stl_scale + 20, base_height + wall_height]  # +-+
                p7 = [i[ex] * scale / 1 * stl_scale + 20,
                      (i[ey] * scale / 1 * stl_scale) + wall_thickness + 20, base_height + wall_height]  # +++
                p8 = [i[sx] * scale / 1 * stl_scale + 20,
                      (i[sy] * scale / 1 * stl_scale) + wall_thickness + 20, base_height + wall_height]  # -++
                vertices = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
                face1_1 = np.array([p1, p4, p2])
                face1_2 = np.array([p2, p4, p3])
                face2_1 = np.array([p1, p5, p8])
                face2_2 = np.array([p1, p8, p4])
                face3_1 = np.array([p5, p6, p7])
                face3_2 = np.array([p5, p7, p8])
                face4_1 = np.array([p6, p2, p3])
                face4_2 = np.array([p6, p3, p7])
                face5_1 = np.array([p3, p4, p7])
                face5_2 = np.array([p4, p8, p7])
                face6_1 = np.array([p1, p2, p6])
                face6_2 = np.array([p1, p6, p5])
                multi_vertices.append(vertices)
                faces.append(face1_1)
                faces.append(face1_2)
                faces.append(face2_1)
                faces.append(face2_2)
                faces.append(face3_1)
                faces.append(face3_2)
                faces.append(face4_1)
                faces.append(face4_2)
                faces.append(face5_1)
                faces.append(face5_2)
                faces.append(face6_1)
                faces.append(face6_2)
                loop += 1
            count += 1
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format(50 + ((count * 25) / len(vec))) + ' %')
            window.update()
        p1 = [19, 20, 0]  # ---
        p2 = [(n_wx * stl_scale) + 20, 20, 0]  # +--
        p3 = [(n_wx * stl_scale) + 20, (n_hy * stl_scale) + 21, 0]  # ++-
        p4 = [19, (n_hy * stl_scale) + 21, 0]  # -+-
        p5 = [19, 20, base_height]  # --+
        p6 = [(n_wx * stl_scale) + 20, 20, base_height]  # +-+
        p7 = [(n_wx * stl_scale) + 20,
              (n_hy * stl_scale) + 21, base_height]  # +++
        p8 = [19, (n_hy * stl_scale) + 21, base_height]  # -++
        face1_1 = np.array([p1, p4, p2])
        face1_2 = np.array([p2, p4, p3])
        face2_1 = np.array([p1, p5, p8])
        face2_2 = np.array([p1, p8, p4])
        face3_1 = np.array([p5, p6, p7])
        face3_2 = np.array([p5, p7, p8])
        face4_1 = np.array([p6, p2, p3])
        face4_2 = np.array([p6, p3, p7])
        face5_1 = np.array([p3, p4, p7])
        face5_2 = np.array([p4, p8, p7])
        face6_1 = np.array([p1, p2, p6])
        face6_2 = np.array([p1, p6, p5])
        faces.append(face1_1)
        faces.append(face1_2)
        faces.append(face2_1)
        faces.append(face2_2)
        faces.append(face3_1)
        faces.append(face3_2)
        faces.append(face4_1)
        faces.append(face4_2)
        faces.append(face5_1)
        faces.append(face5_2)
        faces.append(face6_1)
        faces.append(face6_2)
        loop = 0
        multi_vertices_np = np.array(faces)
        cube = mesh.Mesh(
            np.zeros(multi_vertices_np.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                cube.vectors[i][j] = multi_vertices_np[i][j]
                # print(multi_vertices_np[i][j])
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='loading 100%')
        window.update()
        cube.save(str(save_filename_entry.get()) + '.stl')
        im.show()
        title_lable.configure(text='Import Picture')
        stl_wall_height.place_forget()
        stl_wall_height_lable.place_forget()
        stl_width.place_forget()
        stl_width_lable.place_forget()
        stl_base_wall_height_lable.place_forget()
        stl_base_wall_height.place_forget()
        stl_apply.place_forget()
        gcode_apply.place_forget()
        threshold_entry.place_forget()
        threshold_lable.place_forget()
        scale_entry.place(x=160, y=440)
        scale_lable.place(x=120, y=440)
        save_filename_entry.place(x=350, y=440)
        save_filename_lable.place(x=290, y=440)
        stop_button.place_forget()

        # cv2.imwrite('test_cat.png',color)
        # cv2.imshow('morpho',morpho)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    except Exception as e:
        print(e)


def real_pic_stl1():
    stl_wall_height.place(x=85, y=415)
    stl_wall_height_lable.place(x=10, y=415)
    stl_width.place(x=270, y=415)
    stl_width_lable.place(x=175, y=415)
    scale_lable.configure(text='Scale :')
    scale_lable.place(x=5)
    scale_entry.place(x=45)
    stl_base_wall_height_lable.place(x=370, y=415)
    stl_base_wall_height.place(x=450, y=415)
    stl_apply.place(x=505, y=435)
    stl_apply.configure(command=real_pic_stl2)
    gcode_apply.place(x=543, y=435)
    gcode_apply.configure(command=gcode_convert2)
    threshold_lable.place(x=280, y=440)
    threshold_entry.place(x=375, y=440)
    save_filename_lable.configure(text='Filename :')
    save_filename_lable.place(x=170-40)
    save_filename_entry.place(x=230-40)


def stl_convert1():
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    scale_entry.place(x=160, y=440)
    scale_lable.place(x=120, y=440)
    save_filename_entry.place(x=350, y=440)
    save_filename_lable.place(x=290, y=440)
    stl_wall_height.place(x=85, y=415)
    stl_wall_height_lable.place(x=10, y=415)
    stl_width.place(x=270, y=415)
    stl_width_lable.place(x=175, y=415)
    scale_lable.configure(text='Scale :')
    scale_lable.place(x=100)
    stl_base_wall_height_lable.place(x=370, y=415)
    stl_base_wall_height.place(x=450, y=415)
    stl_apply.place(x=505, y=435)
    stl_apply.configure(command=stl_convert_2)
    gcode_apply.place(x=543, y=435)
    gcode_apply.configure(command=gcode_convert1)


def gcode_convert2():
    try:
        size_input = 5
        img = Image.open(filename_history[0])
        img = img.convert('RGBA')
        cv_img = np.array(img)
        img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        if size_input % 2 != 1:
            size_input += 1
        resize = cv2.resize(img, (size_input*100, size_input*100))
        gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, int(threshold_entry.get()), 7)
        color = cv2.cvtColor(adaptive, cv2.COLOR_BGR2RGB)
        color[np.where((color == [0, 0, 0]).all(axis=2))] = [0, 0, 255]
        color[np.where((color == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
        pil = Image.fromarray(color)
        img = pil
        wx, hy = img.size
        print(img.size)
        px = img.load()
        scale = 2
        im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 1, 255))
        sx, sy, ex, ey = 1, 2, 3, 4
        r, g, b = 2, 1, 0
        vec = []
        idx = -1
        scale = float(scale_entry.get())  # scale
        if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
            stop_button.place(x=400, y=20)
        else:
            return
        if int(shape_line_cheak_box_var.get()) == 1:
            for y in range(hy):
                for x in range(wx):
                    if y-1 < 0:  # บน
                        b = px[x, y]
                    else:
                        b = px[x, y-1]
                    if x+1 == wx:  # ขวา
                        c = px[x, y]
                    else:
                        c = px[x+1, y]
                    if y - 1 < 0:  # บน
                        d = px[x, y]
                    else:
                        d = px[x, y-1]
                    if x - 1 < 0:  # ซ้าย
                        e = px[x, y]
                    else:
                        e = px[x-1, y]
                    if y+1 >= hy:  # ล่าง
                        f = px[x, y]
                    else:
                        f = px[x, y+1]
                    if y+1 == hy:
                        g = px[x, y]
                    elif x+1 == wx:  # ล่างขวา
                        g = px[x, y]
                    else:
                        g = px[x+1, y+1]
                    if y+1 == hy:
                        h = px[x, y]
                    elif x-1 < 0:  # ล่างซ้าย
                        h = px[x, y]
                    else:
                        h = px[x-1, y+1]
                    if y-1 < 0:
                        j = px[x, y]
                    elif x+1 == wx:  # บนขวา
                        j = px[x, y]
                    else:
                        j = px[x+1, y-1]
                    if y-1 < 0:
                        k = px[x, y]
                    elif x-1 < 0:  # บนซ้าย
                        k = px[x, y]
                    else:
                        k = px[x-1, y-1]
                    if px[x, y] != b and px[x, y] != c:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                    elif px[x, y] == e:
                        if px[x, y] != b:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                    elif px[x, y] == b:
                        if px[x, y] != c:
                            if px[x, y] == j:
                                pass
                            else:
                                idx += 1
                                # [prev,sx,sy,ex,ey,next,status]
                                vec.append(
                                    [idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
                    if px[x, y] != b and px[x, y] != e:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
                    elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                        pass
                    elif px[x, y] != f and px[x, y] != c:
                        pass
                    elif px[x, y] != e and px[x, y] == b:
                        if px[x, y] == k:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                    elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
        else:
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
                        idx += 1
                        # [prev,sx,sy,ex,eyo,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                    if px[x, y] != c:
                        idx += 1
                        # [prev,sx,sy,ex,eyo,next,status]
                        vec.append(
                            [idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
        n_vec = []
        semi_vec = []
        small_vec = []
        sx, sy, ex, ey = 1, 2, 3, 4
        draw = ImageDraw.Draw(im)
        end_vec = ['', '']
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='loading 0%')
        window.update()
        for k, i in enumerate(vec):
            o_sx, o_sy = i[sx] - 1, i[sy]
            n_sx_r, n_sy_r = i[sx], i[sy]
            for n in vec:
                # X เปลื่ยน Y เท่า
                if (o_sx + 1 == n_sx_r and n_sx_r == n[sx]) and (o_sy == n_sy_r and n_sy_r == n[sy]) and n[sy] == n[ey]:
                    o_sx += 1
                    n_sx_r += 1
                    # n_vec.append(n)
                    # print(n)
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] == semi_vec[len(semi_vec) - 1][ey] and n[sy] == semi_vec[len(semi_vec) - 1][sy]:
                        #print(n , semi_vec[len(semi_vec) - 1]);
                        semi_vec.append(n)
                    else:
                        if semi_vec[len(semi_vec) - 1][3] == end_vec[0] and semi_vec[len(semi_vec) - 1][4] == end_vec[1]:
                            pass
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                            end_vec[0] = semi_vec[len(semi_vec) - 1][3]
                            end_vec[1] = semi_vec[len(semi_vec) - 1][4]
                        #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
                    # vec.remove(n)
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format(0 + ((k * 25) / len(vec))) + ' %')
            window.update()
        #print('loading 25%')
        # exit()
        small_vec.clear()
        semi_vec.clear()
        end_vec = []
        for k, i in enumerate(vec):
            o_sx, o_sy = i[sx], i[sy] - 1
            n_sx_d, n_sy_d = i[sx], i[sy]
            for n in vec:
                # X เท่า Y เปลื่ยน
                if (o_sx == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] == n[ex]:
                    o_sy += 1
                    n_sy_d += 1
                    # vec.remove(n)
                    # print(n)
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1 and n[ex] == semi_vec[len(semi_vec) - 1][ex] and n[sx] == semi_vec[len(semi_vec) - 1][sx]:
                        #print(n , semi_vec[len(semi_vec) - 1]);
                        semi_vec.append(n)
                    else:
                        for v in end_vec:
                            if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                                break
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                            # print(semi_vec)
                            end_vec.append(
                                [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                        # print(semi_vec)
                        #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format(25 + ((k * 25) / len(vec))) + ' %')
            window.update()
        end_vec.clear()
        semi_vec.clear()
        print('loading 50%')
        for k, i in enumerate(vec):
            o_sx, o_sy = i[sx] - 1, i[sy] - 1
            n_sx_d, n_sy_d = i[sx], i[sy]
            for n in vec:  # แก้ต่อ
                if (o_sx + 1 == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] < n[ex] and n[sy] < n[ey]:
                    o_sx += 1
                    o_sy += 1
                    n_sx_d += 1
                    n_sy_d += 1
                    # vec.remove(n)
                    # print(n)
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1:
                        #print(n , semi_vec[len(semi_vec) - 1]);
                        semi_vec.append(n)
                    else:
                        for v in end_vec:
                            if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                                break
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                            # print(semi_vec)
                            end_vec.append(
                                [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format(50 + ((k * 15) / len(vec))) + ' %')
            window.update()
        semi_vec.clear()
        small_vec.clear()
        break_point = [0]
        end_vec.clear()
        for k, n in enumerate(vec): 
            if n[sx] < n[ex] and n[sy] > n[ey]:
                if len(semi_vec) == 0:
                    semi_vec.append(n)
                elif len(semi_vec) > 0:
                    while True:
                        for e in vec:
                            if e[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and semi_vec[len(semi_vec) - 1][sy] - e[sy] == 1 and e[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and semi_vec[len(semi_vec) - 1][ey] - e[ey] == 1:
                                #print(e , semi_vec[len(semi_vec) - 1]);
                                semi_vec.append(e)
                                # print(break_point)
                                break_point[0] = 0
                                break
                            # print('break_point')
                            break_point[0] = 1
                        if break_point[0] == 1:
                            break
                    # print(semi_vec)
                    if len(semi_vec) == 1:
                        end_vec.append(semi_vec[0])  # print(semi_vec[0])
                    else:
                        for v in end_vec:  # แก้ต่อ
                            if v in semi_vec:
                                small_vec.append(
                                    [semi_vec[0], v, len(semi_vec)])
                                # print([semi_vec[0],v])
                    semi_vec.clear()
                    semi_vec.append(n)
            if for_return[0] == True:
                title_lable.configure(text='Import Picture')
                stop_button.place_forget()
                for_return[0] = False
                return
            title_lable.configure(
                text='loading ' + "{:.2f}".format(65 + ((k * 20) / len(vec))) + ' %')
            window.update()
        semi_vec.clear()
        semi_vec1 = []
        for v in end_vec:
            for i in small_vec:
                if v == i[1]:
                    semi_vec.append(i)
            # print(semi_vec)
            if len(semi_vec) == 0:
                semi_vec1.append(v)
            else:
                n_vec.append([semi_vec[len(semi_vec) - 1][0][0], semi_vec[len(semi_vec) - 1][0][sx], semi_vec[len(semi_vec) - 1][0][sy], semi_vec[len(
                    semi_vec) - 1][1][ex], semi_vec[len(semi_vec) - 1][1][ey], semi_vec[len(semi_vec) - 1][0][5], semi_vec[len(semi_vec) - 1][0][6]])
            semi_vec.clear()
        for i in semi_vec1:
            n_vec.append(i)
        width = [int(stl_width.get()) - 1]  # wall thickness
        semi_vec.clear()
        # print(len(n_vec))
        semi_vec1.clear()
        if width[0] > 1:
            num_minus = [0, 0]  # แก้ต่อโดยเพิ่มจำนวนเรื่อยๆ
            num_plus = [0, 0]
            for v in range(width[0]):
                if v % 2 == 0:
                    num_plus[0] += 1
                    num_plus[1] += 0.2
                    for k, i in enumerate(n_vec):
                        if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                            semi_vec.append([k, (i[sx]*scale)*scale+num_plus[0], (i[sy]*scale)
                                            * scale, (i[ex]*scale)*scale+num_plus[0], (i[ey]*scale)*scale])
                            semi_vec1.append(
                                [k, i[sx]+num_plus[1], i[sy], i[ex]+num_plus[1], i[ey]])
                        elif (i[sx] != i[ex] and i[sy] == i[ey]):
                            semi_vec.append([k, (i[sx]*scale)*scale, (i[sy]*scale)*scale +
                                            num_plus[0], (i[ex]*scale)*scale, (i[ey]*scale)*scale+num_plus[0]])
                            semi_vec1.append(
                                [k, i[sx], i[sy]-num_plus[1], i[ex], i[ey]-num_plus[1]])
                else:
                    num_minus[0] -= 1
                    num_minus[1] -= 0.2
                    for k, i in enumerate(n_vec):
                        if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                            semi_vec.append([k, (i[sx]*scale)*scale+num_minus[0], (i[sy]*scale)
                                            * scale, (i[ex]*scale)*scale+num_minus[0], (i[ey]*scale)*scale])
                            semi_vec1.append(
                                [k, i[sx]+num_minus[1], i[sy], i[ex]+num_minus[1], i[ey]])
                        elif (i[sx] != i[ex] and i[sy] == i[ey]):
                            semi_vec.append([k, (i[sx]*scale)*scale, (i[sy]*scale)*scale +
                                            num_minus[0], (i[ex]*scale)*scale, (i[ey]*scale)*scale+num_minus[0]])
                            semi_vec1.append(
                                [k, i[sx], i[sy]-num_minus[1], i[ex], i[ey]-num_minus[1]])
        for i in semi_vec1:
            n_vec.append(i)
        eshift = 0.03320
        print(wx*scale, hy*scale)
        with open(str(save_filename_entry.get())+'.gcode', 'w') as f:
            f.write('M140 S60\n')
            f.write('M105\n')
            f.write('M190 S60\n')
            f.write('M104 S215\n')
            f.write('M105\n')
            f.write('M109 S215\n')
            f.write('M82\n')
            f.write('M201 X500.00 Y500.00 Z100.00 E5000.00\n')
            f.write('M203 X500.00 Y500.00 Z10.00 E50.00\n')
            f.write('M204 P500.00 R1000.00 T500.00\n')
            f.write('M205 X8.00 Y8.00 Z0.40 E5.00\n')
            f.write('M220 S100\n')
            f.write('M221 S100\n')
            f.write('G28\n')
            f.write('G92 E0\n')
            f.write('G1 Z2.0 F3000\n')
            f.write('G1 X10.1 Y20 Z0.28 F5000.0\n')
            f.write('G1 X10.1 Y200.0 Z0.28 F1500.0 E15\n')
            f.write('G1 X10.4 Y200.0 Z0.28 F5000.0\n')
            f.write('G1 X10.4 Y20 Z0.28 F1500.0 E30\n')
            f.write('G92 E0\n')
            f.write('G1 Z2.0 F3000\n')
            f.write('G92 E0\n')
            f.write('G92 E0\n')
            f.write('G1 F1500 E-6.5\n')
            z = [0.2]
            e = [0.0]
            f.write('G0 F3000 Z'+str(z[0])+'\n')
            for i in range(int(stl_base_wall_height.get())):
                for k, x in enumerate(np.arange(30, wx*scale + 30.2, 0.3)):
                    if k % 2 == 0:
                        f.write('G0 X'+str(x)+' Y'+str(30)+' F5000.0\n')
                        e[0] = e[0] + (math.sqrt(pow(x-x, 2) +
                                       pow((hy*scale+30)-30, 2))*eshift)
                        f.write('G1 X'+str(x)+' Y'+str((hy*scale) +
                                30)+' F1500.0 E' + str(e[0])+'\n')
                    else:
                        f.write('G1 X'+str(x)+' Y' +
                                str((hy*scale) + 30)+' F5000.0\n')
                        e[0] = e[0] + (math.sqrt(pow(x-x, 2) +
                                       pow((hy*scale+30)-30, 2))*eshift)
                        f.write('G0 X'+str(x)+' Y'+str(30) +
                                ' F1500.0 E' + str(e[0])+'\n')
                z[0] += 0.2
                # f.write('LAYER:'+str(i))
                f.write('G0 F3000 Z'+str(z[0])+'\n')
            f.write('G92 E0\n')
            f.write('G92 E0\n')
            e[0] = 0.0
            height = int(stl_wall_height.get())
            for v in range(int(stl_wall_height.get())):
                for k, i in enumerate(n_vec):  # คิด e แยกโดยแบ่งเป็นประเภทของเส้น
                    # print(vec[k])
                    if i[sx] < i[ex] and i[sy] > i[ey]:
                        f.write('G0 X' + str(i[sx] * scale + 30) + ' Y' +
                                str(i[sy] * scale + 30) + ' F5000.0'+'\n')
                        e[0] = e[0] + (math.sqrt(pow((i[sx] * scale + 30)-(i[ex] * scale + 30), 2)+pow(
                            (i[sy] * scale + 30)-(i[ey] * scale + 30), 2))*eshift)
                        f.write('G1 X' + str(i[ex] * scale + 30) + ' Y' + str(
                            i[ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                        f.write('G1' + ' F1500.0 ' + 'E' +
                                str(e[0] - 6.5) + '\n')
                    else:
                        f.write('G0 X' + str(i[sx] * scale + 30) + ' Y' +
                                str(i[sy] * scale + 30) + ' F5000.0'+'\n')
                        e[0] = e[0] + (math.sqrt(pow((i[sx] * scale + 30)-(i[ex] * scale + 30), 2)+pow(
                            (i[ey] * scale + 30)-(i[sy] * scale + 30), 2))*eshift)
                        f.write('G1 X' + str(i[ex] * scale + 30) + ' Y' + str(
                            i[ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                        f.write('G1' + ' F1500.0 ' + 'E' +
                                str(e[0] - 6.5) + '\n')
                z[0] += 0.2
                f.write('G0 F3000 Z'+str(z[0])+'\n')
            f.write('G92 E0\n')
            f.write('G1 Z2 F3000\n')
            f.write('G92 E0\n')
            f.write('G92 E0\n')
            f.write('G1 F1500 E-6.5\n')
            f.write('G1 X5 Y5 F3000\n')
            f.write('G91\n')
            f.write('G1 E-2 F2700\n')
            f.write('G1 E-2 Z2 F2400\n')
            f.write('G1 X5 Y5 F3000\n')
            f.write('G1 Z11\n')
            f.write('G90\n')
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='loading 100%')
        window.update()
        try:os.remove(str(save_filename_entry.get())+'.gcode')
        except:pass
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='Import Picture')
        window.update()
        # cv2.imwrite('test_cat.png',color)
        # cv2.imshow('morpho',morpho)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    except Exception as e:
        print(e)
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='Import Picture')
    window.update()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_base_wall_height.place_forget()
    stl_apply.place_forget()
    gcode_apply.place_forget()
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    stop_button.place_forget()


def gcode_convert1():
    img = Image.open(filename_history[0])
    wx, hy = img.size
    print(img.size)
    px = img.load()
    scale = 2
    im = Image.new('RGBA', (wx*scale, hy*scale), (0, 0, 1, 255))
    sx, sy, ex, ey = 1, 2, 3, 4
    r, g, b = 2, 1, 0
    vec = []
    idx = -1
    if str(scale_entry.get()) != '' and str(save_filename_entry.get()) != '':
        stop_button.place(x=400, y=20)
    else:
        return
    if int(shape_line_cheak_box_var.get()) == 1:
        for y in range(hy):
            for x in range(wx):
                if y-1 < 0:  # บน
                    b = px[x, y]
                else:
                    b = px[x, y-1]
                if x+1 == wx:  # ขวา
                    c = px[x, y]
                else:
                    c = px[x+1, y]
                if y - 1 < 0:  # บน
                    d = px[x, y]
                else:
                    d = px[x, y-1]
                if x - 1 < 0:  # ซ้าย
                    e = px[x, y]
                else:
                    e = px[x-1, y]
                if y+1 >= hy:  # ล่าง
                    f = px[x, y]
                else:
                    f = px[x, y+1]
                if y+1 == hy:
                    g = px[x, y]
                elif x+1 == wx:  # ล่างขวา
                    g = px[x, y]
                else:
                    g = px[x+1, y+1]
                if y+1 == hy:
                    h = px[x, y]
                elif x-1 < 0:  # ล่างซ้าย
                    h = px[x, y]
                else:
                    h = px[x-1, y+1]
                if y-1 < 0:
                    j = px[x, y]
                elif x+1 == wx:  # บนขวา
                    j = px[x, y]
                else:
                    j = px[x+1, y-1]
                if y-1 < 0:
                    k = px[x, y]
                elif x-1 < 0:  # บนซ้าย
                    k = px[x, y]
                else:
                    k = px[x-1, y-1]
                if px[x, y] != b and px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y, x + 1, y + 1, idx + 1, 0])
                elif px[x, y] == e:
                    if px[x, y] != b:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                elif px[x, y] == b:
                    if px[x, y] != c:
                        if px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            # [prev,sx,sy,ex,ey,next,status]
                            vec.append(
                                [idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
                if px[x, y] != b and px[x, y] != e:
                    idx += 1
                    # [prev,sx,sy,ex,ey,next,status]
                    vec.append([idx - 1, x, y + 1, x + 1, y, idx + 1, 0])
                elif px[x, y] != e and px[x, y] == c and px[x, y] != f:
                    pass
                elif px[x, y] != f and px[x, y] != c:
                    pass
                elif px[x, y] != e and px[x, y] == b:
                    if px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x, y, x, y + 1, idx + 1, 0])
                elif px[x, y] != c and px[x, y] == b and px[x, y] == g:
                    if px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        vec.append([idx - 1, x+1, y, x+1, y + 1, idx + 1, 0])
    else:
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
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x, y, x + 1, y, idx + 1, 0])
                if px[x, y] != c:
                    idx += 1
                    # [prev,sx,sy,ex,eyo,next,status]
                    vec.append([idx - 1, x + 1, y, x + 1, y + 1, idx + 1, 0])
    n_vec = []
    semi_vec = []
    small_vec = []
    sx, sy, ex, ey = 1, 2, 3, 4
    draw = ImageDraw.Draw(im)
    end_vec = ['', '']
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 0%')
    window.update()
    for k, i in enumerate(vec):
        o_sx, o_sy = i[sx] - 1, i[sy]
        n_sx_r, n_sy_r = i[sx], i[sy]
        for n in vec:
            # X เปลื่ยน Y เท่า
            if (o_sx + 1 == n_sx_r and n_sx_r == n[sx]) and (o_sy == n_sy_r and n_sy_r == n[sy]) and n[sy] == n[ey]:
                o_sx += 1
                n_sx_r += 1
                # n_vec.append(n)
                # print(n)
                if len(semi_vec) == 0:
                    semi_vec.append(n)
                elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] == semi_vec[len(semi_vec) - 1][ey] and n[sy] == semi_vec[len(semi_vec) - 1][sy]:
                    #print(n , semi_vec[len(semi_vec) - 1]);
                    semi_vec.append(n)
                else:
                    if semi_vec[len(semi_vec) - 1][3] == end_vec[0] and semi_vec[len(semi_vec) - 1][4] == end_vec[1]:
                        pass
                    else:
                        n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                            semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                        end_vec[0] = semi_vec[len(semi_vec) - 1][3]
                        end_vec[1] = semi_vec[len(semi_vec) - 1][4]
                    #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                    small_vec.clear()
                    semi_vec.clear()
                    semi_vec.append(n)
                # vec.remove(n)
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(
            text='loading ' + "{:.2f}".format(0 + ((k * 25) / len(vec))) + ' %')
        window.update()
    #print('loading 25%')
    # exit()
    small_vec.clear()
    semi_vec.clear()
    end_vec = []
    for k, i in enumerate(vec):
        o_sx, o_sy = i[sx], i[sy] - 1
        n_sx_d, n_sy_d = i[sx], i[sy]
        for n in vec:
            # X เท่า Y เปลื่ยน
            if (o_sx == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] == n[ex]:
                o_sy += 1
                n_sy_d += 1
                # vec.remove(n)
                # print(n)
                if len(semi_vec) == 0:
                    semi_vec.append(n)
                elif n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1 and n[ex] == semi_vec[len(semi_vec) - 1][ex] and n[sx] == semi_vec[len(semi_vec) - 1][sx]:
                    #print(n , semi_vec[len(semi_vec) - 1]);
                    semi_vec.append(n)
                else:
                    for v in end_vec:
                        if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                            break
                    else:
                        n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                            semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                        # print(semi_vec)
                        end_vec.append(
                            [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                    # print(semi_vec)
                    #print([semi_vec[0][0],semi_vec[0][1],semi_vec[0][2],semi_vec[len(semi_vec) - 1][3],semi_vec[len(semi_vec) - 1][4],semi_vec[0][5],semi_vec[0][6]])
                    small_vec.clear()
                    semi_vec.clear()
                    semi_vec.append(n)
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(
            text='loading ' + "{:.2f}".format(25 + ((k * 25) / len(vec))) + ' %')
        window.update()
    end_vec.clear()
    semi_vec.clear()
    print('loading 50%')
    for k, i in enumerate(vec):
        o_sx, o_sy = i[sx] - 1, i[sy] - 1
        n_sx_d, n_sy_d = i[sx], i[sy]
        for n in vec:  # แก้ต่อ
            if (o_sx + 1 == n_sx_d and n_sx_d == n[sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[sy]) and n[sx] < n[ex] and n[sy] < n[ey]:
                o_sx += 1
                o_sy += 1
                n_sx_d += 1
                n_sy_d += 1
                # vec.remove(n)
                # print(n)
                if len(semi_vec) == 0:
                    semi_vec.append(n)
                elif n[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and n[sy] - semi_vec[len(semi_vec) - 1][sy] == 1 and n[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and n[ey] - semi_vec[len(semi_vec) - 1][ey] == 1:
                    #print(n , semi_vec[len(semi_vec) - 1]);
                    semi_vec.append(n)
                else:
                    for v in end_vec:
                        if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                            break
                    else:
                        n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                            semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4], semi_vec[0][5], semi_vec[0][6]])
                        # print(semi_vec)
                        end_vec.append(
                            [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                    small_vec.clear()
                    semi_vec.clear()
                    semi_vec.append(n)
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(text='loading ' + "{:.2f}".format(50 + ((k * 15) / len(vec))) + ' %')
        window.update()
    semi_vec.clear()
    small_vec.clear()
    break_point = [0]
    end_vec.clear()
    for k, n in enumerate(vec):  # แก้ต่อ
        #if n[sx] == 82 and n[sy] == 34 and n[ex] == 83 and n[ey] == 33:print(n)
        if n[sx] < n[ex] and n[sy] > n[ey]:
            if len(semi_vec) == 0:
                semi_vec.append(n)
            elif len(semi_vec) > 0:
                while True:
                    for e in vec:
                        if e[sx] - semi_vec[len(semi_vec) - 1][sx] == 1 and semi_vec[len(semi_vec) - 1][sy] - e[sy] == 1 and e[ex] - semi_vec[len(semi_vec) - 1][ex] == 1 and semi_vec[len(semi_vec) - 1][ey] - e[ey] == 1:
                            #print(e , semi_vec[len(semi_vec) - 1]);
                            semi_vec.append(e)
                            # print(break_point)
                            break_point[0] = 0
                            break
                        # print('break_point')
                        break_point[0] = 1
                    if break_point[0] == 1:
                        break
                # print(semi_vec)
                if len(semi_vec) == 1:
                    end_vec.append(semi_vec[0])  # print(semi_vec[0])
                else:
                    for v in end_vec:  # แก้ต่อ
                        if v in semi_vec:
                            small_vec.append([semi_vec[0], v, len(semi_vec)])
                            # print([semi_vec[0],v])
                semi_vec.clear()
                semi_vec.append(n)
        if for_return[0] == True:
            title_lable.configure(text='Import Picture')
            stop_button.place_forget()
            for_return[0] = False
            return
        title_lable.configure(
            text='loading ' + "{:.2f}".format(65 + ((k * 20) / len(vec))) + ' %')
        window.update()
    #print('loading 75%')
    semi_vec.clear()
    semi_vec1 = []
    for v in end_vec:
        for i in small_vec:
            if v == i[1]:
                semi_vec.append(i)
        # print(semi_vec)
        if len(semi_vec) == 0:
            semi_vec1.append(v)
        else:
            n_vec.append([semi_vec[len(semi_vec) - 1][0][0], semi_vec[len(semi_vec) - 1][0][sx], semi_vec[len(semi_vec) - 1][0][sy], semi_vec[len(
                semi_vec) - 1][1][ex], semi_vec[len(semi_vec) - 1][1][ey], semi_vec[len(semi_vec) - 1][0][5], semi_vec[len(semi_vec) - 1][0][6]])
        semi_vec.clear()
    for i in semi_vec1:
        n_vec.append(i)
    width = [int(stl_width.get()) - 1]  # wall thickness
    semi_vec.clear()
    # print(len(n_vec))
    semi_vec1.clear()
    if width[0] > 1:
        num_minus = [0, 0]  # แก้ต่อโดยเพิ่มจำนวนเรื่อยๆ
        num_plus = [0, 0]
        for v in range(width[0]):
            if v % 2 == 0:
                num_plus[0] += 1
                num_plus[1] += 0.2
                for k, i in enumerate(n_vec):
                    if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                        semi_vec.append([k, (i[sx]*scale)*scale+num_plus[0], (i[sy]*scale)
                                        * scale, (i[ex]*scale)*scale+num_plus[0], (i[ey]*scale)*scale])
                        semi_vec1.append(
                            [k, i[sx]+num_plus[1], i[sy], i[ex]+num_plus[1], i[ey]])
                    elif (i[sx] != i[ex] and i[sy] == i[ey]):
                        semi_vec.append([k, (i[sx]*scale)*scale, (i[sy]*scale)*scale +
                                        num_plus[0], (i[ex]*scale)*scale, (i[ey]*scale)*scale+num_plus[0]])
                        semi_vec1.append(
                            [k, i[sx], i[sy]-num_plus[1], i[ex], i[ey]-num_plus[1]])
            else:
                num_minus[0] -= 1
                num_minus[1] -= 0.2
                for k, i in enumerate(n_vec):
                    if (i[sx] < i[ex] and i[sy] > i[ey]) or (i[sx] < i[ex] and i[sy] < i[ey]) or (i[sx] == i[ex] and i[sy] != i[ey]):
                        semi_vec.append([k, (i[sx]*scale)*scale+num_minus[0], (i[sy]*scale)
                                        * scale, (i[ex]*scale)*scale+num_minus[0], (i[ey]*scale)*scale])
                        semi_vec1.append(
                            [k, i[sx]+num_minus[1], i[sy], i[ex]+num_minus[1], i[ey]])
                    elif (i[sx] != i[ex] and i[sy] == i[ey]):
                        semi_vec.append([k, (i[sx]*scale)*scale, (i[sy]*scale)*scale +
                                        num_minus[0], (i[ex]*scale)*scale, (i[ey]*scale)*scale+num_minus[0]])
                        semi_vec1.append(
                            [k, i[sx], i[sy]-num_minus[1], i[ex], i[ey]-num_minus[1]])
    for i in semi_vec1:
        n_vec.append(i)
    eshift = 0.03320
    scale = float(scale_entry.get())  # scale
    print(wx*scale, hy*scale)
    with open(str(save_filename_entry.get())+'.txt', 'w') as f:
        f.write('M140 S60\n')
        f.write('M105\n')
        f.write('M190 S60\n')
        f.write('M104 S215\n')
        f.write('M105\n')
        f.write('M109 S215\n')
        f.write('M82\n')
        f.write('M201 X500.00 Y500.00 Z100.00 E5000.00\n')
        f.write('M203 X500.00 Y500.00 Z10.00 E50.00\n')
        f.write('M204 P500.00 R1000.00 T500.00\n')
        f.write('M205 X8.00 Y8.00 Z0.40 E5.00\n')
        f.write('M220 S100\n')
        f.write('M221 S100\n')
        f.write('G28\n')
        f.write('G92 E0\n')
        f.write('G1 Z2.0 F3000\n')
        f.write('G1 X10.1 Y20 Z0.28 F5000.0\n')
        f.write('G1 X10.1 Y200.0 Z0.28 F1500.0 E15\n')
        f.write('G1 X10.4 Y200.0 Z0.28 F5000.0\n')
        f.write('G1 X10.4 Y20 Z0.28 F1500.0 E30\n')
        f.write('G92 E0\n')
        f.write('G1 Z2.0 F3000\n')
        f.write('G92 E0\n')
        f.write('G92 E0\n')
        f.write('G1 F1500 E-6.5\n')
        z = [0.2]
        e = [0.0]
        f.write('G0 F3000 Z'+str(z[0])+'\n')
        for i in range(int(stl_base_wall_height.get())):
            for k, x in enumerate(np.arange(30, wx*scale + 30.2, 0.3)):
                if k % 2 == 0:
                    f.write('G0 X'+str(x)+' Y'+str(30)+' F5000.0\n')
                    e[0] = e[0] + \
                        (math.sqrt(pow(x-x, 2)+pow((hy*scale+30)-30, 2))*eshift)
                    f.write('G1 X'+str(x)+' Y'+str((hy*scale) + 30) +
                            ' F1500.0 E' + str(e[0])+'\n')
                else:
                    f.write('G1 X'+str(x)+' Y' +
                            str((hy*scale) + 30)+' F5000.0\n')
                    e[0] = e[0] + \
                        (math.sqrt(pow(x-x, 2)+pow((hy*scale+30)-30, 2))*eshift)
                    f.write('G0 X'+str(x)+' Y'+str(30) +
                            ' F1500.0 E' + str(e[0])+'\n')
            z[0] += 0.2
            # f.write('LAYER:'+str(i))
            f.write('G0 F3000 Z'+str(z[0])+'\n')
        f.write('G92 E0\n')
        f.write('G92 E0\n')
        e[0] = 0.0
        height = int(stl_wall_height.get())
        for v in range(height):
            for k, i in enumerate(n_vec):  # คิด e แยกโดยแบ่งเป็นประเภทของเส้น
                # print(vec[k])
                if i[sx] < i[ex] and i[sy] > i[ey]:
                    f.write('G0 X' + str(i[sx] * scale + 30) + ' Y' +
                            str(i[sy] * scale + 30) + ' F5000.0'+'\n')
                    # +(sqrt(pow($x1-$x2,2)+pow($y2-$y1,2))*$eshift)
                    e[0] = e[0] + (math.sqrt(pow((i[sx] * scale + 30)-(i[ex] * scale + 30), 2)+pow(
                        (i[sy] * scale + 30)-(i[ey] * scale + 30), 2))*eshift)
                    f.write('G1 X' + str(i[ex] * scale + 30) + ' Y' + str(
                        i[ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                    f.write('G1' + ' F1500.0 ' + 'E' + str(e[0] - 6.5) + '\n')
                else:
                    f.write('G0 X' + str(i[sx] * scale + 30) + ' Y' +
                            str(i[sy] * scale + 30) + ' F5000.0'+'\n')
                    # +(sqrt(pow($x1-$x2,2)+pow($y2-$y1,2))*$eshift)
                    e[0] = e[0] + (math.sqrt(pow((i[sx] * scale + 30)-(i[ex] * scale + 30), 2)+pow(
                        (i[ey] * scale + 30)-(i[sy] * scale + 30), 2))*eshift)
                    f.write('G1 X' + str(i[ex] * scale + 30) + ' Y' + str(
                        i[ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                    f.write('G1' + ' F1500.0 ' + 'E' + str(e[0] - 6.5) + '\n')
            z[0] += 0.2
            f.write('G0 F3000 Z'+str(z[0])+'\n')
        f.write('G92 E0\n')
        f.write('G1 Z2 F3000\n')
        f.write('G92 E0\n')
        f.write('G92 E0\n')
        f.write('G1 F1500 E-6.5\n')
        f.write('G1 X5 Y5 F3000\n')
        f.write('G91\n')
        f.write('G1 E-2 F2700\n')
        f.write('G1 E-2 Z2 F2400\n')
        f.write('G1 X5 Y5 F3000\n')
        f.write('G1 Z11\n')
        f.write('G90\n')
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='loading 100%')
    window.update()
    try:
        os.remove(str(save_filename_entry.get())+'.gcode')
    except:
        pass
    os.rename(str(save_filename_entry.get())+'.txt',
              str(save_filename_entry.get())+'.gcode')
    if for_return[0] == True:
        title_lable.configure(text='Import Picture')
        stop_button.place_forget()
        for_return[0] = False
        return
    title_lable.configure(text='Import Picture')
    window.update()
    stl_wall_height.place_forget()
    stl_wall_height_lable.place_forget()
    stl_width.place_forget()
    stl_width_lable.place_forget()
    stl_base_wall_height_lable.place_forget()
    stl_base_wall_height.place_forget()
    stl_apply.place_forget()
    gcode_apply.place_forget()
    threshold_entry.place_forget()
    threshold_lable.place_forget()
    stop_button.place_forget()


stop_button = tk.Button(master=window, text='Cancel', command=stop)
shape_line_cheak_box_var = tk.IntVar()
drawing_lines_cheak_box_var = tk.IntVar()
stl_wall_height = tk.Entry(master=window)
stl_wall_height_lable = tk.Label(master=window, text='Wall height :')
stl_width = tk.Entry(master=window)
stl_width_lable = tk.Label(master=window, text='Wall Thickness :')
stl_base_wall_height = tk.Entry(master=window)
stl_base_wall_height_lable = tk.Label(master=window, text='Base height :')
stl_apply = tk.Button(master=window, text='STL', width=3)
gcode_apply = tk.Button(master=window, text='GCODE', width=5)  # ทำต่อ
title_lable = tk.Label(master=window, text='Import Picture', font=('Bold', 20))
title_lable.pack()
import_pic_button = tk.Button(master=window, text='Upload', command=import_pic)
import_pic_button.pack()
file_locate_lable = tk.Label(
    master=window, text='*All file will be save in the program directory.*')
file_locate_lable.place(y=390, x=10)
dev_by_lable = tk.Label(
    master=window, text='*COPYRIGHT © Tamtikorn 2022. All Right Reserved.*')
dev_by_lable.place(y=390, x=317)
scale_lable = tk.Label(master=window, text='Scale :')
scale_lable.place(x=120, y=440)
shape_line_cheak_box = tk.Checkbutton(
    master=window, text='Anti-Aliasing', variable=shape_line_cheak_box_var)
shape_line_cheak_box.place(x=170, y=460)
drawing_lines_cheak_box = tk.Checkbutton(
    master=window, text='Drawing Line(For Upscale(Color),To SGV and To PDF)', variable=drawing_lines_cheak_box_var)
drawing_lines_cheak_box.place(x=265, y=460)
scale_entry = tk.Entry(master=window)
scale_entry.place(x=160, y=440)
save_filename_lable = tk.Label(master=window, text='Filename :')
save_filename_lable.place(x=290, y=440)
save_filename_entry = tk.Entry(master=window)
save_filename_entry.place(x=350, y=440)
threshold_lable = tk.Label(master=window, text="Threshold Value :")
threshold_entry = tk.Entry(master=window)
stl_convert_button = tk.Button(
    master=window, text='To'+'\n' + '3D-Printer', command=stl_convert1, width=8, height=7)
stl_convert_button.place(x=600 - 275 + 70, y=483)
sgv_convert_button = tk.Button(
    master=window, text='To SVG', command=sgv_convert, width=8, height=7)
sgv_convert_button.place(x=505 - 245 + 70, y=483)
pdf_convert_button = tk.Button(
    master=window, text='To PDF', command=pdf_convert, width=8, height=7)
pdf_convert_button.place(x=410 - 215 + 70, y=483)
dxf_convert_button = tk.Button(
    master=window, text='To DXF', command=dxf_convert, width=8, height=7)
dxf_convert_button.place(x=315 - 185 + 70, y=483)
up_scale_line_convert_button = tk.Button(
    master=window, text='Upscale' + '\n' + '(Line Only)', command=Upscale_line, width=8, height=7)
up_scale_line_convert_button.place(x=220 - 155 + 70, y=483)
up_scale_color_convert_button = tk.Button(
    master=window, text='Upscale'+'\n'+'(Color)', command=Upscale_color, width=8, height=7)
up_scale_color_convert_button.place(x=125 - 125 + 70, y=483)
real_pic_stl_button = tk.Button(master=window, text='To'+'\n' + '3D-Printer' +
                                '\n' + '(Non-'+'\n' + 'Digital art)', command=real_pic_stl1, width=8, height=7)
real_pic_stl_button.place(x=600 - 210 + 70, y=483)

window.mainloop()