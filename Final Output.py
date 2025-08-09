from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from captcha_test import generate_captcha
from PIL import Image,ImageTk
import time,random
from table_creation import generate
from email_test import send_openacn_ack,send_otp,send_otp_4_pass
import sqlite3
from tkinter import ttk
import re

generate()

def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt) #ms (1 sec)

list_imgs=['images/logo1.jpg','images/logo2.png','images/logo3.jpg','images/logo4.jpg','images/logo.jpg']
    
root=Tk()
root.state('zoomed')
root.configure(bg='pink')

list_imgs=['images/logo1.jpg', 'images/logo2.png', 'images/logo3.jpg', 'images/logo4.jpg']

def image_animation():
    index = random.randint(0, len(list_imgs) - 1)
    img = Image.open(list_imgs[index]).resize((250, 115))
    imgtk = ImageTk.PhotoImage(img, master=root)
    logo_lbl.configure(image=imgtk)
    logo_lbl.image = imgtk  # Keep a reference to avoid garbage collection
    logo_lbl.after(500, image_animation)
    # Create the logo label once

title_lbl=Label(root,text="Banking Automation",fg='blue',bg='pink',font=('Arial',50,'bold','underline'))
title_lbl.pack()

dt_lbl=Label(root,font=('Arial',15),bg='pink')
dt_lbl.pack(pady=5)
show_dt()

img = Image.open(list_imgs[0]).resize((250, 115))
imgtk = ImageTk.PhotoImage(img, master=root)
logo_lbl = Label(root, image=imgtk)
logo_lbl.place(relx=0, rely=0)
# Start the animation
image_animation()

footer_lbl=Label(root,font=('Arial',20,'bold'),fg='blue',bg='pink',text="Developed By\nYogRajMalik @ 9990576610")
footer_lbl.pack(side='bottom')

code_captcha=generate_captcha()

