from tkinter import *
from winreg import *
from tkinter import messagebox

root = Tk()
root.title("RegEditor")
root.geometry("500x500")

keys = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

keys_listbox = Listbox(yscrollcommand=scrollbar.set)
for i in keys:
    keys_listbox.insert(END, i)
keys_listbox.pack(side=LEFT, fill=BOTH)



scrollbar.config(command=keys_listbox.yview)







root.mainloop()