from tkinter import *
from winreg import *
#import winreg
from tkinter import messagebox


keys = [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]
curkey = -1
keysStr = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
path = ""

RegTypes = ["REG_NONE","REG_SZ","REG_EXPAND_SZ","REG_BINARY","REG_DWORD","REG_DWORD_BIG_ENDIAN","REG_LINK","REG_MULTI_SZ","REG_RESOURCE_LIST","REG_FULL_RESOURCE_DESCRIPTOR","REG_RESOURCE_REQUIREMENTS_LIST","REG_QWORD"]

root = Tk()
root.title("RegEditor")
root.geometry("1000x550")

MainMenu = Menu()
MainMenu.add_cascade(label="File")
MainMenu.add_cascade(label="Edit")
MainMenu.add_cascade(label="View")
root.config(menu = MainMenu)

TextPath = StringVar(root)
TextPath.set(path)
EntryPath = Entry(root, textvariable = TextPath).pack(side = "top", fill = "both")

treeFrame = Frame(root,  width = 200, bg = "#b5b5b5")
mainFrame = Frame(root,  width = 800, bg = "#cfcfcf")
buttonFrame = Frame(root, width = 1000, height = 50, bg = "#b5b5b5")

buttonFrame.pack(side = "bottom", fill = "both")
treeFrame.pack(side = "left", fill = "both")
mainFrame.pack(side = "left", fill = "both")

TreeScrollY = Scrollbar(treeFrame)
TreeScrollY.pack(side = "right", fill = "y")
TreeScrollX = Scrollbar(treeFrame, orient = HORIZONTAL)
TreeScrollX.pack(side = "bottom", fill = "x")

KeysListbox = Listbox(treeFrame, yscrollcommand = TreeScrollY.set, xscrollcommand = TreeScrollX.set, width = 30)
KeysListbox.pack(side = "right" ,fill = "both")
TreeScrollY.config(command = KeysListbox.yview)
TreeScrollX.config(command = KeysListbox.xview)

def ScrollName(*args):
    if ValueNameListbox.yview() != ValueTypeListbox.yview() or ValueNameListbox.yview() != ValueDataListbox.yview():
        ValueNameListbox.yview_moveto(args[0])
    MainScrollY.set(*args)
def ScrollType(*args):
    if ValueNameListbox.yview() != ValueTypeListbox.yview() or ValueTypeListbox.yview() != ValueDataListbox.yview():
        ValueTypeListbox.yview_moveto(args[0])
    MainScrollY.set(*args)
def ScrollData(*args):
    if ValueDataListbox.yview() != ValueTypeListbox.yview() or ValueNameListbox.yview() != ValueDataListbox.yview():
        ValueDataListbox.yview_moveto(args[0])
    MainScrollY.set(*args)
def MainYview(*args):
    ValueNameListbox.yview(*args)
    ValueTypeListbox.yview(*args)
    ValueDataListbox.yview(*args)

MainScrollY = Scrollbar(mainFrame)
MainScrollY.pack(side = "right", fill = "y")
MainScrollY.config(command = MainYview)

ValueNameListbox = Listbox(mainFrame, width = 50, yscrollcommand = ScrollName)
ValueNameListbox.pack(side = "left", fill = "y")

ValueTypeListbox = Listbox(mainFrame, width = 30, yscrollcommand = ScrollType)
ValueTypeListbox.pack(side = "left", fill = "y")

ValueDataListbox = Listbox(mainFrame, width = 100, yscrollcommand = ScrollData)
ValueDataListbox.pack(side = "left", fill = "y")

for i in range(len(keys)):
    KeysListbox.insert(END, keysStr[i])

def GetIn():
    global path
    global curkey

    sel = KeysListbox.curselection()[0]
    selstr = KeysListbox.get(sel)
    print(selstr)

    path = TextPath.get()
    ways = path.split("\\")
    print("_", ways, "_")

    if ways[0] == "":
        curkey = sel
        path += selstr
    elif any(ways[0] == s for s in keysStr):
        path += "\\" + selstr
        ways = path.split("\\")
        briefly = ways[1]
        for j in range(2, len(ways)):
            briefly += "\\" + ways[j]
        print(ways[0], briefly)
    else:
        print("trash into the entrybox")
    TextPath.set(path)
    Follow()

def Back():
    global path
    global curkey
    ways = path.split("\\")
    print("_", ways, "_")
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
    global path
    global curkey
    tmp = path
    path = TextPath.get()
    print(path)
    if path != "":
        ways = path.split("\\")
        print("_", ways, "_")
        curindex = -1
        if any(ways[0] == j for j in keysStr):
            for i in range(len(keysStr)):
                if keysStr[i] == ways[0]: break
            curindex = i
        else: return
        print(curindex)
        curkey = curindex
        briefly = ""
        if len(ways) > 1:
            briefly = ways[1]
            for j in range(2, len(ways)):
                briefly += "\\" + ways[j]
        key = OpenKey(keys[curkey], briefly, 0, KEY_ALL_ACCESS)
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
        ValueNameListbox.delete(0, END)
        ValueTypeListbox.delete(0, END)
        ValueDataListbox.delete(0, END)
        for i in range(len(currentkey)):
            KeysListbox.insert(END, currentkey[i])
        for j in range(len(names)):
            ValueNameListbox.insert(END, names[j])
            ValueTypeListbox.insert(END, RegTypes[types[j]])
            ValueDataListbox.insert(END, str(data[j]))
    else:
        KeysListbox.delete(0, END)
        for i in range(len(keys)):
            KeysListbox.insert(END, keysStr[i])


getinButton = Button(buttonFrame, text = "Get In", command = GetIn).place(x = 5, y = 5, width = 40, height = 20)
backButton = Button(buttonFrame, text = "Back", command = Back).place(x = 45, y = 5, width = 40, height = 20)
followButton = Button(buttonFrame, text = "Follow", command = Follow).place(x = 125, y = 5, width = 60, height = 20)




root.mainloop()