def main_screen():
    def refresh_captcha():
        global code_captcha
        code_captcha=generate_captcha()
        captcha_value_lbl.configure(text=code_captcha)
    
          
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    
    def forgot():
        frm.destroy()
        fp_screen()

    def login():
        utype=acntype_cb.get()
        uacn=acnno_e.get()
        upass=pass_e.get()

        ucaptcha=captcha_e.get()
        global code_captcha
        code_captcha=code_captcha.replace(' ','')

        if utype=="Admin":
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid captcha")
            else:
                messagebox.showerror("Login","You are not Admin!")
        else:
                       
            if code_captcha==ucaptcha:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacn,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])
            else:
                messagebox.showerror("Login","Invalid captcha")

    acntype_lbl=Label(frm,text='ACN Type',font=('Arial',20,'bold'),bg='powder blue')
    acntype_lbl.place(relx=.3,rely=.1)

    acntype_cb=Combobox(frm,values=['User','Admin'],font=('Arial',20,'bold'))
    acntype_cb.current(0)
    acntype_cb.place(relx=.45,rely=.1)

    acnno_lbl=Label(frm,text='🔑ACN',font=('Arial',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()

    pass_lbl=Label(frm,text='🔒 Pass',font=('Arial',20,'bold'),bg='powder blue')
    pass_lbl.place(relx=.3,rely=.3)

    pass_e=Entry(frm,font=('Arial',20,'bold'),bd=5,show='*')
    pass_e.place(relx=.45,rely=.3)

    captcha_lbl=Label(frm,text='Captcha',font=('Arial',20,'bold'),bg='powder blue')
    captcha_lbl.place(relx=.3,rely=.4)

    captcha_value_lbl=Label(frm,text=code_captcha,fg='green',font=('Arial',20,'bold'))
    captcha_value_lbl.place(relx=.45,rely=.4)

    refresh_btn=Button(frm,text="refresh 🔄",command=refresh_captcha)
    refresh_btn.place(relx=.6,rely=.4)

    captcha_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
    captcha_e.place(relx=.45,rely=.5)

    submit_btn=Button(frm,text="Login",command=login,width=17,bg='pink',bd=5,font=('Arial',20,'bold'))
    submit_btn.place(relx=.45,rely=.6)

    fp_btn=Button(frm,text="Forgot Pass",width=17,command=forgot,bg='pink',bd=5,font=('Arial',20,'bold'))
    fp_btn.place(relx=.45,rely=.7)



def fp_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    def back():
        frm.destroy()
        main_screen()

    def fp_pass():
        ueamil=email_e.get()
        uacn=acnno_e.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))
        torow=curobj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Password","ACN does not exist")
        else:
            if ueamil==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_4_pass(ueamil,otp)
                messagebox.showinfo("Forgot Pasword","Otp sent to registered email,kindly verify")
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='select acn_pass from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Forgot Password',f"Your Password is {curobj.fetchone()[0]} ")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Forgot Password","Invalid otp!")

                otp_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()

                verify_btn=Button(frm,command=verify_otp,text="verify",bg='pink',bd=3,font=('Arial',15))
                verify_btn.place(relx=.8,rely=.6)

            else:
                messagebox.showerror("Forgot Password","Email is not matched")

    back_btn=Button(frm,text="back",bg='pink',bd=5,font=('Arial',20,'bold'),command=back)
    back_btn.place(relx=0,rely=0)

    acnno_lbl=Label(frm,text='🔑ACN',font=('Arial',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()

    email_lbl=Label(frm,text='📧Email',font=('Arial',20,'bold'),bg='powder blue')
    email_lbl.place(relx=.3,rely=.3)

    email_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
    email_e.place(relx=.45,rely=.3)
    
    sub_btn=Button(frm,command=fp_pass,text="Submit",bg='pink',bd=5,font=('Arial',20,'bold'))
    sub_btn.place(relx=.5,rely=.4)

def admin_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#1eff00")
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    def logout():
  
        frm.destroy()
        main_screen()

    logout_btn=Button(frm,text="logout",bg='pink',bd=5,font=('Arial',20,'bold'),command=logout)
    logout_btn.place(relx=.9,rely=0)

    def open():
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This open account screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def openac():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            uadhar=adhar_e.get()
            uadr=adr_e.get()
            udob=dob_e.get()
            upass=generate_captcha()
            upass=upass.replace(' ','')
            ubal=0
            uopendate=time.strftime("%A %d-%b-%Y")

            #empty validation
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0:
                messagebox.showerror("Open Account","Empty fields are not allowed")
                return

            #email validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of email")
                return
            
            #mob validation
            match=re.fullmatch("[6-9][0-9]{9}",umob)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of mob")
                return
            
            #mob adhar
            match=re.fullmatch("[0-9]{12}",uadhar)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of adhar")
                return
            

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendate))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select max(acn_acno) from accounts")
            uacn=curobj.fetchone()[0]
            conobj.close()
            send_openacn_ack(uemail,uname,uacn,upass)
            messagebox.showinfo("Account","Account Opened and details sent to email")
            frm.destroy()
            admin_screen()

        name_lbl=Label(ifrm,text='Name',font=('Arial',20,'bold'),bg='white')
        name_lbl.place(relx=.05,rely=.15)

        name_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        name_e.place(relx=.15,rely=.15)
        name_e.focus()

        email_lbl=Label(ifrm,text='Email',font=('Arial',20,'bold'),bg='white')
        email_lbl.place(relx=.05,rely=.4)

        email_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        email_e.place(relx=.15,rely=.4)

        mob_lbl=Label(ifrm,text='Mob',font=('Arial',20,'bold'),bg='white')
        mob_lbl.place(relx=.05,rely=.65)

        mob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        mob_e.place(relx=.15,rely=.65)

        adhar_lbl=Label(ifrm,text='Adhar',font=('Arial',20,'bold'),bg='white')
        adhar_lbl.place(relx=.5,rely=.15)

        adhar_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        adhar_e.place(relx=.6,rely=.15)

        adr_lbl=Label(ifrm,text='Adress',font=('Arial',20,'bold'),bg='white')
        adr_lbl.place(relx=.5,rely=.4)

        adr_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        adr_e.place(relx=.6,rely=.4)

        dob_lbl=Label(ifrm,text='DOB',font=('Arial',20,'bold'),bg='white')
        dob_lbl.place(relx=.5,rely=.65)

        dob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        dob_e.place(relx=.6,rely=.65)

        open_btn=Button(ifrm,command=openac,text="Open ACN",fg='green',bd=5,font=('Arial',20,'bold'))
        open_btn.place(relx=.8,rely=.8)

    def close():
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This close account screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def sent_close_otp():
            uacn=acnno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Close Account","ACN does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_4_pass(torow[3],otp)
                messagebox.showinfo("close Account","Otp sent to registered email,kindly verify")
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='delete from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Close Account',"Account Closed ")
                            conobj.commit()
                            conobj.close()
                            frm.destroy()
                            admin_screen()
                        else:
                            messagebox.showerror("Close Account","Invalid otp!")

                otp_e=Entry(frm,font=('Arial',20,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()

                verify_btn=Button(frm,command=verify_otp,text="verify",bg='pink',bd=3,font=('Arial',15))
                verify_btn.place(relx=.8,rely=.6)

        acnno_lbl=Label(ifrm,text='🔑ACN',font=('Arial',20,'bold'),bg='powder blue')
        acnno_lbl.place(relx=.3,rely=.2)

        acnno_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        acnno_e.place(relx=.45,rely=.2)
        acnno_e.focus()

        otp_btn=Button(ifrm,command=sent_close_otp,width=10,text="Send OTP",bd=5,font=('Arial',20,'bold'))
        otp_btn.place(relx=.6,rely=.3)

    def view():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This view account screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        tree = ttk.Treeview(ifrm, columns=("A","B","C","D","E","F"), show="headings")
        tree.heading("A", text="ACN0.")
        tree.heading("B", text="NAME")
        tree.heading("C", text="Email")
        tree.heading("D", text="MOB")
        tree.heading("E", text="OPEN DATE")
        tree.heading("F", text="BALANCE")

        tree.column("A", width=100,anchor="center")
        tree.column("B", width=150,anchor="center")
        tree.column("C", width=200,anchor="center")
        tree.column("D", width=100,anchor="center")
        tree.column("E", width=100,anchor="center")
        tree.column("F", width=100,anchor="center")
        
        
        tree.place(relx=.1,rely=.1,relwidth=.8,relheight=.4) 

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        curobj.execute(query)
        for tup in curobj.fetchall():
            tree.insert("", "end", values=tup)
        conobj.close()
       
    open_btn=Button(frm,width=10,text="Open ACN",command=open,fg='green',bd=5,font=('Arial',20,'bold'))
    open_btn.place(relx=.001,rely=.1)

    close_btn=Button(frm,width=10,text="Close ACN",command=close,fg='red',bd=5,font=('Arial',20,'bold'))
    close_btn.place(relx=.001,rely=.3)

    view_btn=Button(frm,width=10,text="View ACN",command=view,fg='blue',bd=5,font=('Arial',20,'bold'))
    view_btn.place(relx=.001,rely=.5)

def user_screen(uacn,uname):
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)

    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacn,))
    row=curobj.fetchone()
    conobj.close()

    def logout():
        frm.destroy()
        main_screen()

    def check():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This is check detials screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        acn_lbl=Label(ifrm,text=f"Account No\t=\t{row[0]}",font=('Arial',15),bg='white',fg='black')
        acn_lbl.place(relx=.2,rely=.1)

        bal_lbl=Label(ifrm,text=f"Account Bal\t=\t{row[8]}",font=('Arial',15),bg='white',fg='black')
        bal_lbl.place(relx=.2,rely=.3)

        open_lbl=Label(ifrm,text=f"Open Date\t=\t{row[9]}",font=('Arial',15),bg='white',fg='black')
        open_lbl.place(relx=.2,rely=.5)

        dob_lbl=Label(ifrm,text=f"Date of birth\t=\t{row[7]}",font=('Arial',15),bg='white',fg='black')
        dob_lbl.place(relx=.2,rely=.7)

        adhar_lbl=Label(ifrm,text=f"ADHAR No\t=\t{row[5]}",font=('Arial',15),bg='white',fg='black')
        adhar_lbl.place(relx=.2,rely=.9)


    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This is update detials screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def update_details():
            uname=name_e.get()
            upass=pass_e.get()
            uemail=email_e.get()
            umob=mob_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")
            frm.destroy()
            user_screen(uacn,None)

        name_lbl=Label(ifrm,text='Name',font=('Arial',20,'bold'),bg='white')
        name_lbl.place(relx=.05,rely=.15)

        name_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        name_e.place(relx=.15,rely=.15)
        name_e.focus()
        name_e.insert(0,row[1])

        email_lbl=Label(ifrm,text='Email',font=('Arial',20,'bold'),bg='white')
        email_lbl.place(relx=.05,rely=.4)

        email_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        email_e.place(relx=.15,rely=.4)
        email_e.insert(0,row[3])

        mob_lbl=Label(ifrm,text='Mob',font=('Arial',20,'bold'),bg='white')
        mob_lbl.place(relx=.5,rely=.4)

        mob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        mob_e.place(relx=.6,rely=.4)
        mob_e.insert(0,row[4])

        pass_lbl=Label(ifrm,text='Pass',font=('Arial',20,'bold'),bg='white')
        pass_lbl.place(relx=.5,rely=.15)

        pass_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        pass_e.place(relx=.6,rely=.15)
        pass_e.insert(0,row[2])

        update_btn=Button(ifrm,command=update_details,text="update",bg='pink',bd=5,font=('Arial',20,'bold'))
        update_btn.place(relx=.7,rely=.6)



    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This is deposit screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def deposit_amt():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposit',f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn,None)

        amt_lbl=Label(ifrm,text='Amount',font=('Arial',20,'bold'),bg='white')
        amt_lbl.place(relx=.2,rely=.15)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.15)
        amt_e.focus()

        deposit_btn=Button(ifrm,command=deposit_amt,text="deposit",bg='pink',bd=5,font=('Arial',20,'bold'))
        deposit_btn.place(relx=.6,rely=.4)

    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This is withdraw screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def withdraw_amt():
            uamt=float(amt_e.get())
            if row[8]>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Withdraw',f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn,None)
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")

        amt_lbl=Label(ifrm,text='Amount',font=('Arial',20,'bold'),bg='white')
        amt_lbl.place(relx=.2,rely=.15)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.15)
        amt_e.focus()

        withdraw_btn=Button(ifrm,command=withdraw_amt,text="withdraw",bg='pink',bd=5,font=('Arial',20,'bold'))
        withdraw_btn.place(relx=.6,rely=.4)

    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.6)

        t_lbl=Label(ifrm,text='This is transfer screen',font=('Arial',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()
    
        def transfer_amt():
            toacn=to_e.get()
            uamt=float(amt_e.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(toacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Transfer","To ACN does not exist")
            else:
                if row[8]>=uamt:
                    otp=random.randint(1000,9999)
                    send_otp(row[3],otp,uamt)
                    messagebox.showinfo("Transfer","Otp sent to registered email,kindly verify")
                    def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                            query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                            
                            curobj.execute(query1,(uamt,uacn))
                            curobj.execute(query2,(uamt,toacn))
                            
                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo('Transfer',f"{uamt} Amount Transfered")
                            frm.destroy()
                            user_screen(uacn,None)
                        else:
                            messagebox.showerror("Transfer","Invalid otp!")

                    otp_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
                    otp_e.place(relx=.4,rely=.6)
                    amt_e.focus()

                    verify_btn=Button(ifrm,command=verify_otp,text="verify",bg='pink',bd=3,font=('Arial',15))
                    verify_btn.place(relx=.8,rely=.6)
                else:
                    messagebox.showerror("Transfer","Insufficient Bal")

        to_lbl=Label(ifrm,text='To ACN',font=('Arial',20,'bold'),bg='white')
        to_lbl.place(relx=.2,rely=.15)

        to_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        to_e.place(relx=.4,rely=.15)
        to_e.focus()

        amt_lbl=Label(ifrm,text='Amount',font=('Arial',20,'bold'),bg='white')
        amt_lbl.place(relx=.2,rely=.3)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.3)

        transfer_btn=Button(ifrm,command=transfer_amt,text="transfer",bg='pink',bd=5,font=('Arial',20,'bold'))
        transfer_btn.place(relx=.6,rely=.45)

    logout_btn=Button(frm,text="logout",bg='pink',bd=5,font=('Arial',20,'bold'),command=logout)
    logout_btn.place(relx=.92,rely=0)

    wel_lbl=Label(frm,text=f'Welcome,{row[1]}',font=('Arial',20,'bold'),bg='powder blue',fg='purple')
    wel_lbl.place(relx=0,rely=0)

    check_btn=Button(frm,width=15,command=check,text="Check Details",fg='brown',bd=5,font=('Arial',20,'bold'))
    check_btn.place(relx=.001,rely=.15)

    update_btn=Button(frm,width=15,command=update,text="Update Details",fg='blue',bd=5,font=('Arial',20,'bold'))
    update_btn.place(relx=.001,rely=.3)

    deposit_btn=Button(frm,width=15,command=deposit,text="Deposit",fg='green',bd=5,font=('Arial',20,'bold'))
    deposit_btn.place(relx=.001,rely=.45)

    withdraw_btn=Button(frm,width=15,command=withdraw,text="Withdraw",fg='red',bd=5,font=('Arial',20,'bold'))
    withdraw_btn.place(relx=.001,rely=.6)

    transfer_btn=Button(frm,width=15,command=transfer,text="Transfer",fg='black',bd=5,font=('Arial',20,'bold'))
    transfer_btn.place(relx=.001,rely=.75)

main_screen()
root.mainloop()