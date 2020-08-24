# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:26:38 2018
Updated on Sunday August 23 20:52:00 2020
@author: hnambur
@author: azeembukhariprivate
"""
import sqlite3
import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame,Tk,Label,Entry,Scrollbar,Listbox,Button,END,VERTICAL
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def pyping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def connect_ip(hostname, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((hostname, port))
        sock.close()
        return result == 0

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print ("DB Load Success!!")
    except Error as e:
        print(e)
    return conn

class phonebook(Frame):
    def __init__(self,master):
        Frame.__init__(self)
        self.master = master
        self.connect_db()
        self.load_gui()
        self.load_list()
        
    def onClear(self):
    #clears the textboxes
        self.txt_user.delete(0,END)
        self.txt_empcode.delete(0,END)
        self.txt_ipaddress.delete(0,END)
        self.txt_email.delete(0,END)
    def load_list(self):
        print("Load List")
        
    def on_select(self,event):
        id_list = event.widget
        #selection_id = id_list.curselection()[0]
        #name = id_list.get(selection_id)
        #data = self.my_db.get_record(name)
        self.txt_user.delete(0, END)
        self.txt_user.insert(0,data[0])
        self.txt_empcode.delete(0, END)
        self.txt_empcode.insert(0,data[1])
        self.txt_ipaddress.delete(0, END)
        self.txt_ipaddress.insert(0,data[2])
        self.txt_email.delete(0, END)
        self.txt_email.insert(0,data[3])
    def on_delete(self):
        pass
    def on_close(self):
        """
        Closes the window
        """
        self.conn.close()
        self.master.destroy()
        window.destroy()
        
    def connect_db(self):
        self.conn = create_connection("iptable.db")

    def onClickFind(self):
        print ("Find")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM ipTable WHERE user LIKE ?", ('%'+ self.txt_user.get() + '%',))
        rows = cur.fetchall()
        self.current_name = rows[0][2]
        self.txt_empcode.delete(0, END)
        self.txt_ipaddress.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_user.delete(0, END)

        self.txt_user.insert(0,rows[0][2])
        self.txt_ipaddress.insert(0,rows[0][1])
        self.txt_empcode.insert(0,rows[0][0])
        self.txt_email.insert(0,rows[0][3])

    def onClickAdd(self):
        print ("Add")
        sql = ''' INSERT INTO ipTable (empcode,user,address,mail)
                  VALUES(?,?,?,?) '''
        data = (self.txt_empcode.get(),self.txt_user.get(),self.txt_ipaddress.get(),self.txt_email.get())
        print ("data : ", data)
        cur = self.conn.cursor()
        cur.execute(sql,data)
        self.conn.commit()
        self.txt_empcode.delete(0, END)
        self.txt_ipaddress.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_user.delete(0, END)
        messagebox.showinfo("Info","User Added") 


    def onClickUpdate(self):
        print ("Add")
        sql = ''' UPDATE ipTable SET empcode = ? , address = ?, user = ?, mail = ? WHERE user = ? '''

        data = (self.txt_empcode.get(),self.txt_ipaddress.get(),self.txt_user.get(),self.txt_email.get(),self.current_name)
        print ("data : ", data)
        self.current_name = self.txt_user.get()
        cur = self.conn.cursor()
        cur.execute(sql,data)
        self.conn.commit()
        messagebox.showinfo("Info","User Updated") 
    
    def load_gui(self):
    #setting up gui labels
        self.lbl_fname = Label(self.master, text = 'Full Name ')
        self.lbl_fname.grid(row = 0, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_lname = Label(self.master, text = 'EMP CODE ')
        self.lbl_lname.grid(row = 2, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_phone = Label(self.master, text = 'IP Address ')
        self.lbl_phone.grid(row = 4, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_email = Label(self.master, text = 'Email: ')
        self.lbl_email.grid(row = 6, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        #self.lbl_user = Label(self.master, text = 'User: ')
        #self.lbl_user.grid(row = 0, column = 2, padx = (0,0), pady = (10,0), sticky = 'nw')
        #setting up gui entry fields
        self.txt_user = Entry(self.master, text = '')
        self.txt_user.grid(row = 1, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_empcode = Entry(self.master, text = '')
        self.txt_empcode.grid(row = 3, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_ipaddress = Entry(self.master, text = '')
        self.txt_ipaddress.grid(row = 5, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_email = Entry(self.master, text = '')
        self.txt_email.grid(row = 7, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        #setting up listbox and the scrollbar
        #self.scrollbar1 = Scrollbar(self.master, orient = VERTICAL)
        #self.lstList1 = Listbox(self.master, exportselection = 0, yscrollcommand = self.scrollbar1.set)
        #self.lstList1.bind('<<ListboxSelect>>', self.on_select)
        #self.scrollbar1.config(command = self.lstList1.yview)
        #self.scrollbar1.grid(row = 1, column = 5, rowspan = 7, sticky = 'nes')
        #self.lstList1.grid(row = 1, column = 2, rowspan = 7, columnspan = 3, sticky = 'nsew')
        #setting up buttons
        self.btn_add = Button(self.master, width = 12, height = 2, text = 'Add', command = lambda: self.onClickAdd())
        self.btn_add.grid(row = 8, column = 0, padx = (25,0), pady = (45,10), sticky = 'w')
        self.btn_add = Button(self.master, width = 12, height = 2, text = 'Find', command = lambda: self.onClickFind())
        self.btn_add.grid(row = 8, column = 1, padx = (25,0), pady = (45,10), sticky = 'w')
        self.btn_update = Button(self.master, width = 12, height = 2, text = 'Update', command = lambda: self.onClickUpdate())
        self.btn_update.grid(row = 8, column = 2, padx = (15,0), pady = (45,10), sticky = 'w')
        #self.btn_delete = Button(self.master, width = 12, height = 2, text = 'Delete', command = lambda: phonebook_func.onDelete(self))
        #self.btn_delete.grid(row = 8, column = 3, padx = (15,0), pady = (45,10), sticky = 'w')
        self.btn_close = Button(self.master, width = 12, height = 2, text = 'Close', command = self.on_close)
        self.btn_close.grid(row = 8, column = 4, padx = (15,15), pady = (45,10), sticky = 'e')


class App2(ttk.Frame):
    """ Application to convert feet to meters or vice versa. """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""
        self.btn_get_me_ip = Button(self.master, width = 12, height = 2, text = 'Get Me Free IP', command = lambda: self.get_free_ip())
        self.btn_get_me_ip.grid(row = 8, column = 0, padx = (25,0), pady = (45,10), sticky = 'w')
        self.txt_ip_range = Entry(self.master, text = '')
        self.txt_ip_range.grid(row = 8, column = 4, columnspan = 2, padx = (10,20), pady = (50,10), sticky = 'new')
        self.lbl_ip_range = Label(self.master, text = 'IP Range (xxx.xxx.xxx) ')
        self.lbl_ip_range.grid(row = 8, column = 2, padx = (20,40), pady = (50,10), sticky = 'nw')

    def get_free_ip(self):
        count = 0
        for i in self.txt_ip_range.get(): 
            if i == '.': 
                count = count + 1
        if count != 2:
            messagebox.showinfo("Invalid IP Range"," Please input as xxx.xxx.xxx (Eg : 192.168.1)")
            return

        for i in range(1,255):
            res = connect_ip(self.txt_ip_range.get()+"."+str(i), 135)
            #res = pyping("192.168.100."+str(i))
            if res:
                print("Device found at: ", self.txt_ip_range.get()+"."+str(i) + ":"+str(135))
            else :
                messagebox.showinfo("Take your IP : ",self.txt_ip_range.get()+"."+str(i))
                break
    
if __name__ == "__main__":
    global window
    window = Tk()
    window.title("LIFE IT APP")

    notebook = ttk.Notebook(window)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    notebook.add(frame1, text="IP Table")
    notebook.add(frame2, text="IT Tools")
    notebook.grid()

    #Create tab frames
    app1 = phonebook(master=frame1)
    app1.grid()
    app2 = App2(master=frame2)
    app2.grid()


    #ph = phonebook(window)
    window.mainloop()
