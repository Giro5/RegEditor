from tkinter import *
from winreg import *
#import winreg
from tkinter import messagebox
#from tkinter.messagebox import *
import tkinter.ttk as ttk
import winsound

hkeys = [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]
keysStr = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
path = ""
curpath = ""
key = OpenKey(hkeys[0], "")

RegTypes = ["REG_NONE","REG_SZ","REG_EXPAND_SZ","REG_BINARY","REG_DWORD","REG_DWORD_BIG_ENDIAN","REG_LINK","REG_MULTI_SZ","REG_RESOURCE_LIST","REG_FULL_RESOURCE_DESCRIPTOR","REG_RESOURCE_REQUIREMENTS_LIST","REG_QWORD"]

currentkeys = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
names = []
types = []
data = []

root = Tk()
root.title("RegEditor")
root.geometry("1000x550+300+200")

TextPath = StringVar(root)
TextPath.set(path)
EntryPath = Entry(root, textvariable = TextPath)
EntryPath.pack(side = "top", fill = "both")

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
table.column("Type", width = 40)
table.pack(expand = True, fill = "both", side = "left")

scrolltable = Scrollbar(mainFrame, command = table.yview)
table.configure(yscrollcommand = scrolltable.set)
scrolltable.pack(side = "right", fill = "y")

def changeFocusListbox(event):
    table.delete(*table.get_children())
    for j in range(len(names)):
            table.insert("", END, values = (names[j] if names[j] != "" else "(Default)", RegTypes[types[j]], ConvertTypes(types[j], data[j])))
KeysListbox.bind("<Button-1>", changeFocusListbox)

def changeFocusTreeview(event):
    changeFocusListbox("")
    KeysListbox.delete(0, END)
    for i in range(len(currentkeys)):
            KeysListbox.insert(END, currentkeys[i])
table.bind("<Button-1>", changeFocusTreeview)

for i in range(len(hkeys)):
    KeysListbox.insert(END, keysStr[i])

def RefreshKey():
    global path, key, currentkeys
    ways = path.split("\\")
    print(ways)
    curindex = 5
    if any(ways[0] == j for j in keysStr):
        for i in range(len(keysStr)):
            if keysStr[i] == ways[0]: break
        curindex = i
    else:
        print("_Trash into the entrybox_Rename")
        path = curpath
        TextPath.set(path)
        Follow("")
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
        print("_The key can't opened_Rename")
        path = curpath
        TextPath.set(path)
        Follow("")
        return
    return

def GetIn(event):
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
    Follow("")

KeysListbox.bind("<Double-Button-1>", GetIn)

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
    Follow("")

def ConvertTypes(regtype, value):
    if regtype == REG_NONE:
        return "(zero-length binary value)"

    elif regtype == REG_SZ:
        if value == None:
            return "(Value not set)"
        return value

    elif regtype == REG_EXPAND_SZ:
        if value == None:
            return "(Value not set)"
        return str(value).replace("\\", "/")

    elif regtype == REG_BINARY:
        if value == None:
            return "(zero-length binary value)"
        return [(hex(i)[2:] if i != 0 else "00") for i in value]

    elif regtype == REG_DWORD:
        return (hex(value) if len(hex(value)) > 9 else "0x" + "0" * (10 - len(hex(value))) + hex(value)[2:]) + f" ({value})"

    elif regtype == REG_DWORD_BIG_ENDIAN:
        return ConvertTypes(REG_DWORD, value)

    elif regtype == REG_LINK:
        if value == None:
            return "(Value not set)"
        return value

    elif regtype == REG_MULTI_SZ:
        if len(value) > 0:
            return " ".join(value)
        return ""

    elif regtype == REG_RESOURCE_LIST:
        if value == None:
            return "(Value not set)"
        return value

    elif regtype == REG_FULL_RESOURCE_DESCRIPTOR:
        if value == None:
            return "(Value not set)"
        return value

    elif regtype == REG_RESOURCE_REQUIREMENTS_LIST:
        if value == None:
            return "(Value not set)"
        return value

    elif regtype == REG_QWORD:
        return ConvertTypes(REG_DWORD, value)

    else:
        raise TypeError

