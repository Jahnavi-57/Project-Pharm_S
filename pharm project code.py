import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import date
import time
from PIL import ImageTk,Image
import json



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  



# MySQL Connecting:

mydb=mysql.connector.connect(host='localhost',user='root',password='oranje57',database='pharm')
 


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# Tablet_list

def tablet_list():
    showtabletwin = tk.Toplevel()
    showtabletwin.geometry('1366x768')
    showtabletwin.title('Meds - List')
    showtabletwin.state('zoomed')
    showtabletwinpic = ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
    showtabletwinpanel = Label(showtabletwin, image=showtabletwinpic)
    showtabletwinpanel.pack(side='top', fill='both', expand='yes')
    
    tree = ttk.Treeview(showtabletwin, column=('#c1','#c2','#c3','#c4','#c5'), show='headings', height=25)
    tree.column('#1',width=140,minwidth=140,anchor=tk.CENTER)
    tree.column('#2',width=140,minwidth=140,anchor=tk.CENTER)
    tree.column('#3',width=140,minwidth=140,anchor=tk.CENTER)
    tree.column('#4',width=140,minwidth=140,anchor=tk.CENTER)
    tree.column('#5',width=140,minwidth=140,anchor=tk.CENTER)
    tree.heading('#1',text='Sno')
    tree.heading('#2',text='ID')
    tree.heading('#3',text='Tablet_name')
    tree.heading('#4',text='Availability')
    tree.heading('#5',text='Cost')
    tree.place(x=400, y=100)

    query = "SELECT * FROM tablets"
    mycur = mydb.cursor()
    mycur.execute(query)
    result = mycur.fetchall()
    for row in result:
        tree.insert("", "end", values=row)
        
        
    showtabletwin.mainloop()
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# update table

