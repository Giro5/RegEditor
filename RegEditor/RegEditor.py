from tkinter import *
from winreg import *
#import winreg
from tkinter import messagebox


keys = [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]
keysStr = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
path = "PC\\"


root = Tk()
root.title("RegEditor")
root.geometry("900x500")

MainMenu = Menu()
MainMenu.add_cascade(label="File")
MainMenu.add_cascade(label="Edit")
MainMenu.add_cascade(label="View")
root.config(menu = MainMenu)

VarPath = StringVar(root, value = path).set(path)
EntryPath = Entry(root, textvariable = VarPath).pack(side = "top", fill = "both")


treeFrame = Frame(root, width = 200, bg = "#b5b5b5")
mainFrame = Frame(root, width = 700, bg = "#cfcfcf")

treeFrame.pack(side = "left", fill = "both")
mainFrame.pack(side = "right", fill = "both")

scrollbarY = Scrollbar(treeFrame)
scrollbarY.pack(side = "right", fill = "y")
scrollbarX = Scrollbar(treeFrame, orient = HORIZONTAL)
scrollbarX.pack(side = "bottom", fill = "x")

KeysListbox = Listbox(treeFrame, yscrollcommand = scrollbarY.set, xscrollcommand = scrollbarX.set, width = 30)
KeysListbox.pack(side = "right" ,fill = "both")
scrollbarY.config(command = KeysListbox.yview)
scrollbarX.config(command = KeysListbox.xview)

for i in range(len(keys)):
    KeysListbox.insert(END, keysStr[i])

def GetIn():
    global KeysListbox
    global keys
    sel = KeysListbox.curselection()[0]
    key = OpenKey(keys[sel], "", 0, KEY_ALL_ACCESS)

    for i in range(10):
        KeysListbox.insert(END,)

getinButton = Button(mainFrame, text = "Get In", command = GetIn).place(x = 5, y = 5, width = 40, height = 20)
backButton = Button(mainFrame, text = "Back").place(x = 45, y = 5, width = 40, height = 20)
infoButton = Button(mainFrame, text = "Info").place(x = 85, y = 5, width = 40, height = 20)






root.mainloop()