# Main.py
from Controlls.Arduino_control import *
from Controlls.Camera_control import *
from Controlls.GUI_control import *
from Controlls.Robot_control import *
from Process.Robot_process import *

if __name__ == "__main__":
    root = tk.Tk()
    gui = EurofinsGUI(root)
    root.mainloop()