from gui import GUI
from tkinter import Tk
def main():
    root = Tk()
    root.title('AdaptiveControl Setup')
    # print(dir(root))
    app = GUI(root = root)
    screenx, screeny = resolution = app.screen_size()
    root.geometry(f'{int(screenx/2)}x{int(screeny/1.25)}+{int(screenx/4)}+10')
    app.mainloop()
if __name__=='__main__':
    main()
