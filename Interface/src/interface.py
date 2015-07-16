##
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from tkinter.constants import DISABLED
from matplotlib import style
import numpy as np
import time
import tkinter as tk
from tkinter import ttk


voltage = [8.8, 8.9, 8.8, 9.0, 8.9, 9.2, 9.1, 9.0, 8.8]
current = [0.9, 0.8, 0.9, 1.0, 0.9, 1.2, 1.1, 1.2, 1.0]

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


f2 = Figure(figsize=(5,5), dpi=100)
a2 = f2.add_subplot(111)
x = np.arange(0, 5, 0.1);

class Param:
    m=1
    i=0

y = np.exp(Param.m*x)
a2.plot(x,y)

def animate(i):
    #pullData = open("sampleText.txt","r").read()
    #dataList = pullData.split('\n')
    data = [1, 2, 3, 2, 3, 2, 1, 3, 1, 1, 3, 2, 2, 1, 2, 2, 3, 1, 1, 3, 3, 1, 2, 3, 2, 1, 3, 3, 2, 3, 1, 1, 2, 2, 3,]

    yList = data[0+i:9+i]
    #xList = [9, 6, 8 ,5]
    xList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #for eachLine in dataList:
     #   if len(eachLine) > 1:
      #      x, y = eachLine.split(',')
       #     xList.append(int(x))
        #    yList.append(int(y))

    a.clear()
    a.plot(xList, yList)
    


            

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "SMASH Ground Station")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Read Me", command=lambda: self.show_frame(ReadMe))
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)
        
        
        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree,ReadMe):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Exponential Graph",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Information",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Real-time Graph",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()

class ReadMe(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)
        label = tk.Label(self, text="Read Me", font=LARGE_FONT)
        label.pack(pady=10)
        
        textReadMe = tk.Text(self,width=80,height=30)
        pullReadMe = open("ReadMe.txt","r").read()
        textReadMe.insert('1.0',pullReadMe)
        textReadMe.config(state=DISABLED)
        textReadMe.pack()
        
     
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Exponential Graph", font=LARGE_FONT)
        label.grid(row=0,column=0,columnspan=5 , sticky = "nsew")

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1,column=2,pady=10,padx=50,sticky = "nsew")
        
        
        
        
        self.functionEntry = ttk.Entry(self, text="a=?")
        self.functionEntry.grid(row=3,column=2,padx=10,sticky = "nsew")
         
        label2 = ttk.Label(self, text="y = exp(ax)", font=LARGE_FONT)
        label2.grid(row=3,column=1,padx=10,sticky = "nsew")

        
        self.canvas = FigureCanvasTkAgg(f2, self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid_forget()
        self.canvas.get_tk_widget().grid(row=4,column=0,columnspan=3,sticky = "nsew")


        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=5,column=0,columnspan=3,sticky = "nsew")
        
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()
        
        def changeParam():
            Param.m = float(self.functionEntry.get())
            y = np.exp(Param.m*x)
            a2.clear()
            a2.plot(x,y)
            self.canvas.draw()
            return
            
        button2 = ttk.Button(self,text="Calculate", 
                             command= changeParam )
        button2.grid(row=3,column=0,padx=10,sticky = "nsew")
        
    
        
        self.createFrame()
        #self.updateData()
        
        
    def createFrame(self):
        
        info_frame = tk.Frame(self)
        info_frame.grid(row=4,column=4,padx=20,sticky = "nsew")
        
    
        label_info = tk.Label(info_frame, text="Information", font=LARGE_FONT)
        label_info.grid(row=0,column=0,pady=10,columnspan=2,sticky = "nsew")
        
        
        output_time = tk.Label(info_frame)
        output_time.grid(row=1,column=1,pady=10,sticky = "nsew")
        
        
        output_current = tk.Label(info_frame)
        output_current.grid(row=2,column=1,pady=10,sticky = "nsew")
        
        output_voltage = tk.Label(info_frame)
        output_voltage.grid(row=3,column=1,pady=10,sticky = "nsew")
        
        label_time = tk.Label(info_frame, text="Time", font=14)
        label_time.grid(row=1,column=0,pady=10,sticky = "nsew")
        
        label_current = tk.Label(info_frame, text="Current", font=14)
        label_current.grid(row=2,column=0,pady=10,sticky = "nsew")
        
        label_voltage = tk.Label(info_frame, text="Voltage", font=14)
        label_voltage.grid(row=3,column=0,pady=10,sticky = "nsew")
        
        
        def updateData():
        
            if Param.i==8:
                Param.i=0
            now = time.strftime("%H:%M:%S")
            output_time.configure(text=now)
            output_voltage.configure(text=str(voltage[Param.i]))
            output_current.configure(text=str(current[Param.i]))
            Param.i += 1
            self.master.after(1000, updateData)
            return
            
        updateData()


class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Information", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Exponential Graph",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
        button2 = ttk.Button(self, text="Real-time Graph",
                            command=lambda: controller.show_frame(PageThree))
        button2.pack()
        

        self.label1 = tk.Label(self, text="", font=LARGE_FONT)
        self.label1.pack()
        self.label2 = tk.Label(self, text="Voltage: ", font=LARGE_FONT)
        self.label2.pack()
        #self.updateData()
        
        
     
    #def updateData(self):
     #   
      #  if Param.i==8:
      #      Param.i=0
      #  now = time.strftime("%H:%M:%S")
      #  self.label1.configure(text=now)
      #  self.label2.configure(text="Voltage: " + str(voltage[Param.i]))
      #  Param.i += 1
      #  print(Param.i)
      #  self.master.after(1000, self.updateData)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Real-Time Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button1 = ttk.Button(self, text="Exponential Graph",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()
        
        button1 = ttk.Button(self, text="Information",
                            command=lambda: controller.show_frame(PageTwo))
        button1.pack()


        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        

app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
