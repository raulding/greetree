#! /usr/bin/env python
#coding=utf-8  
 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
 
from email.utils import COMMASPACE,formatdate
from email import encoders
 
import os
import sys

text = ""

def send_mail(date, dev, text, texts=[], files=[], images=[]): 
    global password
    server={}
    server['name'] = 'mail.xxx.com'
    server['user'] = 'xxx'
    server['passwd'] = 'xxxxx'
    to = ['xxxx@xxx.com']
    fro = "xxx@xxx.com" 
    
    msg3 = MIMEMultipart() 
    msg3['From'] = fro 
    msg3['Subject'] = "test %s on %s"%(dev, date) 
    msg3['To'] = COMMASPACE.join(to) #COMMASPACE==', ' 
    msg3['Date'] = formatdate(localtime=True) 
    #msg3.attach(MIMEText(text, 'html', 'utf-8'))  

    for a_text in texts:
        text += str(a_text)
			 
    i = 0;
    for image in images:
        text += '<br><img src="cid:image%d">'%i
        
        part = MIMEImage(open(image, 'rb').read())
        part.add_header('Content-ID', '<image%d>'%i)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(image))

        msg3.attach(part)
        i += 1
   
    for file in files:
       	text += open(file, 'rb').read()
	text += '<br/>'
       	
	#part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
    #part.set_payload(open(file, 'rb').read())
    #encoders.encode_base64(part)
    #part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    #msg3.attach(part)
 
    msg3.attach(MIMEText(text, 'html', 'utf-8'))  
    
    import smtplib 
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd']) 
    msg_content = msg3.as_string()
    smtp.sendmail(fro, to, msg_content) #msg.as_string()
    smtp.close()

def main(argv=[]):
    print ("Send mail start")
    #file = open(input_file, "rb")
    #content = file1.read()
    date = argv[1]
    dev = argv[2]

    send_mail(date, dev, text, [], [], argv[3:])
    print ("Send Over")

if __name__ == '__main__':
    main(sys.argv)
