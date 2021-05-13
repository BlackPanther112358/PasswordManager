import getpass
import tkinter as tk
import pyperclip

#NOTE: Currently upon entering an invald input, the user is stuck in an infinite while loop, ideally we should change that so the user can back out at any point.

def input_yesorno():
    L1=['1','y','Y','Yes','yes','YES',]
    L2=['2','n','N','No','no','NO']
    x=str(input('Enter your choice: ')).strip()
    while True:
        if x in L1:
            return(1)
            break
        elif x in L2:
            return(2)
            break
        else:
            print('Invalid Input')
            x=str(input('Enter your choice: ')).strip()

def input_mainmenu():
    L1=['1','L','login','Login','l','LOGIN']
    L2=['2','s','S','signup','Signup','SIGNUP']
    L3=['3','e','E','exit','Exit','EXIT']
    x=str(input('Enter your choice: ')).strip()
    while True:
        if x in L1:
            return(1)
            break
        elif x in L2:
            return(2)
            break
        elif x in L3:
            return(3)
            break
        else:
            print('Invalid Input')
            x=str(input('Enter your choice: ')).strip()

def input_afterloginmenu():
    L1=['1','S','s','show','Show','SHOW']
    L2=['2','A','a','add','Add','ADD']
    L3=['3','D','d','delete','Delete','DELETE']
    L4=['4','U','u','update','Update','UPDATE']
    L5=['5','password','Password','PASSWORD','pass','Pass','PASS']
    L6=['6','email','Email','EMAIL']                                    
    L7=['7','Delete Account','DELETE ACCOUNT','delete account']
    L8=['8']        #Put some more input options here
    L9=['9','Q','quit','Quit','q','QUIT']
    x=str(input('Enter your choice: ')).strip()
    while True:
        if x in L1:
            return(1)
            break
        elif x in L2:
            return(2)
            break
        elif x in L3:
            return(3)
            break
        elif x in L4:
            return(4)
            break
        elif x in L5:
            return(5)
            break
        elif x in L6:
            return(6)
        elif x in L7:
            return(7)
        elif x in L8:
            return(8)
        elif x in L9:
            return(9)
        else:
            print('Invalid Input')
            x=str(input('Enter your choice: ')).strip()

def input_otp():    
    x=str(input('Enter OTP: ')).strip()
    while True:
        if len(x)==4 and x.isdigit():
            return(int(x))
            break
        else:
            print('Invalid OTP entered, Try Again!!')
            x=str(input('Enter OTP: ')).strip()
    
def input_username():
    a="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ """
    x=str(input('Enter username: ')).strip()
    while True:
        if len(x)<=15 and len(x)>0:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                return(str(x))
                break
            else:
                print('Invalid character used')
                x=str(input('Enter valid username: ')).strip()
        else:
            print('Username cannnot be longer than 15 characters')
            x=str(input('Enter valid username: ')).strip() 

def input_alias():
    a="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    x=str(input('Enter website alias: ')).strip()
    while True:
        if len(x)<=30 and len(x)>0:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                return(str(x))
                break
            else:
                print('Invalid character used')
                x=str(input('Enter valid alias: ')).strip()
        else:
            print('Alias cannnot be longer than 30 characters')
            x=str(input('Enter valid alias: ')).strip() 
    
def input_password():
    a="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ """
    x=str(getpass.getpass('Enter password: ')).strip()
    while True:
        if len(x)<=45 and len(x)>=4:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                print('Password entered successfully')
                return(str(x))
                break
            else:
                print('Invalid character used')
                x=str(getpass.getpass('Enter valid password: ')).strip()
        else:
            print('The length of password should be between 4 and 45')
            x=str(getpass.getpass('Enter valid password: ')).strip() 

def input_newpassword():
    a,n="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ """,3
    x=str(getpass.getpass('Enter password: ')).strip()
    while True:
        if len(x)<=45 and len(x)>=4:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                print('Password entered successfully'+'\n')
                if check_weakpassword(x):
                    print('The password entered is not very strong and might be cracked easily Would you like to reset password? \n\t 1. YES \t 2. NO"')
                    p=input_yesorno()   
                    if p==1:
                        print("Please use a combination on letters, numbers and special characters to make a stronger password. Keeping longer passwords id helpful too"+'\n')
                        x=str(getpass.getpass('Enter valid password: ')).strip()
                    else:  
                        break
                else:
                    break
            else:
                print('Invalid character used')
                x=str(getpass.getpass('Enter valid password: ')).strip()
        else:
            print('The length of password should be between 4 and 45')
            x=str(getpass.getpass('Enter valid password: ')).strip()
    while str(getpass.getpass('Please confirm your password: ')).strip()!=x :
        print('The Passwords entered do not match, please try again')
    print('Password confirmed successfully')
    return(x)

