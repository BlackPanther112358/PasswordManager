import pdb          #remember to remove at last
import os
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from algo import encrypt, decrypt
import mysql.connector
import smtplib
from input_filters import input_alias, input_searchmenu, input_sno

#LINKING PYTHON AND MYSQL:
mydb=mysql.connector.connect(host="localhost",user="root",password="012345")    #Remember to change password

#CREATING DATABASE AND TABLE:
mycursor=mydb.cursor()
mycursor.execute("use PasswordManager")


def export_to_mail(usernamearea,keyarea):
    f=open("exporttomail.txt","w")
    str2="select * from {}".format(keyarea)
    mycursor.execute(str2)
    data=mycursor.fetchall()
    L=["Website                 ","Alias           ","User            ","Password       "]
    f.writelines(L)
    f.write("\n")
    for row in data:
        for attr in row:
            f.write(decrypt(attr,keyarea)+"\t"+"\t")
        f.write("\n")
    f.close()    
    str1="select email from login where Username=%r"%encrypt(usernamearea,'lwosch')
    mycursor.execute(str1)
    y=mycursor.fetchone()
    fromaddr = "csprojectotpgenerator@gmail.com"
    toaddr = decrypt(y[0],'lwosch') 
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = fromaddr 
    # storing the receivers email address  
    msg['To'] = toaddr 
    # storing the subject  
    msg['Subject'] = "Password Email Sync"
    # string to store the body of the mail 
    body = "Your passwords were securely and successfully synced with your mail"
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    # open the file to be sent  
    filename = "Website Password Table"
    attachment = open("exporttomail.txt", "r") 
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    # encode into base64 
    encoders.encode_base64(p)    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls()
    # Authentication 
    s.login("csprojectotpgenerator@gmail.com", "ssllxekmtvfvtshb") 
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    # terminating the session 
    s.quit()
    attachment.close()
    os.remove("exporttomail.txt")
    cur.close()    



def search_procedure(key):
    print("Please choose an method to search:\n\t1. Show all websites\n\t2. Search a website\n\t3. Exit")
    n=input_searchmenu()
    cur=mydb.cursor()
    if n==1:
        cur.execute("select website,website_alias,username from {}".format(key))
        data=cur.fetchall()
        ctr=0
        print('_'*98)
        print(f"|| S.No | {'Website':34} | {'Alias':30} | {'Username':15} ||")
        print('-'*98)
        for i in data:
            ctr+=1
            site=decrypt(i[0],key)
            alias=decrypt(i[1],key)
            uname=decrypt(i[2],key)
            print(f"||  {ctr:02}  | {site:34} | {alias:30} | {uname:15} ||")
        print('_'*98+'\n')
        sno=input_sno(ctr)         
        site=decrypt(data[sno-1][0],key)
        uname=decrypt(data[sno-1][2],key)
        return (site,uname)

    elif n==2:
        print("Enter website or alias to be searched")
        search_string=input_alias()
        cur.execute("select website,website_alias,username from {}".format(key))
        data=cur.fetchall() 
        cur.close()

        L=[]
        for i in data:                                          #decrypting
            site=decrypt(i[0],key)
            alias=decrypt(i[1],key)
            uname=decrypt(i[2],key)
            L+=[(site,alias,uname),]
                                                
        M=[]
        for i in range(len(L)):                              
            L[i]+=((len(((L[i][0]+L[i][1]).lower()).split(search_string.lower()))-1)*len(search_string),)
                                                
        L.sort(key=lambda x:x[-1], reverse=True)
        for i in range(len(L)):
            if L[i][-1]>0:                                      
                M+=[tuple(x for x in L[i] if type(x)==str)]
        if len(M)>10:                           
            M=M[:10]
        for i in range(len(M)):                                 
            M[i]=(i+1,)+M[i]
        ctr=0
        print('_'*98)
        print(f"|| S.No | {'Website':34} | {'Alias':30} | {'Username':15} ||")
        print('-'*98)
        for i in M:     #Write code so that if M is empty, then an error message is diplayed and user is asked to search again.
            ctr+=1
            site=i[1]
            alias=i[2]
            uname=i[3]
            print(f"||  {ctr:02}  | {site:34} | {alias:30} | {uname:15} ||")
        print('_'*98+'\n')
        sno=input_sno(ctr)     
        site=M[sno-1][1]
        uname=M[sno-1][3]
        return (site,uname)

    elif n==3:
        print('This functionality will be available soon.... ;)')       #Tejas was recieving some errors while trying to do this, pls look into the matter
        search_procedure(key)

            