def Follow(event):
    global path, curpath, key, currentkeys
    path = TextPath.get()
    print("\n_Follow_\n" + path)
    if path != "":
        RefreshKey()
        i = 0
        currentkeys.clear()
        while True:
            try: currentkeys.append(EnumKey(key, i))
            except: break
            i += 1
        j = 0
        names.clear()
        types.clear()
        data.clear()
        while True:
            try:
                names.append(EnumValue(key, j)[0])
                types.append(EnumValue(key, j)[2])
                data.append(EnumValue(key, j)[1])
            except: break
            j += 1
        KeysListbox.delete(0, END)
        table.delete(*table.get_children())
        for i in range(len(currentkeys)):
            KeysListbox.insert(END, currentkeys[i])
        for j in range(len(names)):
            table.insert("", END, values = (names[j] if names[j] != "" else "(Default)", RegTypes[types[j]], ConvertTypes(types[j], data[j])))
    else:
        currentkeys = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]
        KeysListbox.delete(0, END)
        for i in range(len(hkeys)):
            KeysListbox.insert(END, keysStr[i])
    curpath = path

EntryPath.bind("<Return>", Follow)

def Refresh(event):
    global path, curpath
    path = curpath
    TextPath.set(path)
    Follow("")

def Export():
    global curpath
    import subprocess
    from tkinter import filedialog
    filepath = filedialog.asksaveasfilename(filetypes = (("Registration Files", "*.reg"), ("All Files", ""))) + ".reg"
    print(filepath)
    subprocess.Popen(f"reg export {curpath} {filepath} /y /reg:64", shell = True)

def Import():
    import subprocess
    from tkinter import filedialog
    filepath = filedialog.askopenfilename(filetypes = (("Registration Files", "*.reg"), ("", "")))
    print(filepath)
    subprocess.Popen(f"reg import {filepath} /reg:64", shell = True)

def Rename():
    global key
    sel = table.index(table.focus())
    if names[sel] != "" and names[sel] != None:
        save = [names[sel], types[sel], data[sel]]
        print(save, "\n", curpath)
        child = Toplevel(root)
        child.title("Rename Key")
        child.geometry("400x220+300+200")
        child.resizable(False, False)
        child.grab_set()
        child.focus_set()
        nameText = StringVar()
        nameText.set(save[0])
        infolabel = Label(child, text = "Enter new name:").place(x = 10, y = 18)
        nameEntry = Entry(child, textvariable = nameText).place(x = 10, y = 40, width = 380, height = 20)
        def OK():
            global key
            if save[0] != nameText.get() and nameText.get() != "":
                DeleteValue(key, save[0])
                SetValueEx(key, nameText.get(), 0, save[1], save[2])
                Refresh("")
                child.destroy()
                return
            else:
                child.destroy()
                return
        def Cancel():
            child.destroy()
        OKButton = Button(child, text = "OK", command = OK).place(x = 220, y = 190, width = 80, height = 20)
        CancelButton = Button(child, text = "Cancel", command = Cancel).place(x = 310, y = 190, width = 80, height = 20)
        child.mainloop()
    else:
       winsound.Beep(900, 250)
       return
    
def Modify():
    global key
    try: sel = table.index(table.focus())
    except: return
    save = [names[sel], types[sel], data[sel]]
    child = Toplevel(root)
    child.title("Edit Data")
    child.geometry("400x220+300+200")
    child.resizable(False, False)
    child.grab_set()
    child.focus_set()
    infolabel = Label(child, text = "Value name:").place(x = 10, y = 18)
    nameEntry = Entry(child, textvariable = StringVar(value = save[0]), state = "disabled").place(x = 10, y = 40, width = 380, height = 20)
    infolabel2 = Label(child, text = "Value data:").place(x = 10, y = 60)
    dataEntry = Entry(child, textvariable = StringVar(value = save[2]))
    dataEntry.place(x = 10, y = 82, width = 380, height = 20)
    def OK():
        global key
        if save[0] != dataEntry.get():
            SetValueEx(key, save[0], 0 , save[1], dataEntry.get())
            Refresh("")
            child.destroy()
            return
        else:
            child.destroy()
            return
    def Cancel():
        child.destroy()
    OKButton = Button(child, text = "OK", command = OK).place(x = 220, y = 190, width = 80, height = 20)
    CancelButton = Button(child, text = "Cancel", command = Cancel).place(x = 310, y = 190, width = 80, height = 20)
    child.mainloop()