def update_table():
    
    upwin=tk.Toplevel()
    upwin.geometry('1366x768')
    upwin.title('Meds - Update')
    upwin.state('zoomed')
    upwinpic=ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
    upwinpanel=Label(upwin,image=upwinpic)
    upwinpanel.pack(side='top',fill='both',expand='yes')
    
    def ups():
        if old.get() == "tablet_name" or 'id':
            q="update tablets set {} = '{}' where tablet_name ='{}'".format(old.get(),new.get(),old1.get())
        else:
            q="update tablets set {} = {} where tablet_name ='{}'".format(old.get(),new.get(),old1.get())
        mycur = mydb.cursor()
        mycur.execute(q)
        mydb.commit()
        
        if ups:
            messagebox.showinfo('success',"A tablet record is updated")
            upwin.destroy()
        else: 
            messagebox.showerror('error',"tablet record is not updated")

    def refer():
        
        tree2 = ttk.Treeview(upwin, column=('#c1','#c2','#c3','#c4','#c5'), show='headings', height=1)
        tree2.column('#1',width=140,minwidth=140,anchor=tk.CENTER)
        tree2.column('#2',width=140,minwidth=140,anchor=tk.CENTER)
        tree2.column('#3',width=140,minwidth=140,anchor=tk.CENTER)
        tree2.column('#4',width=140,minwidth=140,anchor=tk.CENTER)
        tree2.column('#5',width=140,minwidth=140,anchor=tk.CENTER)
        tree2.heading('#1',text='Sno')
        tree2.heading('#2',text='ID')
        tree2.heading('#3',text='Tablet_name')
        tree2.heading('#4',text='Availability')
        tree2.heading('#5',text='Cost')
        tree2.place(x=750, y=100)

        q = f"SELECT * FROM tablets WHERE tablet_name = %s"
        mycur = mydb.cursor()
        mycur.execute(q, (old1.get(),))
        result = mycur.fetchall()
        for row in result:
            tree2.insert("", "end", values=row)
    
    Label(upwin, text="Edit Tablet",font=("italic_iv50",12), width=20).place(x=270, y=200)
    
    refbutton = Button(upwin, text="Refer",font=("italic_iv50",10),command=refer)
    refbutton.place(x=560, y=200)

    #-----------------------------------------------------------------------------------------

    def update_suggestions(event):
        input_text = old1.get().lower()
        matching_tablets = [row[2] for row in data if input_text in row[2].lower()][:4]
        suggestion_var.set(matching_tablets)

        if matching_tablets:
            suggestion_label.config(height=4)
            suggestion_label.place(x=370, y=280)
        else:
            suggestion_label.place_forget()
    def select_suggestion(event):
        selected_suggestion = suggestion_label.get(suggestion_label.curselection())
        old1.delete(0, tk.END)
        old1.insert(0, selected_suggestion)
        suggestion_label.place_forget()
        old1.focus_set()
    def handle_enter(event):
        suggestion_selection = suggestion_label.curselection()
        if suggestion_selection:
            selected_suggestion = suggestion_label.get(suggestion_selection)
            old1.delete(0, tk.END)
            old1.insert(0, selected_suggestion)
            suggestion_label.place_forget()
            old1.icursor(tk.END) 
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM tablets")
    data = mycur.fetchall()
    tab_label = tk.Label(upwin, text="Tablet Name",font=("italic_iv50",12), width=20)
    tab_label.place(x=200, y=250)
    old1 = tk.Entry(upwin)
    old1.place(x=500, y=250,height=30,width=180)
    old1.config(borderwidth=2, relief='sunken')
    old1.bind('<KeyRelease>', update_suggestions)
    old1.bind('<Down>', lambda e: suggestion_label.focus_set())
    old1.bind('<Return>', handle_enter)
    suggestion_var = tk.StringVar()
    suggestion_label = tk.Listbox(upwin, listvariable=suggestion_var, height=4)
    suggestion_label.bind('<ButtonRelease-1>', select_suggestion)
    suggestion_label.bind('<Return>', handle_enter) 

    #---------------------------------------------------------------------------------------

    label = Label(upwin, text="Col. to change",font=("italic_iv50",12), width=20)
    label.place(x=200, y=400)
    

    old = tk.StringVar()
    options = ["Select","id", "tablet_name", "availability","cost"]
    ttk.Combobox(upwin, textvariable=old, values=options).place(x=500, y=400,height=30,width=180)
    old.set(options[0])

    subject_label = Label(upwin, text="New Value",font=("italic_iv50",11), width=20)
    subject_label.place(x=200, y=450)

    new = Entry(upwin)
    new.place(x=500, y=450,height=30,width=180)
    new.config(borderwidth=2, relief='sunken')

    create_table_button = Button(upwin, text="Update",font=("italic_iv50",10), command=ups)
    create_table_button.place(x=700, y=450)
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def delll():
        dell2=dell.get()
        q="delete from tablets where tablet_name='{}'".format(dell2)
        mycur = mydb.cursor()
        mycur.execute(q)
        mydb.commit()
        
        if delll:
            messagebox.showinfo('success',"A tablet record is deleted")
            upwin.destroy()
        else: 
            messagebox.showerror('error',"tablet record is not deleted")
        
    Label(upwin, text="Delete Tablet",font=("italic_iv50",12), width=20).place(x=900, y=200,)
    
    label2 = Label(upwin, text="Tablet Name",font=("italic_iv50",12), width=20)
    label2.place(x=800, y=250)
    
    #---------------------------------------------------------------------------------------
    
    def update_suggestions2(event):
        input_text2 = dell.get().lower()
        matching_tablets2 = [row[2] for row in data if input_text2 in row[2].lower()][:4]
        suggestion_var2.set(matching_tablets2)

        if matching_tablets2:
            suggestion_label2.config(height=4)
            suggestion_label2.place(x=970, y=280)
        else:
            suggestion_label2.place_forget()
    def select_suggestion2(event):
        selected_suggestion2 = suggestion_label2.get(suggestion_label2.curselection())
        dell.delete(0, tk.END)
        dell.insert(0, selected_suggestion2)
        suggestion_label2.place_forget()
        dell.focus_set()
    def handle_enter2(event):
        suggestion_selection2 = suggestion_label2.curselection()
        if suggestion_selection2:
            selected_suggestion2 = suggestion_label2.get(suggestion_selection2)
            dell.delete(0, tk.END)
            dell.insert(0, selected_suggestion2)
            suggestion_label2.place_forget()
            dell.icursor(tk.END) 
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM tablets")
    data = mycur.fetchall()
    dell = tk.Entry(upwin)
    dell.place(x=1070, y=250,height=30,width=180)
    dell.config(borderwidth=2, relief='sunken')
    dell.bind('<KeyRelease>', update_suggestions2)
    dell.bind('<Down>', lambda e: suggestion_label2.focus_set())
    dell.bind('<Return>', handle_enter2)
    suggestion_var2 = tk.StringVar()
    suggestion_label2 = tk.Listbox(upwin, listvariable=suggestion_var2, height=4)
    suggestion_label2.bind('<ButtonRelease-1>', select_suggestion2)
    suggestion_label2.bind('<Return>', handle_enter2) 
    
    #---------------------------------------------------------------------------------------
    
    del_table_button = Button(upwin, text="Delete",font=("italic_iv50",10),command=delll)
    del_table_button.place(x=1300, y=250)
    
    
    
    upwin.mainloop()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  



