from tkinter import *
from winreg import *
#import winreg
from tkinter import messagebox


keys = [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]
keysStr = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "", "HKEY_CURRENT_CONFIG"]

root = Tk()
root.title("RegEditor")
root.geometry("900x500")

treeFrame = Frame(root, height = 500, width = 200, bg = "#b5b5b5")
mainFrame = Frame(root, height = 500, width = 700, bg = "#cfcfcf")

treeFrame.pack(side = "left", fill = "both")
mainFrame.pack(side = "right", fill = "both")
#treeFrame.grid(row = 0, column = 0)
#mainFrame.grid(row = 0, column = 1)

scrollbar = Scrollbar(treeFrame)
scrollbar.pack(side = "right", fill = "y")

keys_listbox = Listbox(treeFrame, yscrollcommand = scrollbar.set, width = 30)
keys_listbox.pack(side = "right" ,fill = "both")
scrollbar.config(command = keys_listbox.yview)

for i in keys:
    keys_listbox.insert(END, keysStr[i - 18446744071562067968])

def GetIn():
    global keys_listbox
    global keys
    sel = _listbox.curselection()[0]
    key = OpenKey(keys[sel], "", 0, KEY_ALL_ACCESS)

    for i in 10:
        keys_listbox.insert(END, )

getinButton = Button(mainFrame, text = "Get In", command = GetIn).place(x = 5, y = 5, width = 40, height = 20)
backButton = Button(mainFrame, text = "Back").place(x = 45, y = 5, width = 40, height = 20)
infoButton = Button(mainFrame, text = "Info").place(x = 85, y = 5, width = 40, height = 20)






root.mainloop()