from gui import GUI
from tkinter import Tk


def main():
    root = Tk()
    root.title('AdaptiveControl Setup')
    # print(dir(root))
    app = GUI(root=root)
    screen_x, screen_y = app.screen_size()
    root.geometry(f'{int(screen_x/2)}x{int(screen_y/1.25)}+{int(screen_x/4)}+10')
    app.mainloop()


if __name__ == '__main__':
    main()