# insert Page:

def insert_page():
    
    insertwin = tk.Toplevel()
    insertwin.geometry('1366x768')
    insertwin.title('Meds - Add tablets')
    insertwin.state('zoomed')
    insertwinpic = ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
    insertwinpanel = tk.Label(insertwin, image=insertwinpic)
    insertwinpanel.pack(side='top', fill='both', expand='yes')  
    
    def remove_rec():
        selected_index = listbox.curselection()
        if selected_index:
            listbox.delete(selected_index)
            
    def add_rec():
        subject = subj_entry.get()
        if subject:
            listbox.insert(tk.END, subject)
            subj_entry.delete(0, tk.END)
            
    def allin():
        tup = []
        for i in range(4):
            rec_name = listbox.get(i)
            if i<2:
                rec_name = str(rec_name)
            else:
                rec_name = int(rec_name)
                
            tup.append(rec_name)
    
        tup = tuple(tup)
        query = f"INSERT INTO tablets(id, tablet_name , availability, cost) VALUES {tup}"
        mycur=mydb.cursor()
        mycur.execute(query)

        mydb.commit()
        
        if allin:
            messagebox.showinfo('success',"A Tablet record is added")
            insertwin.destroy()
        else: 
            messagebox.showerror('error',"Tablet record is not added")
        
        
    
    Label(insertwin, text='''Tablet_Id
Tablet_Name
Availability
Cost''', width=25,font=("italic_iv50",11)).place(x=500, y=100)

    listbox = Listbox(insertwin, height=4, width=40)
    listbox.place(x=200, y=300)

    Label(insertwin, text="Enter record : ", width=20,font=("italic_iv50",12)).place(x=200, y=250)
    subj_entry = Entry(insertwin)
    subj_entry.place(x=500, y=250,height=25,width=180)

    add_subject_button = Button(insertwin, text="Add Record",font=("italic_iv50",12), command=add_rec)
    add_subject_button.place(x=500, y=300)
    Button(insertwin, text="Remove Tablet",font=("italic_iv50",12), command=remove_rec).place(x=500, y=350)
    button = Button(insertwin, text="Insert",font=("italic_iv50",12), command=allin)
    button.place(x=500, y=492)

    mydb.commit()

    
    insertwin.mainloop()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


#bill

