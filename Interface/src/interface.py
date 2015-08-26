##
import serial
import matplotlib
from binascii import crc32
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

ser = serial.Serial(
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.close()
comm_off_on = True
counter_cmd = 0

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
        button1.grid(row=0,column=4,pady=10,padx=50,sticky = "nsew")

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
        
    
        
        self.createFrameInfo()
        self.createFrameComm()
        self.createFrameCommand()
        #self.updateData()
    def createFrameComm(self):
    
        
        comm_frame = tk.Frame(self)
        comm_frame.grid(row=1,column=0,padx=20,sticky = "nsew")
       
        labelComm = tk.Label(comm_frame,text='Port :')
        labelComm.grid(row=0,column=0,padx=10,sticky = "nsew")
        
        entryComm = tk.Entry(comm_frame)
        entryComm.insert(0, 'COM7')
        entryComm.grid(row=0,column=1,padx=10,sticky = "nsew")
        
        labelBaud = tk.Label(comm_frame,text='Baud :')
        labelBaud.grid(row=1,column=0,padx=10,sticky = "nsew")
        
        entryBaud = tk.Entry(comm_frame)
        entryBaud.insert(0, '38400')
        entryBaud.grid(row=1,column=1,padx=10,sticky = "nsew")
        
        self.buttonComm = tk.Button(comm_frame)
        def go_comm(): 
            global comm_off_on
            global ser  
            
            if comm_off_on:
                print('Connection on: '+ entryComm.get() +", Baud= "+ entryBaud.get()) 
                ser.baudrate = entryBaud.get()
                ser.port = entryComm.get()
                ser.open()
                if ser.isOpen():
                    self.buttonComm.config(bg='green')
                    comm_off_on=False
                    
                
            else:
                print('Connection off')
                self.buttonComm.config(bg='red')
                comm_off_on=True 
                ser.close()
 
 
        self.buttonComm.config(text="Connection On/Off",command=go_comm,bg='red')
        self.buttonComm.grid(row=2,column=0,columnspan=2,pady=10,padx=50,sticky = "nsew")
        
        return
    
    def createFrameCommand(self):
        
        command_frame= tk.Frame(self)
        command_frame.grid(row=1,column=1,padx=20,sticky = "nsew")
        
        def go_science_mode():
            global counter_cmd
            # Header of GRIPS
            header = self.header_grips()            
            # Payload cmd science
            checksum_cmd = 231
            cmd_science = 24
            payload_cmd_science =self.do_cmd_payload(cmd_science, checksum_cmd)
            
            
            cmd_science = header + payload_cmd_science 
            ser.write(cmd_science)
            print(ser.read(100))
            counter_cmd+=1
         
        def go_safe_mode():
            global counter_cmd
            # Header of GRIPS
            header = self.header_grips()            
            # Payload cmd science
            checksum_cmd = 234
            cmd_science = 21
            payload_cmd_safe=self.do_cmd_payload(cmd_science, checksum_cmd)
            
            cmd_safe = header + payload_cmd_safe
            ser.write(cmd_safe)
            print(ser.read(100))
            counter_cmd+=1
        

        buttonSc = ttk.Button(command_frame, text="Science mode",
                            command=go_science_mode)
        buttonSc.grid(row=1,column=0,padx=10,sticky = "nsew")
        
        buttonSafe = ttk.Button(command_frame, text="Safe mode",
                            command=go_safe_mode)
        buttonSafe.grid(row=2,column=0,padx=10,sticky = "nsew")
        
        buttonHk = ttk.Button(command_frame, text="Send HK packet",
                            command=self.send_hkpacket_beacon)
        buttonHk.grid(row=3,column=0,padx=10,sticky = "nsew")
        
        return
    
    def header_grips(self):
        global counter_cmd
        # header Grips
        sync1= 0xEB
        sync2 = 0x90
        sysid = 0xC0
        checksum_high=0x00
        checksum_low=0x00
        cmd_type = 0x04
        size_payload_low = 8
        size_payload_high = 0
        
        header = [sync2, sync1, checksum_low ,checksum_high, sysid ,cmd_type, 
                           size_payload_low ,size_payload_high ,
                           counter_cmd,0 ,0 ,0, 0, 0, 0 ,0] # timer and checksum = 0    
        
        
         
        return header
    
    def send_hkpacket_beacon(self):
        global counter_cmd
        global ser

        cmd_hkbeacon_list =  self.header_grips()   + self.do_cmd_payload(254,1)
        ser.write(cmd_hkbeacon_list)
        print(self.readBuffer())
        counter_cmd+=1 
              
    def do_cmd_payload(self,cmd,chk):
        # Payload cmd science
        apid_low = 0x00
        apid_high = 0x05
        sequence_count_low = 0
        sequence_count_high = 0
        length_high=0
        length_low=0
        checksum_cmd = chk     
        payload_cmd = [apid_high ,apid_low ,
                                   sequence_count_high, sequence_count_low,
                                   length_high, length_low, checksum_cmd, 
                                   cmd ,0xF5, 0xF5]
            
        return payload_cmd
            
    def _readline(self):
        global ser
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
                else:
                    break
        return bytes(line)
    
    def readBuffer(self):
        global ser
        packet = bytearray()
        flag = True
        b1 = 0x00
        
        # start reading when sync bytes found
        while self.ser.inWaiting() != 0:
            b2 = self.ser.read(1)
            if b1 == 0xEB:
                if b2 == 0x90:
                    packet += b1
                    packet += b2
                    break
            if b2 == 0xEB:
                    b1 = 0xEB
            else:
                b1 = self.ser.read(1)
                             
        # keep reading until 0xF5F5 found
        b1 = self.ser.read(1)
        packet += b1
        while self.ser.inWaiting() != 0:
            b2 = self.ser.read(1)
            packet += b2
            if b1 == 0xF5:
                if b2 == 0xF5:
                    break
            if b2 == 0xF5:
                b1 = 0xF5
            else:
               b1 = self.ser.read(1) 
               packet += b1
               
        return bytes(packet)
                
    
        
    def fletcher8(self,msg):
        ckA = 0;
        ckB = 0;
        
        for a in range (0, len(msg)):
            ckA += msg[a]
            ckB += ckA
            
        return [ckA,ckB]
    
    def crc16(self,msg):
        crc = 0xFFFF;
        
        for pos in range (0, len(msg)):
            crc ^= msg[pos]
            
            for i in range (8, 0, -1):
                if ((crc & 0x0001) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
                    
        return crc
    
    
    def createFrameInfo(self):
        
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
            global ser
            if Param.i==8:
                Param.i=0
            now = time.strftime("%H:%M:%S")
            output_time.configure(text=now)
            output_voltage.configure(text=str(voltage[Param.i]))
            output_current.configure(text=str(current[Param.i]))
            Param.i += 1
            self.master.after(1000, updateData)
            #if ser.isOpen():
              #  ser.read(200)
            
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

