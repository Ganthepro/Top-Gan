from upscale import upscale
from vector import vector
from models import models
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Top Gan')
        self.window.minsize(width=600, height=600)
        self.window.maxsize(width=600, height=600)
        self.filename_history = ''
        self.interruptStatus = False
        self.stop_button = tk.Button(
            master=self.window, text='Cancel')
        self.shape_line_cheak_box_var = tk.IntVar()
        self.drawing_lines_cheak_box_var = tk.IntVar()
        self.stl_wall_height = tk.Entry(master=self.window)
        self.stl_wall_height_lable = tk.Label(
            master=self.window, text='Wall height :')
        self.stl_width = tk.Entry(master=self.window)
        self.stl_width_lable = tk.Label(
            master=self.window, text='Wall Thickness :')
        self.stl_base_wall_height = tk.Entry(master=self.window)
        self.stl_base_wall_height_lable = tk.Label(
            master=self.window, text='Base height :')
        self.stl_apply = tk.Button(master=self.window, text='STL', width=3)
        self.gcode_apply = tk.Button(
            master=self.window, text='GCODE', width=5)  # ทำต่อ
        self.title_lable = tk.Label(
            master=self.window, text='Import Picture', font=('Bold', 20))
        self.title_lable.pack()
        self.importPic_button = tk.Button(
            master=self.window, text='Upload', command=self.importPic)
        self.importPic_button.pack()
        self.file_locate_lable = tk.Label(
            master=self.window, text='*All file will be save in the program directory.*')
        self.file_locate_lable.place(y=390, x=10)
        self.dev_by_lable = tk.Label(
            master=self.window, text='*COPYRIGHT © Tamtikorn 2022. All Right Reserved.*')
        self.dev_by_lable.place(y=390, x=317)
        self.scale_lable = tk.Label(master=self.window, text='Scale :')
        self.scale_lable.place(x=120, y=440)
        self.shape_line_cheak_box = tk.Checkbutton(
            master=self.window, text='Anti-Aliasing', variable=self.shape_line_cheak_box_var)
        self.shape_line_cheak_box.place(x=170, y=460)
        self.drawing_lines_cheak_box = tk.Checkbutton(
            master=self.window, text='Drawing Line(For Upscale(Color),To SGV and To PDF)', variable=self.drawing_lines_cheak_box_var)
        self.drawing_lines_cheak_box.place(x=265, y=460)
        self.scale_entry = tk.Entry(master=self.window)
        self.scale_entry.place(x=160, y=440)
        self.save_filename_lable = tk.Label(
            master=self.window, text='Filename :')
        self.save_filename_lable.place(x=290, y=440)
        self.save_filename_entry = tk.Entry(master=self.window)
        self.save_filename_entry.place(x=350, y=440)
        self.threshold_lable = tk.Label(
            master=self.window, text="Threshold Value :")
        self.threshold_entry = tk.Entry(master=self.window)
        self.stl_convert_button = tk.Button(
            master=self.window, text='To'+'\n' + '3D-Printer', command=self.to3D, width=8, height=7)
        self.stl_convert_button.place(x=600 - 275 + 70, y=483)
        self.sgv_convert_button = tk.Button(
            master=self.window, text='To SVG', command=self.toSVG, width=8, height=7)
        self.sgv_convert_button.place(x=505 - 245 + 70, y=483)
        self.pdf_convert_button = tk.Button(
            master=self.window, text='To PDF', command=self.toPDF, width=8, height=7)
        self.pdf_convert_button.place(x=410 - 215 + 70, y=483)
        self.dxf_convert_button = tk.Button(
            master=self.window, text='To DXF', command=self.toDXF, width=8, height=7)
        self.dxf_convert_button.place(x=315 - 185 + 70, y=483)
        self.up_scale_line_convert_button = tk.Button(
            master=self.window, text='Upscale' + '\n' + '(Line Only)', command=self.upscaleLine, width=8, height=7)
        self.up_scale_line_convert_button.place(x=220 - 155 + 70, y=483)
        self.up_scale_color_convert_button = tk.Button(
            master=self.window, text='Upscale'+'\n'+'(Color)', command=self.upscaleColor, width=8, height=7)
        self.up_scale_color_convert_button.place(x=125 - 125 + 70, y=483)
        self.real_pic_stl_button = tk.Button(master=self.window, text='To'+'\n' + '3D-Printer' +
                                             '\n' + '(Non-'+'\n' + 'Digital art)', command=self.to3D_real, width=8, height=7)
        self.real_pic_stl_button.place(x=600 - 210 + 70, y=483)
        self.window.mainloop()

    def importPic(self):
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
        if self.filename_history == '':
            self.filename_history = filename
            image = ImageTk.PhotoImage(img)
        elif self.filename_history != '' and self.filename_history != filename:
            self.filename_history = filename
            image = ImageTk.PhotoImage(img)
            print('Selected:', filename)
        image_lable = tk.Label(master=self.window, image=image)
        image_lable.place(x=150, y=80)

    def clearWindow(self):
        self.threshold_entry.place_forget()
        self.threshold_lable.place_forget()
        self.scale_entry.place(x=160, y=440)
        self.scale_lable.place(x=120, y=440)
        self.save_filename_entry.place(x=350, y=440)
        self.save_filename_lable.place(x=290, y=440)
        self.stl_apply.place_forget()
        self.gcode_apply.place_forget()
        self.stl_base_wall_height.place_forget()
        self.stl_base_wall_height_lable.place_forget()
        self.stl_wall_height.place_forget()
        self.stl_wall_height_lable.place_forget()
        self.stl_width.place_forget()
        self.stl_width_lable.place_forget()
        self.gcode_apply.place_forget()
        self.stl_apply.place_forget()

    def upscaleSetup(self, realpic: bool, fline: bool, scale):
        try:
            self.stop_button.place(x=500, y=20)
            up = upscale(scale, self.filename_history, realpic,
                         self.title_lable, self.window, self.stop_button)
            if self.shape_line_cheak_box_var.get() == 1:
                res = up.anti_aliasing(fline)
            else:
                res = up.no_anti_aliasing()
            if res:
                return True
            else:
                return up
        except:pass

    def upscaleColor(self):
        try:
            self.clearWindow()
            up = self.upscaleSetup(False, True, int(self.scale_entry.get()))
            if up != True:
                if self.drawing_lines_cheak_box_var.get() == 1:
                    res = up.drawColor(True)
                else:
                    res = up.drawColor(False)
                if res != True:
                    up.showPic()
                    up.savePic(str(self.save_filename_entry.get())) 
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def upscaleLine(self):
        try:
            self.clearWindow()
            up = self.upscaleSetup(False, True, int(self.scale_entry.get()))
            if up != True:
                res = up.drawLine()
                if res != True:
                    up.showPic()
                    up.savePic(str(self.save_filename_entry.get())) 
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def toPDF(self):
        try:
            self.clearWindow()
            if self.drawing_lines_cheak_box_var.get() == 0:
                up = self.upscaleSetup(False, False, int(self.scale_entry.get()))
            else:
                up = self.upscaleSetup(False, True, int(self.scale_entry.get()))
            if up != True:
                vec = vector(self.title_lable, self.window, self.stop_button)
                res = up.drawColor(False)
                if res != True:
                    if self.drawing_lines_cheak_box_var.get() == 1:
                        vec.convertPDF(res, str(
                            self.save_filename_entry.get()), True, up.getVec(), int(self.scale_entry.get()))
                    else:
                        vec.convertPDF(res, str(
                            self.save_filename_entry.get()), False, up.getVec(), int(self.scale_entry.get()))
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def toSVG(self):
        try:
            self.clearWindow()
            up = self.upscaleSetup(False, True, int(self.scale_entry.get()))
            if up != True:
                vec = vector(self.title_lable, self.window, self.stop_button)
                res = up.drawColor(False)
                if res != True:
                    if self.drawing_lines_cheak_box_var.get() == 1:
                        vec.convertSVG(res, up.getVec(), str(
                            self.save_filename_entry.get()), int(self.scale_entry.get()), True, up.AA)
                    else:
                        vec.convertSVG(res, up.getVec(), str(
                            self.save_filename_entry.get()), int(self.scale_entry.get()), False, up.AA)
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def toDXF(self):
        try:
            self.clearWindow()
            up = self.upscaleSetup(False, True, int(self.scale_entry.get()))
            if up != True:
                vec = vector(self.title_lable, self.window, self.stop_button)
                vec.convertDXF(up.getVec(), str(self.save_filename_entry.get()))
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def toSTL(self, realpic: bool):
        try:
            self.clearWindow()
            up = self.upscaleSetup(realpic, False, 1)
            if up != True:
                md = models(self.title_lable, self.window, self.stop_button)
                md.convertSTL(float(self.stl_base_wall_height.get()), float(self.stl_wall_height.get()), float(
                    self.stl_width.get()), float(self.scale_entry.get()), str(self.save_filename_entry.get()), up.getVec(), up.getSize())
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def toGCODE(self, realpic: bool):
        try:
            self.clearWindow()
            up = self.upscaleSetup(realpic, True, 1)
            if up != True:
                md = models(self.title_lable, self.window, self.stop_button)
                md.convertGCODE(float(self.stl_base_wall_height.get()), float(self.stl_wall_height.get()), float(
                    self.stl_width.get()), float(self.scale_entry.get()), str(self.save_filename_entry.get()), up.getVec(), up.getSize())
        except:pass
        self.title_lable.configure(text="Import Picture")
        self.stop_button.place_forget()

    def to3D(self):
        self.clearWindow()
        self.scale_entry.place(x=160, y=440)
        self.scale_lable.place(x=120, y=440)
        self.save_filename_entry.place(x=350, y=440)
        self.save_filename_lable.place(x=290, y=440)
        self.stl_wall_height.place(x=85, y=415)
        self.stl_wall_height_lable.place(x=10, y=415)
        self.stl_width.place(x=270, y=415)
        self.stl_width_lable.place(x=175, y=415)
        self.scale_lable.configure(text='Scale :')
        self.scale_lable.place(x=100)
        self.stl_base_wall_height_lable.place(x=370, y=415)
        self.stl_base_wall_height.place(x=450, y=415)
        self.stl_apply.place(x=505, y=435)
        self.stl_apply.configure(command=lambda:self.toSTL(False))
        self.gcode_apply.place(x=543, y=435)
        self.gcode_apply.configure(command=lambda:self.toGCODE(False))

    def to3D_real(self):
        self.clearWindow()
        self.stl_wall_height.place(x=85, y=415)
        self.stl_wall_height_lable.place(x=10, y=415)
        self.stl_width.place(x=270, y=415)
        self.stl_width_lable.place(x=175, y=415)
        self.scale_lable.configure(text='Scale :')
        self.scale_lable.place(x=5)
        self.scale_entry.place(x=45)
        self.stl_base_wall_height_lable.place(x=370, y=415)
        self.stl_base_wall_height.place(x=450, y=415)
        self.stl_apply.place(x=505, y=435)
        self.stl_apply.configure(command=lambda:self.toSTL(True))
        self.gcode_apply.place(x=543, y=435)
        self.gcode_apply.configure(command=lambda:self.toGCODE(True))
        self.threshold_lable.place(x=280, y=440)
        self.threshold_entry.place(x=375, y=440)
        self.save_filename_lable.configure(text='Filename :')
        self.save_filename_lable.place(x=170-40)
        self.save_filename_entry.place(x=230-40)

    def interrupt(self):
        self.interruptStatus = True

    def updateLoadingLable(self, lable: str):
        self.title_lable.configure(text=lable)

gui = window()