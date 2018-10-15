from tkinter import *
from winreg import *
#import winreg
from tkinter import messagebox
import tkinter.ttk as ttk

hkeys = [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]
keysStr = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
path = ""
curpath = ""

RegTypes = ["REG_NONE","REG_SZ","REG_EXPAND_SZ","REG_BINARY","REG_DWORD","REG_DWORD_BIG_ENDIAN","REG_LINK","REG_MULTI_SZ","REG_RESOURCE_LIST","REG_FULL_RESOURCE_DESCRIPTOR","REG_RESOURCE_REQUIREMENTS_LIST","REG_QWORD"]

root = Tk()
root.title("RegEditor")
root.geometry("1000x550")

TextPath = StringVar(root)
TextPath.set(path)
EntryPath = Entry(root, textvariable = TextPath).pack(side = "top", fill = "both")

treeFrame = Frame(root,  width = 200, bg = "#b5b5b5")
mainFrame = Frame(root,  width = 800, bg = "#cfcfcf")
buttonFrame = Frame(root, width = 1000, height = 50, bg = "#b5b5b5")

buttonFrame.pack(side = "bottom", fill = "both")
treeFrame.pack(side = "left", fill = "both")
mainFrame.pack(fill = "both", expand = True)

TreeScrollY = Scrollbar(treeFrame)
TreeScrollY.pack(side = "right", fill = "y")
TreeScrollX = Scrollbar(treeFrame, orient = HORIZONTAL)
TreeScrollX.pack(side = "bottom", fill = "x")

KeysListbox = Listbox(treeFrame, yscrollcommand = TreeScrollY.set, xscrollcommand = TreeScrollX.set, width = 30)
KeysListbox.pack(side = "right" ,fill = "both")
TreeScrollY.config(command = KeysListbox.yview)
TreeScrollX.config(command = KeysListbox.xview)

table = ttk.Treeview(mainFrame, show="headings", selectmode="browse")
heading = ("Name", "Type", "Data")
table.config(columns = heading, displaycolumns = heading)
for head in heading:
    table.heading(head, text = head, anchor = "w")
    table.column(head, anchor = "w")
table.pack(expand = True, fill = "both", side = "left")

scrolltable = Scrollbar(mainFrame, command = table.yview)
table.configure(yscrollcommand = scrolltable.set)
scrolltable.pack(side = "right", fill = "y")

for i in range(len(hkeys)):
    KeysListbox.insert(END, keysStr[i])

def GetIn():
    global path
    try: sel = KeysListbox.curselection()[0]
    except : return
    selstr = KeysListbox.get(sel)
    print("\n_Get In_\n" + selstr)
    path = TextPath.get()
    ways = path.split("\\")
    print(ways)
    if ways[0] == "":
        path += selstr
    elif any(ways[0] == s for s in keysStr):
        path += "\\" + selstr
    else:
        print("_Trash into the entrybox_GetIn")
        path = ""
    TextPath.set(path)
    Follow()

def Back():
    global path
    ways = path.split("\\")
    print("\n_Back_\n" + path)
    ways = ways[:-1]
    print(ways)
    if len(ways) > 0:
        comppath = ways[0]
        for i in range(1, len(ways)):
            comppath += "\\" + ways[i]
        print(comppath)
    else:
        comppath = ""
    path = comppath
    TextPath.set(path)
    Follow()

