import gmail
email_id="yograjmalik@gmail.com"
app_pass="stum vqhv zsbc gymx"

def send_openacn_ack(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    sub="Congrates😊,Account opened successfully"
    
    utext=f"""Hello,{uname}
Welcome to PNB Bank
Your Acc No is {uacn}
Your Pass is {upass}
Kindly change your password when you login first

Thanks
PNB Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp(uemail,otp,amt):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for fund transfer"
    
    utext=f"""Your otp is {otp} to transfer amount {amt}

Kindly use this otp to complete transfer
Please don't share to anyone else

Thanks
PNB Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp_4_pass(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for password recovery"
    
    utext=f"""Your otp is {otp} to recover password
Please don't share to anyone else

Thanks
PNB Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)