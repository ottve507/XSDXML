from tkinter import *
from tkinter.ttk import Treeview
from generate_tree import App


#Start of program
#Sets up a basic UI
def main():
        root = Tk()
        root.title('Otto Velander XSD editor')
        root.geometry("1000x600")
        App(root)
        root.mainloop()


if __name__ == "__main__":
    main()