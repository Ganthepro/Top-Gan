import ezdxf as dxf
import svgwrite as svg
from fpdf import FPDF
from PIL import Image

class vector:
    def __init__(self, lable, window, interruptBtn):
        self.pdf = FPDF()
        if lable != None and window != None and interruptBtn != None: 
            self.label = lable
            self.window = window
            self.interruptBtn = interruptBtn
            self.interruptBtn.configure(command=self.interruptFunc)
        self.sx, self.sy, self.ex, self.ey = 1, 2, 3, 4
        self.interrupt = False

    def loadingStatus(self, start: int, end: int, num: int, maxNum: int, text: str):
        try:
            if self.interrupt == True:
                self.interrupt = False
                raise Exception(True)
            load = "{:.2f}".format(start + ((num * end) / maxNum))
            self.label.configure(text=f"{text} ({load}%)")
            self.window.update()
        except:pass

    def interruptFunc(self):
        self.interrupt = True

    def convertPDF(self, im: Image, fname: str, dline: bool, vec: list, scale: int):
        self.pdf.add_page('L')
        id = 0
        start_p = [0, 0]
        n_wx, n_hy = im.size
        px_im = im.load()
        id1 = 0
        for y in range(n_hy):
            for x in range(1, n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] != [0,0,1]:
                    if px_im[x, y] == e:
                        id1 += 1
                    elif px_im[x, y] != e:
                        self.pdf.line(0 / 10, y / 10, (0 + id1) / 10, y / 10)
                        self.pdf.set_line_width(0.2)
                        self.pdf.set_draw_color(
                            px_im[0, y][0], px_im[0, y][1], px_im[0, y][2])
                        id1 = 0
                        break
            self.loadingStatus(0, 50, y, n_hy, "Creating PDF")
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] != [0,0,1]:
                    if px_im[x, y] == e:
                        if start_p[0] + id > n_wx:
                            continue
                        else:
                            id += 1
                    elif px_im[x, y] != e:
                        self.pdf.line(
                            start_p[0] / 10, start_p[1] / 10, (start_p[0] + id) / 10, start_p[1] / 10)
                        self.pdf.set_line_width(0.23)
                        self.pdf.set_draw_color(
                            px_im[x, y][0], px_im[x, y][1], px_im[x, y][2])
                        id = 0
                        start_p[0] = x
                        start_p[1] = y
            self.loadingStatus(50, 50, y, n_hy, "Creating PDF")
        if dline:
            for n, i in enumerate(vec):
                self.pdf.line((i[self.sx]) / 10, ((i[self.sy] - scale)) / 10,
                              (i[self.ex]) / 10, ((i[self.ey] - scale)) / 10)
                self.pdf.set_draw_color(0, 255, 0)
                self.loadingStatus(0, 100, n, len(vec), "Creating PDF Line")
        self.pdf.output(fname + ".pdf")

    def convertDXF(self, vec: list, fname: str):
        doc = dxf.new('R2010')
        msp = doc.modelspace()
        for n, i in enumerate(vec):
            msp.add_line((i[self.sx], i[self.sy]), (i[self.ex], i[self.ey]))
            self.loadingStatus(0, 100, n, len(vec), "Creating DXF")
        doc.saveas(fname + '.dxf')

    def convertSVG(self, im: Image, vec: list, fname: str, scale: int, dline: bool, AA: bool):
        dwg = svg.Drawing(f'{fname}.svg', profile='tiny')
        img = im
        n_wx, n_hy = im.size
        px_im = img.load()
        id1 = 0
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] != [0,0,1]:
                    if px_im[x, y] == e:
                        id1 += 1
                    elif px_im[x, y] != e:
                        dwg.add(dwg.line((0, y), ((0 + id1), y), stroke=svg.rgb(
                            px_im[0, y][0], px_im[0, y][1], px_im[0, y][2], 'RGB'), stroke_width=2))
                        id1 = 0
            self.loadingStatus(0, 50, y, n_hy, "Creating SVG")
        id = 1
        start_p = [0, 0]
        for y in range(n_hy):
            for x in range(n_wx):
                if x - 1 < 0:  # ซ้าย
                    e = px_im[x, y]
                else:
                    e = px_im[x - 1, y]
                if px_im[x, y] != [0,0,1]:
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
            self.loadingStatus(50, 100, y, n_hy, "Creating SVG")
        if dline:
            for n, i in enumerate(vec):
                dwg.add(dwg.line(((i[self.sx] + 1), (i[self.sy] - scale)), ((i[self.ex] + 1),
                        (i[self.ey] - scale)), stroke=svg.rgb(0, 255, 0, 'RGB'), stroke_width=1.5))
                self.loadingStatus(0, 100, n, len(vec), "Drawing Line")
        elif AA:
            count_1 = 0
            for y in range(0, n_hy):
                for x in range(0, n_wx):
                    for i in vec:
                        if x == (i[self.ex]) and y == (i[self.ey] - 1):
                            dwg.add(dwg.line(((i[self.sx]), (i[self.sy] - (1 * scale))), ((i[self.ex]), (i[self.ey] - (1 * scale))),
                                             stroke=svg.rgb(px_im[(i[self.ex]), i[self.ey] - 1][0], px_im[(i[self.ex]), i[self.ey] - 1][1], px_im[(i[self.ex]),  i[self.ey] - 1][2], 'RGB'), stroke_width=2.5))
                            count_1 += 1
                self.loadingStatus(0, 100, y, n_hy, "Drawing Shape Line")
        dwg.save()