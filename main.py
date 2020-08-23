# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:26:38 2018
Updated on Sunday August 23 20:52:00 2020
@author: hnambur
@author: azeembukhariprivate
"""
import sqlite3
from tkinter import Frame,Tk,Label,Entry,Scrollbar,Listbox,Button,END,VERTICAL

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
        self.txt_fname.delete(0,END)
        self.txt_lname.delete(0,END)
        self.txt_phone.delete(0,END)
        self.txt_email.delete(0,END)
    def load_list(self):
        print("Load List")
        
    def on_select(self,event):
        id_list = event.widget
        #selection_id = id_list.curselection()[0]
        #name = id_list.get(selection_id)
        #data = self.my_db.get_record(name)
        self.txt_fname.delete(0, END)
        self.txt_fname.insert(0,data[0])
        self.txt_lname.delete(0, END)
        self.txt_lname.insert(0,data[1])
        self.txt_phone.delete(0, END)
        self.txt_phone.insert(0,data[2])
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
        
    def connect_db(self):
        self.conn = create_connection("recipebook.db")

    def onClickFind(self):
        print ("Find")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM issuingTable WHERE name LIKE ?", ('%'+ self.txt_fname.get() + '%',))
        rows = cur.fetchall()
        self.txt_phone.delete(0, END)
        self.txt_fname.delete(0, END)
        self.txt_fname.insert(0,rows[0][1])
        self.txt_phone.insert(0,rows[0][10])

    def onClickAdd(self):
        print ("Add")
        sql = ''' INSERT INTO issuingTable (name,whatsapp)
                  VALUES(?,?) '''
        data = (self.txt_fname.get(),self.txt_phone.get())
        print ("data : ", data)
        cur = self.conn.cursor()
        cur.execute(sql,data)
        self.conn.commit()
    
    def load_gui(self):
    #setting up gui labels
        self.lbl_fname = Label(self.master, text = 'First Name: ')
        self.lbl_fname.grid(row = 0, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_lname = Label(self.master, text = 'Last Name: ')
        self.lbl_lname.grid(row = 2, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_phone = Label(self.master, text = 'Phone: ')
        self.lbl_phone.grid(row = 4, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_email = Label(self.master, text = 'Email: ')
        self.lbl_email.grid(row = 6, column = 0, padx = (27,0), pady = (10,0), sticky = 'nw')
        self.lbl_user = Label(self.master, text = 'User: ')
        self.lbl_user.grid(row = 0, column = 2, padx = (0,0), pady = (10,0), sticky = 'nw')
        #setting up gui entry fields
        self.txt_fname = Entry(self.master, text = '')
        self.txt_fname.grid(row = 1, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_lname = Entry(self.master, text = '')
        self.txt_lname.grid(row = 3, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_phone = Entry(self.master, text = '')
        self.txt_phone.grid(row = 5, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        self.txt_email = Entry(self.master, text = '')
        self.txt_email.grid(row = 7, column = 0, columnspan = 2, padx = (30,40), pady = (0,0), sticky = 'new')
        #setting up listbox and the scrollbar
        self.scrollbar1 = Scrollbar(self.master, orient = VERTICAL)
        self.lstList1 = Listbox(self.master, exportselection = 0, yscrollcommand = self.scrollbar1.set)
        self.lstList1.bind('<<ListboxSelect>>', self.on_select)
        self.scrollbar1.config(command = self.lstList1.yview)
        self.scrollbar1.grid(row = 1, column = 5, rowspan = 7, sticky = 'nes')
        self.lstList1.grid(row = 1, column = 2, rowspan = 7, columnspan = 3, sticky = 'nsew')
        #setting up buttons
        self.btn_add = Button(self.master, width = 12, height = 2, text = 'Add', command = lambda: self.onClickAdd())
        self.btn_add.grid(row = 8, column = 0, padx = (25,0), pady = (45,10), sticky = 'w')
        self.btn_add = Button(self.master, width = 12, height = 2, text = 'Find', command = lambda: self.onClickFind())
        self.btn_add.grid(row = 8, column = 1, padx = (25,0), pady = (45,10), sticky = 'w')
        self.btn_update = Button(self.master, width = 12, height = 2, text = 'Update', command = lambda: phonebook_func.onUpdate(self))
        self.btn_update.grid(row = 8, column = 2, padx = (15,0), pady = (45,10), sticky = 'w')
        self.btn_delete = Button(self.master, width = 12, height = 2, text = 'Delete', command = lambda: phonebook_func.onDelete(self))
        self.btn_delete.grid(row = 8, column = 3, padx = (15,0), pady = (45,10), sticky = 'w')
        self.btn_close = Button(self.master, width = 12, height = 2, text = 'Close', command = self.on_close)
        self.btn_close.grid(row = 8, column = 4, padx = (15,0), pady = (45,10), sticky = 'e')
if __name__ == "__main__":
    root = Tk()
    ph = phonebook(root)
    root.mainloop()