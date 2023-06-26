from stl import mesh
import numpy as np
import math
import pygcode

class models:
    def __init__(self, lable, window, interruptBtn):
        if lable != None and window != None and interruptBtn != None: 
            self.label = lable
            self.window = window
            self.interruptBtn = interruptBtn
            self.interruptBtn.configure(command=self.interruptFunc)
        self.sx, self.sy, self.ex, self.ey = 1, 2, 3, 4
        self.interrupt = False

    def interruptFunc(self):
        self.interrupt = True

    def loadingStatus(self, start: int, end: int, num: int, maxNum: int, text: str):
        try:
            if self.interrupt == True:
                self.interrupt = False
                raise Exception(True)
            load = "{:.2f}".format(start + ((num * end) / maxNum))
            self.label.configure(text=f"{text} ({load}%)")
            self.window.update()
        except:pass

    def convertSTL(self, base_wall_height: float, wall_wall_height: float, wall_thickness: float, stl_scale: float, fname: str, vec: list, size: tuple):
        multi_vertices = []
        faces = []
        scale = 1
        self.n_wx, self.n_hy = size
        for k, i in enumerate(vec):
            if i[self.sy] == i[self.ey]:
                p1 = [i[self.sx] * scale / 1 * stl_scale + 20, i[self.sy] *
                      scale / 1 * stl_scale + 20, base_wall_height]  # ---
                p2 = [i[self.ex] * scale / 1 * stl_scale + 20, i[self.ey] *
                      scale / 1 * stl_scale + 20, base_wall_height]  # +--
                p3 = [i[self.ex] * scale / 1 * stl_scale + 20, (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20,
                      base_wall_height]  # ++-
                p4 = [i[self.sx] * scale / 1 * stl_scale + 20, (i[self.sy] * scale / 1) * stl_scale + wall_thickness + 20,
                      base_wall_height]  # -+-
                p5 = [i[self.sx] * scale / 1 * stl_scale + 20, i[self.sy] * scale / 1 * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # --+
                p6 = [i[self.ex] * scale / 1 * stl_scale + 20, i[self.ey] * scale / 1 * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # +-+
                p7 = [i[self.ex] * scale / 1 * stl_scale + 20, (i[self.ey] * scale / 1 * stl_scale) + wall_thickness + 20,
                      base_wall_height + wall_wall_height]  # +++
                p8 = [i[self.sx] * scale / 1 * stl_scale + 20, (i[self.sy] * scale / 1 * stl_scale) + wall_thickness + 20,
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
                vec.pop(vec.index(i))
            self.loadingStatus(0, 25, k, len(vec), "Creating STL")
        for k, i in enumerate(vec):
            if i[self.sx] == i[self.ex]:
                p1 = [(i[self.sx] * scale / 1) * stl_scale + 20, (i[self.sy] * scale / 1) * stl_scale + 20,
                      base_wall_height]  # ---
                p2 = [(i[self.sx] * scale / 1) * stl_scale + wall_thickness + 20, (i[self.sy] * scale / 1) * stl_scale + 20,
                      base_wall_height]  # +--
                p3 = [(i[self.ex] * scale / 1) * stl_scale + wall_thickness + 20,
                      (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20, base_wall_height]  # ++-
                p4 = [(i[self.ex] * scale / 1) * stl_scale + 20, (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20,
                      base_wall_height]  # -+-
                p5 = [(i[self.sx] * scale / 1) * stl_scale + 20, (i[self.sy] * scale / 1) * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # --+
                p6 = [(i[self.sx] * scale / 1) * stl_scale + wall_thickness + 20, (i[self.sy] * scale / 1) * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # +-+
                p7 = [(i[self.ex] * scale / 1) * stl_scale + wall_thickness + 20,
                      (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20, base_wall_height + wall_wall_height]  # +++
                p8 = [(i[self.ex] * scale / 1) * stl_scale + 20, (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20,
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
                p1 = [i[self.sx] * scale / 1 * stl_scale + 20, i[self.sy] *
                      scale / 1 * stl_scale + 20, base_wall_height]  # ---
                p2 = [i[self.ex] * scale / 1 * stl_scale + 20, i[self.ey] *
                      scale / 1 * stl_scale + 20, base_wall_height]  # +--
                p3 = [i[self.ex] * scale / 1 * stl_scale + 20, (i[self.ey] * scale / 1) * stl_scale + wall_thickness + 20,
                      base_wall_height]  # ++-
                p4 = [i[self.sx] * scale / 1 * stl_scale + 20, (i[self.sy] * scale / 1) * stl_scale + wall_thickness + 20,
                      base_wall_height]  # -+-
                p5 = [i[self.sx] * scale / 1 * stl_scale + 20, i[self.sy] * scale / 1 * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # --+
                p6 = [i[self.ex] * scale / 1 * stl_scale + 20, i[self.ey] * scale / 1 * stl_scale + 20,
                      base_wall_height + wall_wall_height]  # +-+
                p7 = [i[self.ex] * scale / 1 * stl_scale + 20, (i[self.ey] * scale / 1 * stl_scale) + wall_thickness + 20,
                      base_wall_height + wall_wall_height]  # +++
                p8 = [i[self.sx] * scale / 1 * stl_scale + 20, (i[self.sy] * scale / 1 * stl_scale) + wall_thickness + 20,
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
            self.loadingStatus(25, 75, k, len(vec), "Creating STL")
        p1 = [19, 20, 0]  # ---
        p2 = [(self.n_wx * stl_scale) + 20, 20, 0]  # +--
        p3 = [(self.n_wx * stl_scale) + 20,
              (self.n_hy * stl_scale) + 21, 0]  # ++-
        p4 = [19, (self.n_hy * stl_scale) + 21, 0]  # -+-
        p5 = [19, 20, base_wall_height]  # --+
        p6 = [(self.n_wx * stl_scale) + 20, 20, base_wall_height]  # +-+
        p7 = [(self.n_wx * stl_scale) + 20, (self.n_hy * stl_scale) +
              21, base_wall_height]  # +++
        p8 = [19, (self.n_hy * stl_scale) + 21, base_wall_height]  # -++
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
        multi_vertices_np = np.array(faces)
        surface = mesh.Mesh(
            np.zeros(multi_vertices_np.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                surface.vectors[i][j] = multi_vertices_np[i][j]
        surface.save(f'{fname}.stl')

    def convertGCODE(self, base_wall_height: float, wall_wall_height: float, wall_thickness: float, scale: float, fname: str, vec: list, size: tuple):
        n_vec = []
        scale_1 = 2
        semi_vec = []
        small_vec = []
        end_vec = ['', '']
        for k, i in enumerate(vec):
            o_sx, o_sy = i[self.sx] - 1, i[self.sy]
            n_sx_r, n_sy_r = i[self.sx], i[self.sy]
            for n in vec:
                # X เปลื่ยน Y เท่า
                if (o_sx + 1 == n_sx_r and n_sx_r == n[self.sx]) and (o_sy == n_sy_r and n_sy_r == n[self.sy]) and n[self.sy] == n[self.ey]:
                    o_sx += 1
                    n_sx_r += 1
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[self.sx] - semi_vec[len(semi_vec) - 1][self.sx] == 1 and n[self.ex] - semi_vec[len(semi_vec) - 1][self.ex] == 1 and n[self.ey] == semi_vec[len(semi_vec) - 1][self.ey] and n[self.sy] == semi_vec[len(semi_vec) - 1][self.sy]:
                        semi_vec.append(n)
                    else:
                        if semi_vec[len(semi_vec) - 1][3] == end_vec[0] and semi_vec[len(semi_vec) - 1][4] == end_vec[1]:
                            pass
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                            end_vec[0] = semi_vec[len(semi_vec) - 1][3]
                            end_vec[1] = semi_vec[len(semi_vec) - 1][4]
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
            self.loadingStatus(0, 25, k, len(vec), "Linking Line")
        small_vec.clear()
        semi_vec.clear()
        end_vec = []
        for k, i in enumerate(vec):
            o_sx, o_sy = i[self.sx], i[self.sy] - 1
            n_sx_d, n_sy_d = i[self.sx], i[self.sy]
            for n in vec:
                # X เท่า Y เปลื่ยน
                if (o_sx == n_sx_d and n_sx_d == n[self.sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[self.sy]) and n[self.sx] == n[self.ex]:
                    o_sy += 1
                    n_sy_d += 1
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[self.sy] - semi_vec[len(semi_vec) - 1][self.sy] == 1 and n[self.ey] - semi_vec[len(semi_vec) - 1][self.ey] == 1 and n[self.ex] == semi_vec[len(semi_vec) - 1][self.ex] and n[self.sx] == semi_vec[len(semi_vec) - 1][self.sx]:
                        semi_vec.append(n)
                    else:
                        for v in end_vec:
                            if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                                break
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                            end_vec.append(
                                [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
            self.loadingStatus(25, 25, k, len(vec), "Linking Line")
        end_vec.clear()
        semi_vec.clear()
        for k, i in enumerate(vec):
            o_sx, o_sy = i[self.sx] - 1, i[self.sy] - 1
            n_sx_d, n_sy_d = i[self.sx], i[self.sy]
            for n in vec:  # แก้ต่อ
                if (o_sx + 1 == n_sx_d and n_sx_d == n[self.sx]) and (o_sy + 1 == n_sy_d and n_sy_d == n[self.sy]) and n[self.sx] < n[self.ex] and n[self.sy] < n[self.ey]:
                    o_sx += 1
                    o_sy += 1
                    n_sx_d += 1
                    n_sy_d += 1
                    if len(semi_vec) == 0:
                        semi_vec.append(n)
                    elif n[self.sx] - semi_vec[len(semi_vec) - 1][self.sx] == 1 and n[self.sy] - semi_vec[len(semi_vec) - 1][self.sy] == 1 and n[self.ex] - semi_vec[len(semi_vec) - 1][self.ex] == 1 and n[self.ey] - semi_vec[len(semi_vec) - 1][self.ey] == 1:
                        semi_vec.append(n)
                    else:
                        for v in end_vec:
                            if semi_vec[len(semi_vec) - 1][3] == v[0] and semi_vec[len(semi_vec) - 1][4] == v[1]:
                                break
                        else:
                            n_vec.append([semi_vec[0][0], semi_vec[0][1], semi_vec[0][2], semi_vec[len(
                                semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                            end_vec.append(
                                [semi_vec[len(semi_vec) - 1][3], semi_vec[len(semi_vec) - 1][4]])
                        small_vec.clear()
                        semi_vec.clear()
                        semi_vec.append(n)
            self.loadingStatus(50, 25, k, len(vec), "Linking Line")
        semi_vec.clear()
        small_vec.clear()
        break_point = [0]
        end_vec.clear()
        for k, n in enumerate(vec):  # แก้ต่อ
            if n[self.sx] < n[self.ex] and n[self.sy] > n[self.ey]:
                if len(semi_vec) == 0:
                    semi_vec.append(n)
                elif len(semi_vec) > 0:
                    while True:
                        for e in vec:
                            if e[self.sx] - semi_vec[len(semi_vec) - 1][self.sx] == 1 and semi_vec[len(semi_vec) - 1][self.sy] - e[self.sy] == 1 and e[self.ex] - semi_vec[len(semi_vec) - 1][self.ex] == 1 and semi_vec[len(semi_vec) - 1][self.ey] - e[self.ey] == 1:
                                semi_vec.append(e)
                                break_point[0] = 0
                                break
                            break_point[0] = 1
                        if break_point[0] == 1:
                            break
                    if len(semi_vec) == 1:
                        end_vec.append(semi_vec[0])
                    else:
                        for v in end_vec:
                            if v in semi_vec:
                                small_vec.append(
                                    [semi_vec[0], v, len(semi_vec)])
                    semi_vec.clear()
                    semi_vec.append(n)
            self.loadingStatus(75, 10, k, len(vec), "Linking Line")
        semi_vec.clear()
        semi_vec1 = []
        for v in end_vec:
            for i in small_vec:
                if v == i[1]:
                    semi_vec.append(i)
            if len(semi_vec) == 0:
                semi_vec1.append(v)
            else:
                n_vec.append([semi_vec[len(semi_vec) - 1][0][0], semi_vec[len(semi_vec) - 1][0][self.sx], semi_vec[len(semi_vec) - 1][0][self.sy], semi_vec[len(
                    semi_vec) - 1][1][self.ex], semi_vec[len(semi_vec) - 1][1][self.ey], semi_vec[len(semi_vec) - 1][0][5], semi_vec[len(semi_vec) - 1][0][6]])
            semi_vec.clear()
        for i in semi_vec1:
            n_vec.append(i)
        width = [wall_thickness - 1]  # wall thickness
        semi_vec.clear()
        semi_vec1.clear()
        if width[0] > 1:
            num_minus = [0, 0]  # แก้ต่อโดยเพิ่มจำนวนเรื่อยๆ
            num_plus = [0, 0]
            for v in range(width[0]):
                if v % 2 == 0:
                    num_plus[0] += 1
                    num_plus[1] += 0.2
                    for k, i in enumerate(n_vec):
                        if (i[self.sx] < i[self.ex] and i[self.sy] > i[self.ey]) or (i[self.sx] < i[self.ex] and i[self.sy] < i[self.ey]) or (i[self.sx] == i[self.ex] and i[self.sy] != i[self.ey]):
                            semi_vec.append([k, (i[self.sx]*scale_1)*scale_1+num_plus[0], (i[self.sy]*scale_1)
                                            * scale_1, (i[self.ex]*scale_1)*scale_1+num_plus[0], (i[self.ey]*scale_1)*scale_1])
                            semi_vec1.append(
                                [k, i[self.sx]+num_plus[1], i[self.sy], i[self.ex]+num_plus[1], i[self.ey]])
                        elif (i[self.sx] != i[self.ex] and i[self.sy] == i[self.ey]):
                            semi_vec.append([k, (i[self.sx]*scale_1)*scale_1, (i[self.sy]*scale_1)*scale_1 +
                                            num_plus[0], (i[self.ex]*scale_1)*scale_1, (i[self.ey]*scale_1)*scale_1+num_plus[0]])
                            semi_vec1.append(
                                [k, i[self.sx], i[self.sy]-num_plus[1], i[self.ex], i[self.ey]-num_plus[1]])
                else:
                    num_minus[0] -= 1
                    num_minus[1] -= 0.2
                    for k, i in enumerate(n_vec):
                        if (i[self.sx] < i[self.ex] and i[self.sy] > i[self.ey]) or (i[self.sx] < i[self.ex] and i[self.sy] < i[self.ey]) or (i[self.sx] == i[self.ex] and i[self.sy] != i[self.ey]):
                            semi_vec.append([k, (i[self.sx]*scale_1)*scale_1+num_minus[0], (i[self.sy]*scale_1)
                                            * scale_1, (i[self.ex]*scale_1)*scale_1+num_minus[0], (i[self.ey]*scale_1)*scale_1])
                            semi_vec1.append(
                                [k, i[self.sx]+num_minus[1], i[self.sy], i[self.ex]+num_minus[1], i[self.ey]])
                        elif (i[self.sx] != i[self.ex] and i[self.sy] == i[self.ey]):
                            semi_vec.append([k, (i[self.sx]*scale_1)*scale_1, (i[self.sy]*scale_1)*scale_1 +
                                            num_minus[0], (i[self.ex]*scale_1)*scale_1, (i[self.ey]*scale_1)*scale_1+num_minus[0]])
                            semi_vec1.append(
                                [k, i[self.sx], i[self.sy]-num_minus[1], i[self.ex], i[self.ey]-num_minus[1]])
                self.loadingStatus(85, 15, v, width[0], "Linking Line")
        for i in semi_vec1:
            n_vec.append(i)
        eshift = 0.03320
        wx, hy = size
        print(wx*scale, hy*scale)
        with open(f'{fname}.gcode', 'w') as f:
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
            for i in range(int(base_wall_height)):
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
                self.loadingStatus(0, 50, i, int(
                    base_wall_height), "Creating GCODE")
                z[0] += 0.2
                f.write('G0 F3000 Z'+str(z[0])+'\n')
            f.write('G92 E0\n')
            f.write('G92 E0\n')
            e[0] = 0.0
            height = int(wall_wall_height)
            for v in range(height):
                for k, i in enumerate(n_vec):
                    if i[self.sx] < i[self.ex] and i[self.sy] > i[self.ey]:
                        f.write('G0 X' + str(i[self.sx] * scale + 30) + ' Y' +
                                str(i[self.sy] * scale + 30) + ' F5000.0'+'\n')
                        e[0] = e[0] + (math.sqrt(pow((i[self.sx] * scale + 30)-(i[self.ex] * scale + 30), 2)+pow(
                            (i[self.sy] * scale + 30)-(i[self.ey] * scale + 30), 2))*eshift)
                        f.write('G1 X' + str(i[self.ex] * scale + 30) + ' Y' + str(
                            i[self.ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                        f.write('G1' + ' F1500.0 ' + 'E' +
                                str(e[0] - 6.5) + '\n')
                    else:
                        f.write('G0 X' + str(i[self.sx] * scale + 30) + ' Y' +
                                str(i[self.sy] * scale + 30) + ' F5000.0'+'\n')
                        e[0] = e[0] + (math.sqrt(pow((i[self.sx] * scale + 30)-(i[self.ex] * scale + 30), 2)+pow(
                            (i[self.ey] * scale + 30)-(i[self.sy] * scale + 30), 2))*eshift)
                        f.write('G1 X' + str(i[self.ex] * scale + 30) + ' Y' + str(
                            i[self.ey] * scale + 30) + ' F1500.0 ' + 'E' + str(e[0]) + '\n')
                        f.write('G1' + ' F1500.0 ' + 'E' +
                                str(e[0] - 6.5) + '\n')
                self.loadingStatus(50, 100, v, height, "Creating GCODE")
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
            f.close()
            
    def twoColor_gcode(self, in_fname: str, out_fname: str):
        with open(in_fname, 'r+') as f:
            texts = f.readlines()
            flag_mash = False
            flag_type = False
            base_line = ""
            base_max_layer = 0 
            for t in texts:
                if base_line != "":
                    if base_line in t:
                        base_max_layer += 1
                else:
                    if "MESH" in t:
                        flag_mash = True
                    if "TYPE" in t and t != ";TYPE:SKIRT\n":
                        flag_type = True
                    if flag_mash and flag_type and "X" in t and "Y" in t:
                        for i in t.removesuffix("\n"):
                            if i != "X":
                                t = t.removeprefix(i)
                            if i == "E":
                                t = t.replace(t[t.index(i):-1],"")
                                break
                        base_line = t.removesuffix("\n")
            flag_value = {"G1" : False,"z" : False,"e" : False}
            value = {"G1" : "","z" : "","e" : ""}
            for i in range(texts.index(f";LAYER:{base_max_layer + 2}\n") - 1,0,-1):
                if "X" in texts[i].removesuffix("\n") and "Y" in texts[i].removesuffix("\n") and not flag_value["G1"]: 
                    flag_value["G1"] = True
                    try:
                        value["G1"] = texts[i].removeprefix(texts[i][0:texts[i].index("F")])
                    except:
                        value["G1"] = texts[i].removeprefix(texts[i][0:texts[i].index("X")])
                if "Z" in texts[i].removesuffix("\n") and not flag_value["z"]:
                    flag_value["z"] = True
                    value["z"] = texts[i][texts[i].index("Z"):-1]
                if "E" in texts[i].removesuffix("\n") and ("G1" in texts[i].removesuffix("\n") or "G0" in texts[i].removesuffix("\n")) and not flag_value["e"]:
                    flag_value["e"] = True
                    value["e"] = texts[i][texts[i].index("E"):-1]
                for v in flag_value.values():
                    if v == False:
                        flag = False
                        break
                    else:
                        flag = True
                if flag:
                    break
            x = value["z"][value["z"].index("Z") + 1:-1] + value["z"][-1]
            script = ["M83\n",f"G1 F300 Z{float(x) + 1}\n","G1 F9000 X190 Y190\n"
                    ,"G1 F300 Z15\n","M104 S180\n","M300\n","M0\n","G4 S180\n","M109 S200\n",f"G1 F300 {value['z']}\n"
                    ,f"G1 {value['G1']}",f"G1 F300 {value['z']}\n","G1 F1500\n","M82\n",f"G92 {value['e']}\n"]
            for i in script:
                print(i)
                texts.insert(texts.index(f";LAYER:{base_max_layer + 2}\n"),i)
                
        with open(f"{out_fname}.gcode", "w") as file:
            for i,line in enumerate(texts):
                file.write(line)
                self.loadingStatus(0, 100, i, len(texts), "Converting")

