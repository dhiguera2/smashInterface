##
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time
import tkinter as tk
from tkinter import ttk

i=0
voltage = [8.8, 8.9, 8.8, 9, 8.9, 9.2, 9.1, 9.0, 8.8]

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

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

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


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Exponential Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Information",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        button3 = ttk.Button(self, text="Real-time Graph",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        
        label2 = tk.Label(self, text="m =", font=LARGE_FONT)
        label2.pack(pady=10,padx=10)
        
        entry = tk.Entry(self, bd =5)
        entry.pack()
        
        def changeParam():
            Param.m = float(entry.get())
            y = np.exp(Param.m*x)
            a2.clear()
            a2.plot(x,y)
            canvas.draw()
            return
            
        
        button4 = ttk.Button(self, text="Update graph",
                            command= changeParam )
        button4.pack()
        
        canvas = FigureCanvasTkAgg(f2, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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
        self.updateData()
        
        
     
    def updateData(self):
        
        if Param.i==8:
            Param.i=0
        now = time.strftime("%H:%M:%S")
        self.label1.configure(text=now)
        self.label2.configure(text="Voltage: " + str(voltage[Param.i]))
        Param.i += 1
        print(Param.i)
        self.master.after(1000, self.updateData)


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
