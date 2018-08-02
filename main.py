import tkinter as tk
from window import Window

def main():
    root = tk.Tk()
    pacman = Window(root)
    pacman.run()


if __name__ == '__main__':
    main()
