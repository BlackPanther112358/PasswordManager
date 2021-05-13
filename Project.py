#ALL THE CONCERNED MODULES SHALL BE IMPORTED HERE ONLY 
import os
import random
import string
import mysql.connector
import smtplib
import math
import socket
from algo import generate_key, encrypt, decrypt
from pyperclip import copy
import time
from input_filters import *
from export import *

#LINKING PYTHON AND MYSQL:
mydb=mysql.connector.connect(host="localhost",user="root",password="123456")    #Remember to change password

#CREATING DATABASE AND TABLE:
mycursor=mydb.cursor()
mycursor.execute("use PasswordManager") 
mycursor.execute("create table if not exists Login(Username varchar(100) not null unique, Password varchar(100) not null, Password_Key char(6) primary key,email varchar(100) not null )")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#CREATING BASIC FUNCTIONS USED IN THE FILE
def randomPassword(n):              # this password generator is capable of randomly and securely generating any length(>=4) password, since 4 chars already fixed
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)

    for i in range(n):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions to generate and send OTP
def generateOTP(): 
    # Declare a digits variable to store the digits
    digits = "0123456789"
    OTP = "" 
    # length of otp can be changed by varying the value in range
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
    return OTP    


def sendOTP():
    x=generateOTP()
    str1="select email from login where Username=%r"%encrypt(username,'lwosch')
    mycursor.execute(str1)
    y=mycursor.fetchone()
    print("OTP sent to mail ",decrypt(y[0],'lwosch'))
    server=smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("csprojectotpgenerator@gmail.com","ssllxekmtvfvtshb")
    message="""Greetings!
We have received a request for password reset for your password manager account.
The OTP required for verification is: {}.
This OTP is valid only for the next 10 mins.
It is advised not to disclose this to anyone.
If no such request is raised, kindly ignore the message.""".format(x)
    server.sendmail("csprojectotpgenerator@gmail.com",decrypt(y[0],'lwosch'),message)
    server.quit()
    c,n=0,3
    start_time=time.time()
    while n>0 and c==0:                 #3 attempts at entering right OTP
        if time.time()-start_time<=600:
            OTP_received=input_otp()    
            if x==str(OTP_received):
                print("Authorization complete. Proceeding to password reset..."+'\n')
                pswd=input_newpassword()   
                query="update login set password=%r where username=%r"%(encrypt(pswd,'lwosch'),encrypt(username,'lwosch'))
                mycursor.execute(query)
                mydb.commit()
                print("Password successfully changed, You can now login with your new password.")
                menu()
            else:
                print("Incorrect OTP!!! Try Again"+'\n')
                n-=1
        else:
            print("Timeout!!! OTP Expired"+'\n')
            break
    print("OTP VERIFICATION FAILED. Would you like to resend OTP? \n\t 1. YES \t 2. NO")
    p=input_yesorno()   
    if p==1:
        sendOTP()
    else:
        print("Attempt to login failed."+'\n')
        menu()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions to check for duplicates
def username_duplicate(x):
    x=encrypt(x,"lwosch")
    cur=mydb.cursor()
    query="Select username from login"
    mycursor.execute(query)
    data=cur.fetchall()
    a=set()
    for row in data:
        a.update(row)
    n=len(a)
    a.add(x)
    m=len(a)
    if m==n:
        return False
    else:
        return True

def key_duplicate(x):
    cur=mydb.cursor()
    query="Select Password_key from login"
    mycursor.execute(query)
    data=cur.fetchall()
    a=set()
    for row in data:
        a.update(row)
    n=len(a)
    a.add(x)
    m=len(a)
    if m==n:
        return False
    else:
        return True

def password_duplicate(uname,website):
    uname,website=encrypt(uname,key),encrypt(website,key)
    cur=mydb.cursor()
    query="select username, website, website_alias from {}".format(key)
    mycursor.execute(query)
    data=cur.fetchall()
    a=set() 
    for row in data:
        a.add((row[0],row[1]))
    n=len(a)
    a.add((uname,website))
    m=len(a)
    if m==n:
        return False
    else:
        return True
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#CREATING FUNCTIONS TO BE USED IN THE Main Menu
    
def signup():                       #this function adds the login details to the master 'login' table and creates a table for the user using the key 
    print('\n'+"""Create an account for a secure way to store your passwords all at one place never again needing to remember them.
          This is the safest way to store passwords and accessing them at one go"""+'\n')
    global username
    username=input_username() 
    while not username_duplicate(username): 
        print("Username already used, try again!!")
        username=input_username()
    pswd=input_newpassword()
    key=generate_key()
    while not key_duplicate(key):
        key=generate_key()          #FUN FACT: If all possible keys which our function can generate have been used, then this will lead to an infinite loop...OOPSSS...
    key_main='lwosch'               #Use this key to encrypt anything out of the user table, lwosch is our initials encrypted using affine cipher.
    global email
    email = input_email()
    mycursor.execute("insert into login values('"+encrypt(username,key_main)+"','"+encrypt(pswd,key_main)+"','"+key+"','"+encrypt(email,key_main)+"')")
    mydb.commit()
    query="create table if not exists {} (Website varchar(100) not null, Website_Alias varchar(100), Username varchar(100) not null,Password varchar(150) not null)". format(key)
    cur=mydb.cursor()
    cur.execute(query)
    cur.close
    print("User created successfully\n")
    menu()                          #now prompt the user to login


