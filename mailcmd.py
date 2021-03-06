#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time 
import imaplib,smtplib, email
from email.message import EmailMessage

class mailcmd:
    """
    A class for send command from my email.
    
    """
    def __init__(self,imap_server,imap_port,
            smtp_server,smtp_port,account,password):
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.account = account
        self.password = password
        self.flag = ''
        self.to_addr=["yf@ziwu.net","zspace@139.com","info+robot@yufu.org"]

    def getcmd(self,flag="UNSEEN"):
        """
        Get command from mail
        """

        self.flag = flag
        sublist =[]
        try:
            with imaplib.IMAP4_SSL(self.imap_server,self.imap_port) as M:
                M.login(self.account,self.password)
    
                i=0
                M.select()
                # result, message = M.select()
                res, data = M.search(None, self.flag)
                for num in data[0].decode().split():
                    res, data = M.fetch(num, 'RFC822')
                    try:
                        msg=data[0][1].decode()
                    except:
                        msg=data[0][1].decode('gbk','ignore')
                    msg = email.message_from_string(msg)
                    i+=1
                    sub=email.header.decode_header(msg['subject'])
                    if sub[0][1]!=None:
                        str=sub[0][0].decode(sub[0][1])
                    else:
                        str=sub[0][0]
                    sublist.append(str)

                ts=mailcmd.time_bj()
                print( "%s get %d command from mail." %(ts, i))
                #for i in range(len(sublist)):
            #    print(i+1,sublist[i])
        except Exception as e:
            print( 'imap error: %s' % e)

        return sublist
    

    def sendtext(self,txt):
        """
        Send message back
        """
        ts=mailcmd.time_bj()
        msg=EmailMessage()
        msg.set_content(txt)
        msg['Subject']="Robot message "+ts
        msg['From']=self.account
        msg['To']=",".join(self.to_addr)
 
        M = smtplib.SMTP_SSL(self.smtp_server,self.smtp_port)
        try:
            M.login(self.account,self.password)
            M.send_message(msg)
            print( "%s send mail ok!" %(ts))
        except Exception as e:
            print( 'send mail error: %s' % e)

        M.quit()
    

    def sendhtml(self,txt):
        """
        Send message back
        """
        ts=mailcmd.time_bj()
        msg=EmailMessage()
        msg.set_content(txt)
        msg['Subject']="Robot message "+ts
        msg['From']=self.account
        msg['To']=",".join(self.to_addr)
        
        html_tpl = ('<html><head><style type="text/css">'
                'table.gridtable{{color:#333333;border-width:1px;border-style:solid;width:100%;'
            'border-color:#666666;border-collapse:collapse;margin:0 auto}}'
            'table.gridtable th{{color:#0000a0;font-size:14px;padding: 10px;background-color:#dedede;}}'
            'table.gridtable td{{font-size:16px;text-align:left;padding:14px;background-color:#ffffff;}}'
            '</style></head><body><center><div align="center";style="text-align:center;width:400px"><br><br>'
            '<table class="gridtable"><tr><th>{msg_head}</th></tr><tr><td>'
            '{msg_body}</td></tr></table><br>'
            '<div style="color:#00a0a0;font-family:arial;font-size:11px">PyRobot service powered by<br>'
            '<a style="text-decoration:none" href="http://www.yufu.org">yufu.org</a>&copy;2017'
            '</div></div></center></body></html>')

        txt=txt.replace('\n','<br>')
        html_msg=html_tpl.format(msg_head='PyRobot Message', msg_body=txt)
        msg.add_alternative(html_msg ,subtype="html")
 
        M = smtplib.SMTP_SSL(self.smtp_server,self.smtp_port)
        try:
            M.login(self.account,self.password)
            M.send_message(msg)
            print( "%s send mail ok!" %(ts))
        except Exception as e:
            print( 'send mail error: %s' % e)
            
        M.quit()
    

    def time_bj():
        ts=time.strftime("%Y-%m-%d %H:%M:%S",
                time.gmtime(time.time()+28800))
        return ts
        
if __name__ == "__main__":

#    m = mailcmd('imap.gmail.com','993',
#            'smtp.gmail.com','465',
#            'robot@yufu.org','qdlzxkgk')

    m = mailcmd('imap.exmail.qq.com','993',
            'smtp.exmail.qq.com','465',
            'robot@ziwu.net','qdlzxkgk8G')

    #cmd=m.getcmd()
    cmd=m.getcmd('ALL')
    if cmd:
        msg="Hello,你好\nI've got some command:\n\n"
        msg+='<ul><li>'+'</li><li>'.join(cmd)+'</li></ul>'
        msg+='\n\n PyRobot 正在全力运行...\n'
        print(msg)
        #m.sendtext(msg)
        #m.sendhtml(msg)
    print( "Done!" )
