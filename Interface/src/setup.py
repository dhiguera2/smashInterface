import sys
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['ReadMe.txt','sampleTest.txt']
build_exe_options = { "includes": ["tkinter","matplotlib","numpy","time"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "interface",
        version = "0.1",
        description = "My GUI application!",
        options = {"build.exe": build_exe_options },
        executables = [Executable("interface.py", base=base)])