def login():
    print('\n'+"Welcome back!!")
    global username
    username=input_username()
    mycursor.execute("select username from login where username='"+encrypt(username,'lwosch')+"'")
    pot=mycursor.fetchone()
    if pot is not None:
        query="select Password_key from login where username=%r"%encrypt(username,'lwosch')
        mycursor.execute(query)
        global key
        key=mycursor.fetchone()[0]
        
        print("VALID USERNAME!!!"+'\n')
        sum1=0
        while sum1<3:
            pswd=input_password()    
            mycursor.execute("select password from login where password='"+encrypt(pswd,'lwosch')+"' and Username='"+encrypt(username,'lwosch')+"'")
            a=mycursor.fetchone()    
            if a is not None:
                    print('\n'+'~'*48+'\n'+'~'*16+"LOGIN SUCCESSFUL"+'~'*15+'\n'+'~'*48)
                    afterloginmenu()

            else:
                print('\n'+"Incorrect password, login failed!!"+'\n'+"Try Again"+'\n')
                sum1+=1   
        print("Three attempts to login failed. Generating OTP...")
        sendOTP()
    else:
        print("User does not exist\n")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CREATING FUNCTIONS TO BE USED IN THE After Login Menu

def show_pswd():          
    cur=mydb.cursor()
    site,uname=search_procedure(key)
    if site is not None and uname is not None:
        query="select password from {} where Username='{}' and Website='{}'".format(key,encrypt(uname,key),encrypt(site,key))   
        cur.execute(query)
        data=cur.fetchone()
    else:
        afterloginmenu()
    if data is not None:
        print('\nThe requested password will be displayed in a new window and will only remain visible for 30 seconds for security reasons.')
        ciphertext=data[0]
        x=decrypt(ciphertext,key)
        show_password(x)
    else:
        print("Data not Found")
    print('\n'+'~'*98)
    afterloginmenu()


def add_pswd():
    cur=mydb.cursor()
    site=input_website()              
    uname=input_username()          
    print("Would you like a keep an alias name for the website? \n\t 1. YES \t 2. NO")
    n=input_yesorno()
    alias=""
    if n==1:
        alias=input_alias()  
    else:
        print("Website alias denied by user")
    while not password_duplicate(uname,site):
        print("Password already stored! Use show option to view saved password.")
        site=input_website()              
        uname=input_username()
        if n==1:
            alias=input_alias()
    print("Would you like a suggested password? \n\t 1. YES \t 2. NO")
    n=input_yesorno()
    pswd=""
    if n==1:
        x=input_passwordlength()    
        pswd=randomPassword(x-4)
        print("Random Password Generated Successfully: ",pswd )              #here x-4 is used because in the code a password of length 4 is already fixed
    elif n==2:
        print("Random password generation denied by user")
        pswd=input_newpassword()
    query="insert into {} values('{}','{}','{}','{}')". format(key, encrypt(site,key), encrypt(alias,key), encrypt(uname,key), encrypt(pswd,key))
    cur.execute(query)
    mydb.commit()
    print('\n'+'~'*98)
    afterloginmenu()
       


def delete_pswd():       
    cur=mydb.cursor()
    site,uname=search_procedure(key)
    query="select password from {} where Username='{}' and Website='{}'".format(key,encrypt(uname,key),encrypt(site,key))   
    cur.execute(query)
    data=cur.fetchone()
    if data is not None:
        print("Do you really want to delete the password? \n\t 1. YES \t 2. NO")
        n=input_yesorno()
        if n==1:
            query = "delete from {} where (Website='{}' or Website_Alias='{}') and username='{}'". format(key,encrypt(site,key),encrypt(site,key),encrypt(uname,key))
            cur.execute(query)
            mydb.commit()
            print("Password successfully deleted") 
        elif n==2:
            print("Password deletion denied by user")
    else:
        print("Data not found")
    cur.close()
    print('\n'+'~'*98)
    afterloginmenu()


def update_pswd():
    cur=mydb.cursor()
    site,uname=search_procedure(key)
    query="select password from {} where Username='{}' and Website='{}'".format(key,encrypt(uname,key),encrypt(site,key))   
    cur.execute(query)
    data=cur.fetchone()
    if data is not None:
        print("Would you like a suggested password? \n\t 1. YES \t 2. NO")  
        n=input_yesorno()
        if n==1:
            x=input_passwordlength()
            pswd=randomPassword(x-4)
            print("Random Password Generated Successfully: ",pswd )             #here x-4 is used because in the code a password of length 4 is already fixed
        elif n==2:
            print("Random password generation denied by user")
            print("Enter new password below")
            pswd=input_newpassword()
        query = "update {} set password='{}' where Username='{}' and (Website='{}' or Website_Alias='{}')". format(key,encrypt(pswd,key),encrypt(uname,key),encrypt(site,key),encrypt(site,key))
        cur.execute(query)
        mydb.commit()
        print("Password successfully updated")
        print("Would you like to copy password to clipboard? \n\t 1. YES \t 2. NO")
        y=input_yesorno()
        if y==1:
            print("Copying to clipboard...")
            copy(pswd)
            print("Password successfully copied to clipboard")
        else:
            print("Copy to clipboard denied by user")
    else:
        print("Data not found")
    print('\n'+'~'*98)
    afterloginmenu()