def Delete():
    print(root.focus_get())
    if str(root.focus_get()).split(".!")[len(str(root.focus_get()).split(".!")) - 1] == "treeview":
        if table.focus() == "":
            return
        try: sel = table.index(table.focus())
        except: return
        save = [names[sel], types[sel], data[sel]]
        answer = messagebox.askyesno("Confirmation of deletion", "Are you sure?")
        print(answer)
        if answer:
            DeleteValue(key, save[0])
    elif str(root.focus_get()).split(".!")[len(str(root.focus_get()).split(".!")) - 1] == "listbox":
        try: sel = KeysListbox.curselection()[0]
        except: return
        selStr = KeysListbox.get(sel)
        answer = messagebox.askyesno("Confirmation of deletion", "Are you sure?")
        print(answer)
        if answer:
            DeleteKey(key, selStr)
    else:
        winsound.Beep(900, 250)
    Refresh("")

def Create(regtype):
    if regtype == "key":
        i = 1
        while True:
            if any(f"New Key #{i}" == j for j in KeysListbox.get(0, END)): i += 1
            else: break
        newkey = CreateKey(key, f"New Key #{i}")
        newkey.Close()
    elif any(regtype == j for j in [1, 2, 3, 4, 7, 11]):
        i = 1
        while True:
            if any(f"New Value #{i}" == j for j in [table.item(k)["values"][0] for k in table.get_children()]): i += 1
            else: break
        SetValueEx(key, f"New Value #{i}", 0, regtype, None)
        Refresh("")
        table.focus(table.get_children()[len(table.get_children()) - 1])
        Rename()
    else:
        print("not found")
    Refresh("")

MainMenu = Menu(root)
FileItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "File", menu = FileItem)
FileItem.add_cascade(label = "Import", command = Import)
FileItem.add_cascade(label = "Export", command = Export)
FileItem.add_separator()
FileItem.add_cascade(label = "Exit", command = root.destroy)

EditItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "Edit", menu = EditItem)
NewItem = Menu(EditItem, tearoff = 0)
NewItem.add_command(label = "Key", command = lambda: Create("key"))
NewItem.add_separator()
NewItem.add_cascade(label = "String Value", command = lambda: Create(REG_SZ))
NewItem.add_cascade(label = "Binary Value", command = lambda: Create(REG_BINARY))
NewItem.add_cascade(label = "DWORD (32-bit) Value", command = lambda: Create(REG_DWORD))
NewItem.add_cascade(label = "QWORD (64-bit) Value", command = lambda: Create(REG_QWORD))
NewItem.add_cascade(label = "Multi-String Value", command = lambda: Create(REG_MULTI_SZ))
NewItem.add_cascade(label = "Expandable String Value", command = lambda: Create(REG_EXPAND_SZ))
EditItem.add_cascade(label = "New", menu = NewItem)
EditItem.add_separator()
EditItem.add_cascade(label = "Delete", command = Delete)
EditItem.add_cascade(label = "Rename", command = Rename)
EditItem.add_separator()
EditItem.add_cascade(label = "Copy key")

ViewItem = Menu(MainMenu, tearoff = 0)
MainMenu.add_cascade(label = "View", menu = ViewItem)
ViewItem.add_cascade(label = "Refresh            F5", command = lambda: Refresh(""))
root.bind("<F5>", Refresh)

getinButton = Button(buttonFrame, text = "Get In")
getinButton.bind("<Button-1>", GetIn)
getinButton.place(x = 5, y = 5, width = 60, height = 40)

backButton = Button(buttonFrame, text = "Back", command = Back).place(x = 65, y = 5, width = 60, height = 40)

followButton = Button(buttonFrame, text = "Follow")
followButton.bind("<Button-1>", Follow)
followButton.place(x = 125, y = 5, width = 60, height = 40)

renameButton = Button(buttonFrame, text = "Rename", command = Rename).place(x = 205, y = 5, width = 60, height = 40)
modifyButton = Button(buttonFrame, text = "Modify", command = Modify).place(x = 265, y = 5, width = 60, height = 40)
deleteButton = Button(buttonFrame, text = "Delete", command = Delete).place(x = 325, y = 5, width = 60, height = 40)

def TableDropDown(event):
    print("focus the element", table.focus(), "|")
    if table.focus() != "":
        EditFocus = Menu(table, tearoff = 0)
        EditFocus.add_cascade(label = "Modify...", command = Modify)
        EditFocus.add_separator()
        EditFocus.add_cascade(label = "Delete", command = Delete)
        EditFocus.add_cascade(label = "Rename", command = Rename)
        EditFocus.post(event.x_root, event.y_root)
    else:
        NoFocus = Menu(table, tearoff = 0)
        NoFocus.add_cascade(label = "New           ", menu = NewItem)
        NoFocus.post(event.x_root, event.y_root)
    return
table.bind("<Button-3>", TableDropDown)

root.config(menu = MainMenu)

root.mainloop()