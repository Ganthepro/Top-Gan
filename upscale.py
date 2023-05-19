import cv2
import numpy as np
from PIL import Image, ImageDraw
import math

class upscale:
    def __init__(self, scale: int, im: str, realpic: bool, lable, window, interruptBtn):
        if lable != None and window != None and interruptBtn != None:
            self.label = lable
            self.window = window
            self.interruptBtn = interruptBtn
            self.interruptBtn.configure(command=self.interruptFunc)
        self.interrupt = False
        if realpic:
            self.img = self.convertREALPIC(im, 51)
        else:
            self.img = Image.open(im)
        self.scale = scale
        self.vec = []
        self.img = self.img.convert('RGBA')
        self.wx, self.hy = self.img.size
        self.sx, self.sy, self.ex, self.ey = 1, 2, 3, 4
        self.px = self.img.load()

    def interruptFunc(self):
        self.interrupt = True

    def loadingStatus(self, start: int, end: int, num: int, maxNum: int, text: str):
        try:
            if self.interrupt:
                self.interrupt = False
                raise Exception(True)
            load = "{:.2f}".format(start + ((num * end) / maxNum))
            self.label.configure(text=f"{text} ({load}%)")
            self.window.update()
        except:
            pass

    def getVec(self):
        return self.vec

    def getSize(self):
        return (self.img.size[0] * self.scale, self.img.size[1] * self.scale)

    def showPic(self):
        self.im.show()

    def savePic(self, fname: str):
        self.im.save(fname + '.png')

    def drawLine(self):
        self.im = Image.new('RGBA',  (self.wx * self.scale,
                            self.hy * self.scale), (0, 0, 1, 255))
        draw = ImageDraw.Draw(self.im)
        for n, i in enumerate(self.vec):
            draw.line(
                ((i[self.sx]) + 0,
                 (i[self.sy]) + 0,
                 (i[self.ex]) + 0,
                 (i[self.ey]) + 0
                 ), fill=(0, 255, 1, 255))
            self.loadingStatus(0, 100, n, len(self.vec), "Drawing Line")
        return self.im

    def drawColor(self, dline: bool):
        self.im = Image.new('RGBA',  (self.wx * self.scale,
                            self.hy * self.scale), (0, 0, 1, 255))
        cv_img = np.array(self.img)
        img_cv2 = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        n_hy, n_wx = self.hy * self.scale, self.wx * self.scale
        RGB = []
        yshift = -1
        for y in range(self.hy):
            for x in range(self.wx):
                blue = img_cv2[y, x, 0]
                green = img_cv2[y, x, 1]
                red = img_cv2[y, x, 2]
                RGB.append([red, green, blue])
                self.im.putpixel(
                    (x * self.scale, y * self.scale), (red, green, blue))
            self.loadingStatus(0, 25, y, self.hy, "Drawing Line & Color")
        px_im = self.im.load()
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != e:
                    self.im.putpixel((x, y), (e[0], e[1], e[2]))
            self.loadingStatus(25, 10, y, n_hy, "Drawing Line & Color")
        draw = ImageDraw.Draw(self.im)
        for n, i in enumerate(self.vec):
            draw.line(((i[self.sx]), (i[self.sy]) + (yshift * self.scale), (i[self.ex]),
                      (i[self.ey]) + (yshift * self.scale)), fill=(0, 255, 1, 255))
            self.loadingStatus(35, 10, n, len(self.vec),
                               "Drawing Line & Color")
        for y in range(n_hy):
            for x in range(n_wx):
                if y - 1 < 0:  # บน
                    b = px_im[x, y]
                else:
                    b = px_im[x, y - 1]
                if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != b and b != (
                        0, 255, 1, 255):
                    self.im.putpixel((x, y), (b[0], b[1], b[2]))
            self.loadingStatus(45, 5, y, n_hy, "Drawing Line & Color")
        for y in reversed(range(n_hy)):
            for x in range(n_wx):
                if y + 1 >= n_hy:  # ล่าง
                    f = px_im[x, y]
                else:
                    f = px_im[x, y + 1]
                if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != f and f != (
                        0, 255, 1, 255):
                    self.im.putpixel((x, y), (f[0], f[1], f[2]))
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
                if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != e and e != (
                        0, 255, 1, 255):
                    self.im.putpixel((x, y), (e[0], e[1], e[2]))
            self.loadingStatus(50, 25, y, n_hy, "Drawing Line & Color")
        for y in range(n_hy):
            for x in reversed(range(n_wx)):
                if x + 1 == n_wx:  # ขวา
                    c = px_im[x, y]
                else:
                    c = px_im[x + 1, y]
                if px_im[x, y] == (0, 0, 1, 255) and px_im[x, y] != c and c != (
                        0, 255, 1, 255):
                    self.im.putpixel((x, y), (c[0], c[1], c[2]))
            self.loadingStatus(75, 25, y, n_hy, "Drawing Line & Color")
        if dline == False:
            for y in range(n_hy):
                for x in range(n_wx):
                    if x - 1 < 0:  # ซ้าย
                        e = px_im[x, y]
                    else:
                        e = px_im[x - 1, y]
                    if px_im[x, y] == (0, 255, 1, 255):
                        self.im.putpixel((x, y), (e[0], e[1], e[2]))
                self.loadingStatus(0, 33, y, n_hy, "Removing Line")
            for y in range(n_hy):
                for x in range(n_wx):
                    if y - 1 < 0:  # บน
                        b = px_im[x, y]
                    else:
                        b = px_im[x, y - 1]
                    if px_im[x, y] == (0, 255, 1, 255):
                        self.im.putpixel((x, y), (b[0], b[1], b[2]))
                self.loadingStatus(33, 33, y, n_hy, "Removing Line")
            for y in range(n_hy):
                for x in range(n_wx):
                    if x - 1 < 0:  # ซ้าย
                        e = px_im[x, y]
                    else:
                        e = px_im[x - 1, y]
                    if px_im[x, y] == (0, 255, 1, 255):
                        self.im.putpixel((x, y), (e[0], e[1], e[2]))
                self.loadingStatus(66, 34, y, n_hy, "Removing Line")
        return self.im

    def anti_aliasing(self, fixline: bool):
        self.AA = True
        self.px = self.img.load()
        idx = -1
        for y in range(self.hy):
            for x in range(self.wx):
                if y - 1 < 0:  # บน
                    b = self.px[x, y]
                else:
                    b = self.px[x, y - 1]
                if x + 1 == self.wx:  # ขวา
                    c = self.px[x, y]
                else:
                    c = self.px[x + 1, y]
                if y - 1 < 0:  # บน
                    d = self.px[x, y]
                else:
                    d = self.px[x, y - 1]
                if x - 1 < 0:  # ซ้าย
                    e = self.px[x, y]
                else:
                    e = self.px[x - 1, y]
                if y + 1 >= self.hy:  # ล่าง
                    f = self.px[x, y]
                else:
                    f = self.px[x, y + 1]
                if y + 1 == self.hy:
                    g = self.px[x, y]
                elif x + 1 == self.wx:  # ล่างขวา
                    g = self.px[x, y]
                else:
                    g = self.px[x + 1, y + 1]
                if y + 1 == self.hy:
                    h = self.px[x, y]
                elif x - 1 < 0:  # ล่างซ้าย
                    h = self.px[x, y]
                else:
                    h = self.px[x - 1, y + 1]
                if y - 1 < 0:
                    j = self.px[x, y]
                elif x + 1 == self.wx:  # บนขวา
                    j = self.px[x, y]
                else:
                    j = self.px[x + 1, y - 1]
                if y - 1 < 0:
                    k = self.px[x, y]
                elif x - 1 < 0:  # บนซ้าย
                    k = self.px[x, y]
                else:
                    k = self.px[x - 1, y - 1]
                if self.px[x, y] != b and self.px[x, y] != c:
                    idx += 1
                    self.vec.append([idx - 1, x * self.scale, y * self.scale, (x + 1)
                                     * self.scale, (y + 1) * self.scale, idx + 1, 0])
                elif self.px[x, y] == e:
                    if self.px[x, y] != b:
                        idx += 1
                        self.vec.append([idx - 1, x * self.scale, y * self.scale,
                                         (x + 1) * self.scale, y * self.scale, idx + 1, 0])
                elif self.px[x, y] == b:
                    if self.px[x, y] != c:
                        if self.px[x, y] == j:
                            pass
                        else:
                            idx += 1
                            self.vec.append([idx - 1, (x + 1) * self.scale, y * self.scale,
                                             (x + 1) * self.scale, (y + 1) * self.scale, idx + 1, 0])
                if self.px[x, y] != b and self.px[x, y] != e:
                    idx += 1
                    self.vec.append([idx - 1, x * self.scale, (y + 1) * self.scale,
                                     (x + 1) * self.scale, y * self.scale, idx + 1, 0])
                elif self.px[x, y] != e and self.px[x, y] == c and self.px[x, y] != f:
                    pass
                elif self.px[x, y] != f and self.px[x, y] != c:
                    pass
                elif self.px[x, y] != e and self.px[x, y] == b:
                    if self.px[x, y] == k:
                        pass
                    else:
                        idx += 1
                        # [prev,sx,sy,ex,ey,next,status]
                        self.vec.append([idx - 1, x * self.scale, y * self.scale, x *
                                         self.scale, (y + 1) * self.scale, idx + 1, 0])
                elif self.px[x, y] != c and self.px[x, y] == b and self.px[x, y] == g:
                    if self.px[x, y] == j:
                        pass
                    else:
                        idx += 1
                        self.vec.append([idx - 1, (x + 1) * self.scale, y * self.scale, (x + 1) * self.scale,
                                         (y + 1) * self.scale, idx + 1, 0])  # [prev,sx,sy,ex,ey,next,status]
            self.loadingStatus(0, 100, y, self.hy, "Creating Vector")
        if fixline:
            n_vec = []
            semi_vec = []
            for k, n in enumerate(self.vec):
                for i in self.vec:
                    if n[self.sx] == i[self.sx] and n[self.sy] - i[self.sy] == self.scale and n[self.ex] == i[self.ex] and i[self.ey] - n[self.ey] == self.scale:
                        semi_vec.append(n)  # /
                        semi_vec.append(i)  # \
                        n_vec.append([n[0], n[self.sx], n[self.sy], n[self.ex] -
                                     math.ceil(self.scale / 2), n[self.ey] + math.ceil(self.scale / 2)])
                        n_vec.append([i[0], i[self.sx] + math.ceil(self.scale / 2),
                                     i[self.sy] + math.ceil(self.scale / 2), i[self.ex], i[self.ey]])
                self.loadingStatus(0, 100, k, len(self.vec), "Fixing Line")
            for i in self.vec:
                if i in semi_vec:
                    pass
                else:
                    n_vec.append(i)
            self.vec = n_vec

    def no_anti_aliasing(self):
        self.AA = False
        idx = -1
        for y in range(self.hy):
            for x in range(self.wx):
                if y - 1 < 0:
                    b = self.px[x, y]
                else:
                    b = self.px[x, y - 1]
                if x + 1 == self.wx:
                    c = self.px[x, y]
                else:
                    c = self.px[x + 1, y]
                if self.px[x, y] != b:
                    idx += 1
                    self.vec.append([idx - 1, x * self.scale, y * self.scale, (x + 1)
                                     * self.scale, y * self.scale, idx + 1, 0])
                if self.px[x, y] != c:
                    idx += 1
                    self.vec.append([idx - 1, (x + 1) * self.scale, y * self.scale, (x + 1) * self.scale,
                                     (y + 1) * self.scale, idx + 1, 0])
            if self.interrupt:
                self.interrupt = False
                return True
            load = "{:.2f}".format(0 + ((y * 100) / self.hy))
            self.label.configure(text=f"Creating Vector ({load}%)")
            self.window.update()
            self.loadingStatus(0, 100, y, self.hy, "Creating Vector")

    def convertREALPIC(self, im: Image, threshold: int):
        img = Image.open(im)
        wx, hy = img.size
        img = img.convert('RGBA')
        cv_img = np.array(img)
        img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        resize = cv2.resize(img, (1*wx, 1*hy))
        grey_img = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
        invert_img = cv2.bitwise_not(grey_img)
        blur_img = cv2.GaussianBlur(invert_img, (111, 111), 0)
        invblur_img = cv2.bitwise_not(blur_img)
        sketch_img = cv2.divide(grey_img, invblur_img, scale=256.0)
        adaptive = cv2.adaptiveThreshold(
            sketch_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, int(threshold), 9)
        color = cv2.cvtColor(adaptive, cv2.COLOR_BGR2RGB)
        color[np.where((color == [0, 0, 0]).all(axis=2))] = [0, 0, 255]
        color[np.where((color == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
        return Image.fromarray(color)