def bill():
    billwin = tk.Toplevel()
    billwin.geometry('1366x768')
    billwin.title('Meds - Bill')
    billwin.state('zoomed')
    billwinpic = ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
    billwinpanel = Label(billwin, image=billwinpic)
    billwinpanel.pack(side='top', fill='both', expand='yes')
    
    def pay():
        selected_tablets = []
        selected_qty = []
        total_cost = 0

        for i in range(listbox1.size()):
            selected_tablet = listbox1.get(i)
            selected_tablets.append(selected_tablet)
            
            qty = int(listbox2.get(i))
            selected_qty.append(qty)
            
            for row in data:
                if row[2] == selected_tablet:
                    total_cost += row[4]*qty

        json_selected_tablets = json.dumps(selected_tablets)
        json_selected_qty = json.dumps(selected_qty)

        query = "INSERT INTO customers(customer_name, phn_no, tablets_purchased, tablets_qty,  total_cost) VALUES ('{}', {}, '{}','{}',{})".format(name.get(), ph.get(), json_selected_tablets,json_selected_qty,total_cost)

        mycur = mydb.cursor()
        mycur.execute(query)
        mydb.commit()

        if mycur.rowcount > 0:
            for i, selected_tablet in enumerate(selected_tablets):
                update_query = "UPDATE tablets SET availability = availability - {} WHERE tablet_name = '{}'".format(selected_qty[i], selected_tablet)
                mycur.execute(update_query)
                mydb.commit()
            messagebox.showinfo('Success', 'Purchase Successful')
            billwin.destroy()
        else:
            messagebox.showerror('Error', 'BILL ERROR')   
        
    
    def add_rec():
        sub = sub_entry.get()
        qt = qt_entry.get()

        if sub and qt:
            mycur = mydb.cursor()

            query = "SELECT availability FROM tablets WHERE tablet_name = %s"
            mycur.execute(query, (sub,))
            result = mycur.fetchone()

            if result:
                availability = result[0]
                if int(qt) > availability:
                    messagebox.showinfo('Error', 'Insufficient tablet availability')
                else:
                    listbox1.insert(tk.END, sub)
                    sub_entry.delete(0, tk.END)
                    listbox2.insert(tk.END, qt)
                    qt_entry.delete(0, tk.END)
            else:
                messagebox.showinfo('Error', 'Tablet not found')

            mycur.close()
        else:
            messagebox.showinfo('Error', 'Give tablet name and quantity')

            
            
    def remove_rec():
        selected_index = listbox1.curselection() or listbox2.curselection()
        if selected_index:
            listbox1.delete(selected_index)
            listbox2.delete(selected_index)
    
    
    tree4 = ttk.Treeview(billwin, column=('#c1','#c2','#c3','#c4','#c5'), show='headings', height=25)
    tree4.column('#1',width=80,minwidth=80,anchor=tk.CENTER)
    tree4.column('#2',width=100,minwidth=100,anchor=tk.CENTER)
    tree4.column('#3',width=150,minwidth=150,anchor=tk.CENTER)
    tree4.column('#4',width=110,minwidth=110,anchor=tk.CENTER)
    tree4.column('#5',width=110,minwidth=110,anchor=tk.CENTER)
    tree4.heading('#1',text='Sno')
    tree4.heading('#2',text='ID')
    tree4.heading('#3',text='Tablet name')
    tree4.heading('#4',text='Availablity')
    tree4.heading('#5',text='Cost')
    tree4.place(x=850, y=100)
    query = "SELECT * FROM tablets"
    mycur = mydb.cursor()
    mycur.execute(query)
    result = mycur.fetchall()
    for row in result:
        tree4.insert("", "end", values=row)


    qu="select * from tablets"
    mycur=mydb.cursor()
    mycur.execute(qu)
    data = mycur.fetchall()
    mydb.commit
    
    Label(billwin, text="Name:",font=("italic_iv50",12), width=20).place(x=200, y=200)
    name = Entry(billwin)
    name.place(x=500, y=200,height=25,width=180)
    name.config(borderwidth=2, relief='sunken')
    
    Label(billwin, text="Phone:",font=("italic_iv50",12), width=20).place(x=200, y=250)
    ph = Entry(billwin)
    ph.place(x=500, y=250,height=25,width=180)
    ph.config(borderwidth=2, relief='sunken')
    
    Label(billwin, text="Enter Tablet : ",font=("italic_iv50",12), width=20).place(x=200, y=300)
    
    #-------------------------------------------------------------------------------------------
    
    def update_suggestions3(event):
        input_text3 = sub_entry.get().lower()
        matching_tablets3 = [row[2] for row in data if input_text3 in row[2].lower()][:4]
        suggestion_var3.set(matching_tablets3)

        if matching_tablets3:
            suggestion_label3.config(height=4)
            suggestion_label3.place(x=500, y=320)
        else:
            suggestion_label3.place_forget()
    def select_suggestion3(event):
        selected_suggestion3 = suggestion_label3.get(suggestion_label3.curselection())
        sub_entry.delete(0, tk.END)
        sub_entry.insert(0, selected_suggestion3)
        suggestion_label3.place_forget()
        sub_entry.focus_set()
    def handle_enter3(event):
        suggestion_selection3 = suggestion_label3.curselection()
        if suggestion_selection3:
            selected_suggestion3 = suggestion_label3.get(suggestion_selection3)
            sub_entry.delete(0, tk.END)
            sub_entry.insert(0, selected_suggestion3)
            suggestion_label3.place_forget()
            sub_entry.icursor(tk.END) 
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM tablets")
    data = mycur.fetchall()
    sub_entry = tk.Entry(billwin)
    sub_entry.place(x=500, y=300,height=25,width=180)
    sub_entry.config(borderwidth=2, relief='sunken')
    sub_entry.bind('<KeyRelease>', update_suggestions3)
    sub_entry.bind('<Down>', lambda e: suggestion_label3.focus_set())
    sub_entry.bind('<Return>', handle_enter3)
    suggestion_var3 = tk.StringVar()
    suggestion_label3 = tk.Listbox(billwin, listvariable=suggestion_var3, height=4)
    suggestion_label3.bind('<ButtonRelease-1>', select_suggestion3)
    suggestion_label3.bind('<Return>', handle_enter3) 
    
    #-------------------------------------------------------------------------------------------
    
    Label(billwin, text="Enter Quantity : ",font=("italic_iv50",12), width=20).place(x=200, y=450)
    qt_entry = Entry(billwin)
    qt_entry.place(x=500, y=450,height=25,width=100)
    
    listbox1 = Listbox(billwin, height=8, width=40)
    listbox1.place(x=370, y=500,)
    
    listbox2 = Listbox(billwin, height=8, width=20)
    listbox2.place(x=650, y=500)
    
    Button(billwin, text="Add Tablet",font=("italic_iv50",9),command=add_rec).place(x=620, y=450)
    Button(billwin, text="Remove Tablet",font=("italic_iv50",9), command=remove_rec).place(x=720, y=450)
    Button(billwin, text="Pay",font=("italic_iv50",9), command=pay).place(x=800, y=500)
    billwin.mainloop()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  



