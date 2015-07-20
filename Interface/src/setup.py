import sys
from cx_Freeze import setup, Executable
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




# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['ReadMe.txt','sampleTest.txt']
#packages=['matplotlib.backends.backend_tkagg']
build_exe_options = { "excludes": ["dateutil","pytz","six","pyparsing","time","tkinter","matplotlib","numpy","time"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "interface",
        version = "0.1",
        description = "My GUI application!",
        options = {"build.exe":build_exe_options},
        executables = [Executable("interface.py", base=base)])