import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,font,colorchooser
from PIL import ImageGrab, ImageTk, Image
from resource import logo_ico
import base64

class MainWindow(object):
    def __init__(self):
        # 定义展示的窗口大小，固定比例 2.35:1
        self.cv_width = 940
        self.cv_height = 400

        # 用户导入的图片，文字信息
        self.originimage = None
        self.resizeimage = None
        self.tk_image = None

        self.curImageSize = 300
        self.curImageCenterPos = (self.cv_width/2,self.cv_height/2)

        self.curTextPos = (self.cv_width/2,self.cv_height/2)

        # canvas 上的索引
        self.canvas_imgIndex = None
        self.canvas_textIndex = None
        self.rulers = []

        self.__createMainwinow()

    def show(self):
        self.root.mainloop()

    def __createMainwinow(self):
        self.root = tk.Tk()
        self.root.iconphoto(True, ImageTk.PhotoImage(data=base64.b64decode(logo_ico)))
        self.root.title("一键生成微信公众号封面")
        self.root.geometry('960x520')
        self.root.resizable(0,0)

        self.__createInfoframe()
        self.__createMoveControlFrame()

        # 创建一个Canvas，设置其背景色为白色
        self.canvas = tk.Canvas(self.root, height=self.cv_height, width=self.cv_width, highlightthickness=0, bg = 'white')
        self.canvas.pack()

        self.__createRuler()

    def __createInfoframe(self):
        self.infoframe = ttk.Frame(self.root)
        self.infoframe.pack(anchor='w', padx=10, pady=5)

        self.element_frame = ttk.Frame(self.infoframe)
        self.element_frame.pack(side='left')

        # 图片信息
        tk.Label(self.element_frame, text="图片地址: ").grid(row=0,column=0)
        self.picpath = tk.StringVar()
        ttk.Entry(self.element_frame, textvariable=self.picpath, width = 30, state="readonly").grid(row=0,column=1)
        ttk.Button(self.element_frame, text ="打开图片", width = 8, takefocus=False, command = self.__openLocalImage).grid(row=0,column=2,padx=5,pady=5)
        ttk.Button(self.element_frame, text ="放大图片", width = 8, takefocus=False, command = self.__zoomUpImage).grid(row=0,column=3)
        ttk.Button(self.element_frame, text ="缩小图片", width = 8, takefocus=False, command = self.__zoomDownImage).grid(row=0,column=4,padx=5)

        # 用户输入的字体
        ttk.Label(self.element_frame, text="文字内容: ").grid(row=1,column=0)
        self.var_text = tk.StringVar()
        self.var_text.trace_add("write", self.__FontChange)
        ttk.Entry(self.element_frame, textvariable=self.var_text, width = 30).grid(row=1,column=1)

        # 字体样式
        self.__createFontFamilyCombobox()

        # 展示详细编辑字体的 Frame
        self.font_frame = tk.Frame(self.element_frame)
        self.font_frame.grid(row=2,column=2,columnspan=3,sticky=tk.W,pady=5,padx=5)

        # 字体相关的设置，字体大小，加粗，斜体，下划线，删除线,颜色
        self.__createFontSizeCombobox(self.font_frame).pack(side='left')
        self.__createFontBoldCheckButton(self.font_frame).pack(side='left', padx=6)
        self.__createFontSlantCheckButton(self.font_frame).pack(side='left')
        self.__createFontUnderlineCheckButton(self.font_frame).pack(side='left',padx=6)
        self.__createFontOverstrikeCheckButton(self.font_frame).pack(side='left')

        self.color_button = tk.Button(self.font_frame, text ="", width = 3, background="#3C70C6",command = self.__ColorChange)
        self.color_button.pack(side='left',padx=6)

    # 控制移动部分
    def __createMoveControlFrame(self):
        self.moveframe = tk.Frame(self.infoframe)
        self.moveframe.pack(padx=50, pady=5)

        # 上下左右4个移动按钮
        ttk.Button(self.moveframe,text ="上", width = 2, takefocus=False, command = self.__moveUp).grid(row=0,column=1)
        ttk.Button(self.moveframe,text ="下", width = 2, takefocus=False, command = self.__moveDown).grid(row=2,column=1)
        ttk.Button(self.moveframe,text ="左", width = 2, takefocus=False, command = self.__moveLeft).grid(row=1,column=0,padx=3)
        ttk.Button(self.moveframe,text ="右", width = 2, takefocus=False, command = self.__moveRight).grid(row=1,column=2,padx=3)
        
        ttk.Label(self.moveframe, text="移动尺寸").grid(row=0,column=3, pady=5, padx=15)
        ttk.Label(self.moveframe, text="移动对象").grid(row=1,column=3)

        # 移动距离的下拉菜单
        self.var_movesize = tk.StringVar()
        self.movesize_combobox = ttk.Combobox(self.moveframe, textvariable=self.var_movesize)
        self.movesize_combobox['state'] = "readonly"        
        self.movesize_combobox['value'] = (1,5,10,20,30,50)
        self.movesize_combobox.current(1)
        self.movesize_combobox.grid(row=0,column=4,sticky = tk.W+tk.E)

        # 移动对象的下拉菜单
        self.var_moveobject = tk.StringVar()
        self.moveobject_combobox = ttk.Combobox(self.moveframe, textvariable=self.var_moveobject)
        self.moveobject_combobox['state'] = "readonly"  
        self.moveobjects = ("图片", "文字", "图片+文字")  
        self.moveobject_combobox['value'] = self.moveobjects
        self.moveobject_combobox.current(0)
        self.moveobject_combobox.grid(row=1,column=4,sticky = tk.W+tk.E)

        self.buttonframe = tk.Frame(self.moveframe)
        self.buttonframe.grid(row=2,column=4, sticky = tk.E)
        # 重置位置 和 保存图片 按钮
        ttk.Button(self.buttonframe,text ="重置位置", width = 8, takefocus=False, command = self.__resetPos).pack(side="left")
        ttk.Button(self.buttonframe,text ="保存图片", width = 8, takefocus=False, command = self.__saveImage).pack()

    # 标尺
    def __clearRuler(self):
        if self.rulers:
            for i in self.rulers:
                self.canvas.delete(i)

    def __createRuler(self):
        self.__clearRuler()

        # 绘制 1:1 的标尺， 记录标尺，在最后保存图片的时候清除
        self.rulers = []
        ruler_start = (self.cv_width-self.cv_height) / 2
        # 中央 1:1 的标尺
        self.rulers.append(self.canvas.create_line(ruler_start, 0, ruler_start, self.cv_height, dash=(4, 4)))
        self.rulers.append(self.canvas.create_line(self.cv_width-ruler_start, 0, self.cv_width-ruler_start, self.cv_height, dash=(4, 4)))

        # 防止过于靠边的标尺       
        self.rulers.append(self.canvas.create_line(self.cv_width/8, 0, self.cv_width/8, self.cv_height, dash=(4, 4)))
        self.rulers.append(self.canvas.create_line(self.cv_width*7/8, 0, self.cv_width*7/8, self.cv_height, dash=(4, 4)))

        # 中央水平的标尺
        self.rulers.append(self.canvas.create_line(0, self.cv_height/2, self.cv_width, self.cv_height/2, dash=(4, 4)))
        
    def __ColorChange(self):
        result = colorchooser.askcolor()
        if result[1]:
            self.color_button["background"] = result[1]
            self.__FontChange()


    def __FontChange(self, *args):
        # 删除旧的字体
        if self.canvas_textIndex :
            self.canvas.delete(self.canvas_textIndex)

        if self.var_text.get():
            f = font.Font(  family=self.var_fontfamily.get(), 
                            size=self.var_fontsize.get(),
                            weight="bold" if self.fontweight_status else "normal",
                            slant="italic" if self.fontslant_status else "roman",
                            underline=1 if self.fontunderline_status else 0,
                            overstrike=1 if self.fontoverstrike_status else 0 )
            self.canvas_textIndex = self.canvas.create_text(self.curTextPos[0],self.curTextPos[1],anchor="center", text=self.var_text.get(), font=f, fill = self.color_button["background"])
            self.__createRuler()

    # 字体样式
    def __createFontFamilyCombobox(self):
        self.var_fontfamily = tk.StringVar()
        self.var_fontfamily.trace_add("write", self.__FontChange)
        # 创建字体的下拉菜单
        self.fontfamily_combobox = ttk.Combobox(self.element_frame, textvariable=self.var_fontfamily)
        self.fontfamily_combobox['state'] = "readonly"
        # 获取当前系统中所有的字体，并筛选出首字母是中文的字体           
        list_families = []
        for i in font.families():
            if (i[0] != "@") and ('\u4e00' <= i[0] <= '\u9fff'):
                list_families.append(i)
        self.families = tuple(list_families)            
        self.fontfamily_combobox['value'] = self.families
        
        # 默认选用 微软雅黑字体
        try:
            currentindex = self.families.index("微软雅黑")
        except:
            currentindex = 0
        self.fontfamily_combobox.current(currentindex)
        self.fontfamily_combobox.grid(row=1,column=2, columnspan=3, sticky=tk.W+tk.E,padx=5)

    # 字体大小
    def __createFontSizeCombobox(self, parent):
        self.var_fontsize = tk.StringVar()
        self.var_fontsize.trace_add("write", self.__FontChange)
        # 创建字体的下拉菜单
        self.fontsize_combobox = ttk.Combobox(parent, width=5, textvariable=self.var_fontsize)
        self.fontsize_combobox['state'] = "readonly"
        self.tuple_size = (8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72)        
        self.fontsize_combobox['value'] = self.tuple_size
        currentindex = self.tuple_size.index(48)
        self.fontsize_combobox.current(currentindex)
        return self.fontsize_combobox

    def __changeFontweightStyle(self):
        if not self.fontweight_status:
            self.fontweight_checkbutton['style'] = 'check_bold.TButton'
        else:
            self.fontweight_checkbutton['style'] = 'bold.TButton'

        self.fontweight_status = bool(1-self.fontweight_status)

        self.__FontChange()

    # 粗体
    def __createFontBoldCheckButton(self, parent):
        self.fontweight_status = False
        ttkstyle = ttk.Style()
        ttkstyle.configure('bold.TButton', font=('宋体', 8, 'bold'))
        ttkstyle.configure('check_bold.TButton', font=('宋体', 8, 'bold'),background ="#0078D7")
        self.fontweight_checkbutton = ttk.Button(parent, text ="B", style='bold.TButton', width=2, takefocus=False,  command = self.__changeFontweightStyle)
        return self.fontweight_checkbutton
    
    def __changeFontSlantStyle(self):
        if not self.fontslant_status:
            self.fontslant_checkbutton['style'] = 'check_italic.TButton'
        else:
            self.fontslant_checkbutton['style'] = 'italic.TButton'

        self.fontslant_status = bool(1-self.fontslant_status)

        self.__FontChange()

    # 斜体
    def __createFontSlantCheckButton(self, parent):
        self.fontslant_status = False
        ttkstyle = ttk.Style()
        ttkstyle.configure('italic.TButton', font=('宋体', 8,'bold','italic') )
        ttkstyle.configure('check_italic.TButton', font=('宋体', 8,'bold','italic'),background ="#0078D7" )
        self.fontslant_checkbutton = ttk.Button(parent, text ="I", width=2, style='italic.TButton', takefocus=False, command = self.__changeFontSlantStyle)

        return self.fontslant_checkbutton

    def __changeFontUnderlineStyle(self):
        if not self.fontunderline_status:
            self.fontunderline_checkbutton['style'] = 'check_underline.TButton'
        else:
            self.fontunderline_checkbutton['style'] = 'underline.TButton'

        self.fontunderline_status = bool(1-self.fontunderline_status)
        self.__FontChange()

    # 下划线
    def __createFontUnderlineCheckButton(self, parent):
        self.fontunderline_status = False
        ttkstyle = ttk.Style()
        ttkstyle.configure('underline.TButton', font=('宋体', 8,'bold', "underline"))
        ttkstyle.configure('check_underline.TButton', font=('宋体', 8,'bold', "underline"), background ="#0078D7" )
        self.fontunderline_checkbutton = ttk.Button(parent, text ="U",width =2,  style='underline.TButton', takefocus=False, command = self.__changeFontUnderlineStyle)
        return self.fontunderline_checkbutton


    def __changeFontOverstrikeStyle(self):
        if not self.fontoverstrike_status:
            self.fontoverstrike_checkbutton['style'] = 'check_overstrike.TButton'
        else:
            self.fontoverstrike_checkbutton['style'] = 'overstrike.TButton'

        self.fontoverstrike_status = bool(1-self.fontoverstrike_status)
        self.__FontChange()

    # 删除线
    def __createFontOverstrikeCheckButton(self, parent):
        self.fontoverstrike_status = False
        ttkstyle = ttk.Style()
        ttkstyle.configure('overstrike.TButton', font=('宋体', 8, 'bold', "overstrike"))
        ttkstyle.configure('check_overstrike.TButton', font=('宋体', 8,'bold', "overstrike"),background ="#0078D7")
        self.fontoverstrike_checkbutton = ttk.Button(parent, text ="ab", style='overstrike.TButton', takefocus=False,  width =2, command = self.__changeFontOverstrikeStyle)
        return self.fontoverstrike_checkbutton

    def __clearImageInfo(self):
        del self.originimage
        del self.resizeimage
        del self.tk_image

        self.originimage = None
        self.resizeimage = None
        self.tk_image = None

    def __canvasShowImage(self):
        ratio = self.originimage.width/self.originimage.height
        if ratio > 1:
            self.resizeimage = self.originimage.resize((self.curImageSize, int(self.curImageSize/ratio)),Image.NEAREST)
        else :
            self.resizeimage = self.originimage.resize((int(self.curImageSize*ratio), self.curImageSize),Image.NEAREST)

        self.tk_image = ImageTk.PhotoImage(self.resizeimage)
        self.canvas_imgIndex = self.canvas.create_image(self.curImageCenterPos[0]-self.resizeimage.width/2, self.curImageCenterPos[1]-self.resizeimage.height/2, anchor ='nw', image=self.tk_image)
        self.__FontChange()
        self.__createRuler()


    def __openLocalImage(self):
        ftypes = [('png files', '*.png'), ('jpg files', '*.jpg'),  ('gif files', '*.gif')]
        file_path = filedialog.askopenfilename(title="选择背景图片", filetypes=ftypes )
        if file_path:
            self.picpath.set(file_path)
            if self.canvas_imgIndex:
                self.canvas.delete(self.canvas_imgIndex)

            self.__clearImageInfo()
            self.originimage = Image.open(file_path)
            self.__canvasShowImage()

    def __zoomUpImage(self):
        if not self.canvas_imgIndex:
            return

        self.canvas.delete(self.canvas_imgIndex)
        self.curImageSize += 20
        self.__canvasShowImage()

    def __zoomDownImage(self):
        if not self.canvas_imgIndex:
            return

        self.canvas.delete(self.canvas_imgIndex)
        self.curImageSize -= 20
        self.__canvasShowImage()

    def __moveUp(self):
        direction = "up"
        self.__move(direction)

    def __moveDown(self):
        direction = "down"
        self.__move(direction)

    def __moveLeft(self):
        direction = "left"
        self.__move(direction)
    
    def __moveRight(self):
        direction = "right"
        self.__move(direction)

    def __move(self, direction:str):
        if self.var_moveobject.get() == self.moveobjects[0]:
            self.__MoveImage(direction)
        elif self.var_moveobject.get() == self.moveobjects[1]:
            self.__MoveText(direction)
        else :
            self.__MoveImage(direction)
            self.__MoveText(direction)

    def __MoveImage(self, direction:str):
        if not self.canvas_imgIndex:
            return
        
        self.canvas.delete(self.canvas_imgIndex)

        step = int(self.var_movesize.get())
        if direction == "up" :   
            self.curImageCenterPos = (self.curImageCenterPos[0], self.curImageCenterPos[1]-step)
        elif direction == "down" :
            self.curImageCenterPos = (self.curImageCenterPos[0], self.curImageCenterPos[1]+step)
        elif direction == "left":
            self.curImageCenterPos = (self.curImageCenterPos[0]-step, self.curImageCenterPos[1])
        elif direction == "right":
            self.curImageCenterPos = (self.curImageCenterPos[0]+step, self.curImageCenterPos[1])
        else :
            self.curImageCenterPos = self.curImageCenterPos

        self.__canvasShowImage()

    def __MoveText(self, direction:str):
        if not self.canvas_textIndex:
            return
        self.canvas.delete(self.canvas_textIndex)

        step = int(self.var_movesize.get())
        if direction == "up" :   
            self.curTextPos = (self.curTextPos[0], self.curTextPos[1]-step)
        elif direction == "down" :
            self.curTextPos = (self.curTextPos[0], self.curTextPos[1]+step)
        elif direction == "left":
            self.curTextPos = (self.curTextPos[0]-step, self.curTextPos[1])
        elif direction == "right":
            self.curTextPos = (self.curTextPos[0]+step, self.curTextPos[1])
        else :
            self.curTextPos = self.curTextPos

        self.__FontChange()

    def __resetPos(self):
        self.curImageCenterPos = (self.cv_width/2,self.cv_height/2)
        if self.canvas_imgIndex:
            self.canvas.delete(self.canvas_imgIndex)
            self.__canvasShowImage()
        
        self.curTextPos = (self.cv_width/2,self.cv_height/2)
        if self.canvas_textIndex:
            self.canvas.delete(self.canvas_textIndex)
            self.__FontChange()

    def __saveImage(self):
        self.__clearRuler()
        self.canvas.update()
        # 获取初始位置
        x = self.root.winfo_rootx()+self.canvas.winfo_x()
        y = self.root.winfo_rooty()+self.canvas.winfo_y()
        # 获取窗口长宽
        width = x + self.canvas.winfo_width()
        height = y + self.canvas.winfo_height()
        size = (x,y,width,height)
        pic = ImageGrab.grab(size)
        pic.save("./cover.png")
        self.__createRuler()

if __name__ == '__main__':
    mainwindow = MainWindow()
    mainwindow.show()
