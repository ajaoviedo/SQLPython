from tkinter import *
from tkinter import messagebox
import pyodbc
import pandas as pd

def logbuttonclick():
    try:
        username = usertext.get()
        pwd = passtext.get()
        if username == "" or pwd == "":
            return None
        global conn
        conn = pyodbc.connect(driver="SQL Server", server ="10.140.244.212\SQLEXPRESS,1434", user = username, password = pwd) #192.168.1.14
    except:
        return None
    
    root = Tk()
    root.title("AJ")
    root.geometry("1200x600")
    center(root)

    tf = Frame(root)
    bf = Frame(root)
    tf.pack()
    bf.pack(side=BOTTOM)

    global a1
    a1 = Button(tf, text = "Retrieve All Databases", command = dbaseonclick)
    a1.pack(side = TOP)
    global b1
    b1 = Listbox(tf)
    b1.pack()

    global a2
    a2 = Button(tf, text = "Retrieve All Tables", command = tableonclick)
    a2.pack(side = TOP)
    global b2
    b2 = Listbox(tf)
    b2.pack()
    
    global a3
    a3 = Button(tf, text = "Read Table", command = readonclick)
    a3.pack(side = TOP)
    global b3
    b3 = Text(tf)
    b3.pack()

    root.mainloop()

def dbaseonclick():   
    cursor = conn.cursor()
    query = pd.read_sql_query('SELECT name FROM sys.databases',conn)
    b1.delete(0,END)
    for i in range(len(query)) : 
        b1.insert(END, query.loc[i, "name"]) # add each row (database name) to the listbox
        
def tableonclick():
    cursor = conn.cursor()
    db = b1.get(ANCHOR)
    if db == "":
        messagebox.showerror(title = "Error", message = "Choose a database")
        return None
    cursor.execute(f'USE {db};') #change to specific database
    query = pd.read_sql_query('SELECT * FROM sys.Tables',conn)
    b2.delete(0,END)
    for i in range(len(query)) : 
        b2.insert(END, query.loc[i, "name"]) # add each row (database name) to the listbox
        
def readonclick():
    table = b2.get(ANCHOR)
    if table == "":
        messagebox.showerror(title = "Error", message = "Choose a table")
        return None
    query = pd.read_sql_query(f'SELECT * from {table}',conn)
    b3.delete(1.0,END)
    b3.insert(END, query)
    
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    

login = Tk()
login.title("Login")
login.geometry("600x400")
center(login)

f = Frame(login)
f.pack()

title1 = Label(f, text = "SQL Server Express Login\n", font=("Microsoft Sans Serif", 16))
title1.pack()

t1 = Label(f, text = "Username:", font=("Microsoft Sans Serif", 16))
t1.pack()

usertext = Entry(f, font=("Microsoft Sans Serif", 16))
usertext.pack()

t2 = Label(f, text = "Password:", font=("Microsoft Sans Serif", 16))
t2.pack()

passtext = Entry(f, font=("Microsoft Sans Serif", 16))
passtext.pack()

logbutton = Button(f, text = "Login", font=("Microsoft Sans Serif", 12), command = logbuttonclick)
logbutton.pack()


login.mainloop()