import tkinter as tk
from uimain import Main
import os

def main():
    root = tk.Tk()
    root.title('动平衡许用剩余不平衡量计算器')
    root.iconbitmap(os.path.join(os.path.dirname(__file__), 'icon.ico'))
    root.resizable(False, False)
    app = Main(root)
    app.create()
    app.mainloop()

if __name__ == '__main__':
    main()