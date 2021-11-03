from __future__ import print_function
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from quickstart import *

tk = Tk()
tk.title("Welcome!!")


def Upload():
    try:
        path = filedialog.askopenfile()
        FilePath = path.name
        Uploadfile(FilePath)
    except(AttributeError):
        tkinter.messagebox.showerror("Cant find file","Please Select Again!")


def DownLoad():
    indexs = listBox1.curselection()
    for i in indexs:
        Downloadfile(i, listBox1.get(i))


def Refresh():
    listBox1.delete(0, END)
    items = listfile()
    for item in items:
        listBox1.insert(items.index(item), str(items.index(item)) + ") " + item['name'])
    listBox1.pack()


# Header
lb1 = Label(tk, text="Connect to Google Drive!!", fg="blue")
lb1.pack(side=TOP)
lb2 = Label(tk)
lb2.pack(side=BOTTOM)

# Listbox
items = listfile()
listBox1 = Listbox(lb2, width=60, height=30, xscrollcommand=True)
for item in items:
    listBox1.insert(items.index(item), str(items.index(item)) + ") " + item['name'])
listBox1.pack()

# Button Upload,Download,Refresh
pnw1 = PanedWindow(lb2, orient=HORIZONTAL)
pnw1.pack()
#Upload
btnUpload = tkinter.Button(pnw1, text=("Upload"), command=Upload,  fg='red')
pnw1.add(btnUpload)
#Refresh
btnRefresh = tkinter.Button(pnw1, text=("Refresh"), command=Refresh,  fg='red')
pnw1.add(btnRefresh)
#Download
btnDownload = tkinter.Button(pnw1, text=("Download"), command=DownLoad,  fg='red')
pnw1.add(btnDownload)


tk.mainloop()