# history

def history():
    historywin = tk.Toplevel()
    historywin.geometry('1366x768')
    historywin.title('Meds - History')
    historywin.state('zoomed')
    historywinpic = ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
    historywinpanel = Label(historywin, image=historywinpic)
    historywinpanel.pack(side='top', fill='both', expand='yes')
    
    
    tree3 = ttk.Treeview(historywin, column=('#c1','#c2','#c3','#c4','#c5','#c6'), show='headings', height=25)
    tree3.column('#1',width=40,anchor=tk.CENTER)
    tree3.column('#2',width=200,anchor=tk.CENTER)
    tree3.column('#3',width=140,anchor=tk.CENTER)
    tree3.column('#4',width=600,anchor=tk.CENTER)
    tree3.column('#5',width=250,anchor=tk.CENTER)
    tree3.column('#6',width=100,anchor=tk.CENTER)
    tree3.heading('#1',text='Sno')
    tree3.heading('#2',text='Name')
    tree3.heading('#3',text='Phone')
    tree3.heading('#4',text='Tablets')
    tree3.heading('#5',text='Quantity')
    tree3.heading('#6',text='Bill Cost')
    tree3.place(x=100, y=100)

    query = "SELECT * FROM customers"
    mycur = mydb.cursor()
    mycur.execute(query)
    result = mycur.fetchall()
    for row in result:
        tree3.insert("", "end", values=row)
        
        

    historywin.mainloop()

      
      
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  




# Page Close Confirmations (Messagebox):

def homelogout():

    messagebox.showinfo('Thank You','Logged out successfully')
    home.destroy()

def homeclose():

    if messagebox.askokcancel('Quit','Do you want to logout and quit?'):
        home.destroy()
        quit()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  

    
# Welcome text
def update_welcome_text_position():
    canvas.move(welcome_text, 1, 0)
    x, _ = canvas.coords(welcome_text)
    if x > canvas.winfo_width():
        canvas.move(welcome_text, -canvas.winfo_width(), 0)
    home.after(10, update_welcome_text_position)



# Home Page:


home=tk.Tk()
home.geometry('1366x768')
home.title('Meds')
home.state('zoomed')
home.protocol('WM_DELETE_WINDOW',homeclose)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------
canvas = tk.Canvas(home, width=home.winfo_screenwidth(), height=35)
canvas.pack()
welcome_text = canvas.create_text(0, 20, text="Welcome to the Pharmaceutical Stores!", font=("Italic_IV50", 20), anchor="w",fill="green")  
update_welcome_text_position()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------


currtime=time.strftime('%H:%M')
currdate=date.today().strftime("%d/%m/%Y")

homepic=ImageTk.PhotoImage(Image.open("C:\\Users\\M.Jahnavi\\OneDrive - Amrita Vishwa Vidyapeetham- Chennai Campus\\Sem-3\DBMS\\Project pharmacy\\Pharmacy_front.jpeg"))
homepanel=Label(home,image=homepic)
homepanel.pack(side='top',fill='both',expand='yes')


Label(home,text=('Logged in: '+currtime+', '+currdate),font=('italic_iv50',16),bg='pink').place(x=980,y=100)


Button(home,text='Bill',font=('italic_iv50',20),command=bill,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=400,y=250)
Button(home,text='Customer History',font=('italic_iv50',20),command=history,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=400,y=350)


Button(home,text='Show Tablets',font=('italic_iv50',20),command=tablet_list,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=850,y=250)
Button(home,text='Edit Tablets',font=('italic_iv50',20),command=update_table,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=850,y=350)
Button(home,text='Add Tablets',font=('italic_iv50',20),command=insert_page,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=850,y=450)


Button(home,text='Logout',font=('italic_iv50',20),command=homelogout,height=1,width=10,bg='pink').place(x=1100,rely=0.85)


home.mainloop()