def Follow():
    global path, curpath
    path = TextPath.get()
    print("\n_Follow_\n" + path)
    if path != "":
        ways = path.split("\\")
        print(ways)
        curindex = 5
        if any(ways[0] == j for j in keysStr):
            for i in range(len(keysStr)):
                if keysStr[i] == ways[0]: break
            curindex = i
        else:
            print("_Trash into the entrybox_Follow")
            path = ""
            TextPath.set(path)
            Follow()
            return
        print(curindex)
        briefly = ""
        if len(ways) > 1:
            briefly = ways[1]
            for j in range(2, len(ways)):
                briefly += "\\" + ways[j]
        try:
            key = OpenKey(hkeys[curindex], briefly, 0, KEY_ALL_ACCESS)
        except BaseException:
            path = curpath
            TextPath.set(path)
            Follow()
            return
        i = 0
        currentkey = []
        while True:
            try: currentkey.append(EnumKey(key, i))
            except: break
            i += 1
        j = 0
        names = []
        types = []
        data = []
        while True:
            try:
                names.append(EnumValue(key, j)[0])
                types.append(EnumValue(key, j)[2])
                data.append(EnumValue(key, j)[1])
            except: break
            j += 1
        KeysListbox.delete(0, END)
        table.delete(*table.get_children())
        for i in range(len(currentkey)):
            KeysListbox.insert(END, currentkey[i])
        for j in range(len(names)):
            table.insert("", END, values = (names[j] if names[j] != "" else "(Default)", RegTypes[types[j]], str(data[j]) if data[j] != None else "(Value not set)"))
    else:
        KeysListbox.delete(0, END)
        for i in range(len(hkeys)):
            KeysListbox.insert(END, keysStr[i])
    curpath = path

def Refresh():
    global path, curpath
    path = curpath
    TextPath.set(path)
    Follow()

def Export():
    global curpath
    if curpath != "":
        ways = curpath.split("\\")
        curindex = 5
        if any(ways[0] == j for j in keysStr):
            for i in range(len(keysStr)):
                if keysStr[i] == ways[0]: break
            curindex = i
        else:
            print("_Trash into the entrybox_Export")
            path = ""
            TextPath.set(path)
            Follow()
            return
        briefly = ""
        if len(ways) > 1:
            briefly = ways[1]
            for j in range(2, len(ways)):
                briefly += "\\" + ways[j]
        try:
            key = OpenKey(hkeys[curindex], briefly, 0, KEY_ALL_ACCESS)
        except BaseException:
            path = curpath
            TextPath.set(path)
            Follow()
            return

        import os, sys
        import win32api
        import win32security
        privflag = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), privflag)
        privid = win32security.LookupPrivilegeValue(None, "SeBackupPrivilege")
        win32security.AdjustTokenPrivileges(hToken, 0, [(privid, win32security.SE_PRIVILEGE_ENABLED)])

        filepath = "reg.reg"
        import os.path, os
        if os.path.exists(filepath):
            os.remove(filepath)
        SaveKey(key, filepath)
    else: return

def Import():
    return

def Rename():
    global curpath
    sel = table.focus()
    print(sel)
    

def Modify():
    return

def Delete():
    return

def Create():
    return


getinButton = Button(buttonFrame, text = "Get In", command = GetIn).place(x = 5, y = 5, width = 60, height = 40)
backButton = Button(buttonFrame, text = "Back", command = Back).place(x = 65, y = 5, width = 60, height = 40)
followButton = Button(buttonFrame, text = "Follow", command = Follow).place(x = 125, y = 5, width = 60, height = 40)
renameButton = Button(buttonFrame, text = "Rename", command = Rename).place(x = 205, y = 5, width = 60, height = 40)
modifyButton = Button(buttonFrame, text = "Modify", command = Modify).place(x = 265, y = 5, width = 60, height = 40)
deleteButton = Button(buttonFrame, text = "Delete", command = Delete).place(x = 325, y = 5, width = 60, height = 40)
createButton = Button(buttonFrame, text = "Create", command = Create).place(x = 385, y = 5, width = 60, height = 40)



MainMenu = Menu(root)
FileItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "File", menu = FileItem)
FileItem.add_cascade(label = "Import")
FileItem.add_cascade(label = "Export", command = Export)
FileItem.add_separator()
FileItem.add_cascade(label = "Exit", command = root.destroy)

EditItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "Edit", menu = EditItem)

ViewItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "View", menu = ViewItem,)
ViewItem.add_cascade(label = "Refresh", command = Refresh)

root.config(menu = MainMenu)

root.mainloop()