def del_account():
    print("This change is permanent and cannot be reverted")
    print("Are you sure you would like to proceed and delete your account? \n\t 1. YES \t 2. NO")
    i=input_yesorno()
    if i==1:
        cur=mydb.cursor()
        uname=input_username()
        print("Please re-enter your password to confirm the action")
        pswd=input_password()       #Password being taken as input, Master table
        mycursor.execute("select password from login where password='"+encrypt(pswd,'lwosch')+"' and Username='"+encrypt(uname,'lwosch')+"'")
        a=mycursor.fetchone()    
        if a is not None:
            print("Authorization complete. Deletion in process...")
            query1="Drop table {}".format(key)
            cur.execute(query1)
            query2= "delete from login where username='"+encrypt(uname,'lwosch')+"'"
            cur.execute(query2)
            mydb.commit()
            cur.close()
            print("Account deleted successfully\n")
            menu()
        else:
            print("Data not found")
            print('\n'+'~'*98)
            afterloginmenu()
    elif i==2:
        print("Account deletion cancelled by user. No changes were made.")
        print('\n'+'~'*98)
        afterloginmenu()

        
def account_passchange():
    print("Please enter your current password to authorize the action.")
    pswd_initial=input_password()       #Password being taken as input, Master table
    mycursor.execute("select password from login where password='"+encrypt(pswd_initial,'lwosch')+"' and Username='"+encrypt(username,'lwosch')+"'")
    a=mycursor.fetchone()    
    if a is not None:
        print("Authorization complete. Initializing password change...")
        pswd_new=input_newpassword()
        query="update login set password=%r where username=%r"%(encrypt(pswd_new,'lwosch'),encrypt(username,'lwosch'))
        mycursor.execute(query)
        mydb.commit()
        print("Password successfully changed, You can now login with your new password.")
        print('\n'+'~'*98)
        afterloginmenu()
    else:
        print("Authorization failed!!")
        print('\n'+'~'*98)
        afterloginmenu()


def account_emailchange():
    print("Please enter your current password to authorize the action.")
    pswd=input_password()       #Password being taken as input, Master table
    mycursor.execute("select password from login where password='"+encrypt(pswd,'lwosch')+"' and Username='"+encrypt(username,'lwosch')+"'")
    a=mycursor.fetchone()    
    if a is not None:
        print("Authorization complete. Initializing E-mail change...")
        email=input_email()
        query="update login set email=%r where username=%r"%(encrypt(email,'lwosch'),encrypt(username,'lwosch'))
        mycursor.execute(query)
        mydb.commit()
        print("E-mail successfully changed.")
        print('\n'+'~'*98)
        afterloginmenu()
    else:
        print("Authorization failed!!")
        print('\n'+'~'*98)
        afterloginmenu()
   

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DRIVER FUNCTIONS

def afterloginmenu():#this is the second menu after login
    while True:
        print()
        print("\t1. Show Passwords")
        print("\t2. Add Passwords")
        print("\t3. Delete Passwords")
        print("\t4. Update Passwords")
        print("\t5. Change Account Password")
        print("\t6. Change Account E-mail")
        print("\t7. Delete Account")
        print("\t8. Export to Mail")
        print("\t9. Exit")
        print()
        i=input_afterloginmenu()
        print()
        if i==1:
            show_pswd()
        if i==2:
            add_pswd()
        if i==3:
            delete_pswd()
        if i==4:
            update_pswd()
        if i==5:
            account_passchange()
        if i==6:
            account_emailchange()
        if i==7:
            del_account()
        if i==8:
            #import socket
            try:
                host = socket.gethostbyname("one.one.one.one")
                s=socket.create_connection((host, 80), 2)
                s.close()
                print("Processing your request...")
                export_to_mail(username,key)
            except:
                print("Internet not connected, Please check your internet connection")

        if i==9:
            os.system('cls')
            print()
            print('-'*98+'\n'+'*'*10+'='*18+'*'*8+"WELCOME TO PASSWORD MANAGER"+'*'*8+'='*18+'*'*9+'\n'+'-'*98)
            menu()
        


#this is the whole menu that is looping again and again making the whole program run
def menu():
    while True:
        print("\t1. Login")
        print("\t2. SignUp")
        print("\t3. Exit")
        print()
        i=input_mainmenu()
        if i==1:
            login()
        if i==2:
            signup()
        if i==3:
            mydb.close()
            quit()


#----------------------------------------------------------------------------------------------------------
os.system('cls')
print()
print('-'*98+'\n'+'*'*10+'='*18+'*'*8+"WELCOME TO PASSWORD MANAGER"+'*'*8+'='*18+'*'*9+'\n'+'-'*98)
menu()   