def input_email():      
    a="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    x=str(input('Enter your email: ')).strip()
    while True:
        if len(x)<=30 and len(x)>0:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                y,c=x.split('@',1),0
                for i in y:
                    if i!='':
                        c+=1
                    if c==2:
                        break
                if c==2:
                    z,c=x.split('@')[-1].split('.',1),0
                    for i in z:
                        if i!='':
                            c+=1
                        if c==2:
                            break
                    if c==2:
                        return(str(x))
                        break
                    else:
                        print('Email must contain dot(.)')
                        x=str(input('Enter valid email: ')).strip()
                else:
                    print('Email must contain @')
                    x=str(input('Enter valid email: ')).strip()
            else:
                print('Invalid character used')
                x=str(input('Enter valid email: ')).strip()
        else:
            print('Email cannnot be longer than 30 characters')
            x=str(input('Enter valid email: ')).strip()

def input_website():        
    a="""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    x=str(input('Enter website name: ')).strip()
    while True:
        if len(x)<=30 and len(x)>0:
            c=True
            for i in x:
                if i not in a:
                    c=False
                    break
            if c:
                y,c=x.split('.'),0
                for i in y:
                    if i!='':
                        c+=1
                    if c==3:
                        break
                if c==3:
                    return(str(x))
                else:
                    print('Website must contain dot(.)')
                    x=str(input('Enter valid website name: ')).strip()
            else:
                print('Invalid character used')
                x=str(input('Enter valid website name: ')).strip()
        else:
            print('Website cannnot be longer than 30 characters')
            x=str(input('Enter valid website name: ')).strip()
    
def input_passwordlength():
    x=str(input('Enter Password length: ')).strip()
    while True:
        if x.isdigit():
            if int(x)>=4 and int(x)<=45:
                return(int(x))
                break
            else:
                print('The length of password should be between 4 and 45')
                x=str(input('Enter valid password length: ')).strip()
        else:
            print('Password length must be a number')
            x=str(input('Enter  valid password length: ')).strip()

def input_searchmenu():
    L1=['1','all','All','ALL']
    L2=['2']            #Put some more input options here
    L3=['3']
    x=str(input('Enter your choice: ')).strip()
    while True:
        if x in L1:
            return(1)
            break
        elif x in L2:
            return(2)
            break
        elif x in L3:
            return(3)
        else:
            print('Invalid Input')
            x=str(input('Enter your choice: ')).strip()

def check_weakpassword(x):
    r,a=0,''
    if x.lower().islower()==True:
        y,z='',''
        for i in x:
            if i.islower():
                y+=i
            elif i.isupper():
                z+=i
        if len(y)>0:
            r+=1
        if len(z)>2:
            r+=2
        elif len(z)>0:
            r+=1
    y,b='',''
    for i in a:
        if i.isdigit():
            y+=i
        else:
            b+=i
    if len(y)>0:
        r+=1
    if len(b)>2:
        r+=2
    elif len(b)>0:
        r+=1
    if len(x)>15:
        r+=4
    elif len(x)>12:
        r+=3
    elif len(x)>8:
        r+=2
    elif len(x)>6:
        r+=1
    if r>=6:
        return False
    else:
        return True


def input_sno(n):           
    x=str(input("Enter S.No. whose password needs to be shown: ")).strip()
    while True:
        if x.isdigit():
            if int(x)<=n:
                return int(x)
            else:
                print('Enter a valid Serial no.')
                x=str(input("Enter S.No.: ")).strip()
        else:
            print('Please Enter a number')
            x=str(input("Enter S.No.: ")).strip()


def show_password(x):
    w=tk.Tk()
    w.title("Displaying Password")
    w.geometry('300x100')
    lbl=tk.Label(w,text=x)
    lbl.place(relx = 0.5,rely = 0.5,anchor = 'center')
    def countdown(count):        
        label['text'] = str(count)+' seconds left'
        if count > 0:
            w.after(1000, countdown, count-1)   
        else:
            w.destroy()
    label = tk.Label(w)
    label.place(relx = 1.0,rely = 0.0,anchor ='ne')
    def close():
        w.destroy()
    b1=tk.Button(w,text='Close Window',command=close)
    b1.place(relx=0.8, rely=0.9, anchor='se')
    def copy():
        pyperclip.copy(x)
    b2=tk.Button(w,text='Copy to Clipboard',command=copy)
    b2.place(relx=0.1, rely=0.9, anchor='sw')   
    countdown(30)
    w.mainloop()

