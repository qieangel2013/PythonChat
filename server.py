#!/usr/bin/env python
#coding:gbk
import socket,threading,time,sys,os,re,wx
class Zqfframe(wx.Frame):
    def __init__(self,parent,id,title):
         wx.Frame.__init__(self,parent,id,title,size=(500,500))
         self.panel=wx.Panel(self,-1)
         self.richText = wx.TextCtrl(self.panel, -1,"",  size=(488, 460), style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_READONLY|wx.TE_LINEWRAP)   
         font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)  
         self.richText.SetFont(font) 
         self.icon = wx.Icon('ico/ss16.ico', wx.BITMAP_TYPE_ICO)
         self.SetIcon(self.icon)
         self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
    def OnCloseWindow(self,event):
        self.Destroy()
        sys.exit(1)
class Zqfapp(wx.App):
    def OnInit(self):
        self.frame=Zqfframe(parent=None,id=-1,title="张秋方—server")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
strss=""
def runs(obj):
    global strss
    def clientcl(clientsock,addrr):
        global strss
        c_ip,c_port=addrr
        strss=strss +"连接ip来自于：" + str(c_ip) + ",端口号为：" + str(c_port)+ "\n"
        obj.SetLabelText(strss)
        while 1:
                data=clientsock.recv(4096)
                m1=re.match(r"(.*?)\#tc$",data)
                if m1:
                    j=userobj.index(clientsock)
                    dfgs=users[j]+"已经退出聊天室"
                    strss= strss +"系统提示：" + dfgs+ "\n"
                    obj.SetLabelText(strss)
                    users.pop(j)
                    userobj.pop(j)
                    for s in userobj:
                        s.send(bytes("系统提示#" + dfgs))
                else:
                    try:
                        if clientsock in userobj:
                            strss=strss+users[userobj.index(clientsock)]+"说："
                        strss= strss + data+ "\n"
                        obj.SetLabelText(strss)
                        m=re.match(r"(.*?)\-client$",data)
                        if m:
                            clientsock.send(bytes("欢迎您,%s" % m.group(1)))
                            if m.group(1) in users:
                                kxcv="_" + m.group(1)
                            else:
                                kxcv=m.group(1) 
                            asdfg="欢迎%s加入聊天室" % kxcv
                            for s in userobj:
                                s.send(bytes("系统提示#" + asdfg))
                            users.append(kxcv)
                            userobj.append(clientsock)
                            userlist=":".join(users)
                            if len(users)==1:
                                userlist=":" +userlist
                            for s in userobj:
                                s.send(bytes(userlist))
                        else:
                            try:
                                i=userobj.index(clientsock)
                                userlists=":".join(users)
                                if len(users)==1:
                                    userlists=":" +userlists
                                for s in userobj:
                                    s.send(bytes(users[i]+"#")+ data)
                                    s.send(bytes(userlists))
                            except:
                                strss= strss +"向聊天室转发信息出错"+ "\n"
                                obj.SetLabelText(strss)
                    except:
                            strss= strss +"处理数据出错"+ "\n"
                            obj.SetLabelText(strss)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    localip = socket.gethostbyname(socket.gethostname())
    addr=(localip,1111)
    s.bind(addr)
    s.listen(1)
    clients=[]
    users=[]
    userobj=[]
    strss="服务开始启动...\n"
    obj.SetLabelText(strss)
    while 1:
            client,addrs=s.accept()
            try:
                    clients.append(client)
                    t=threading.Thread(target=clientcl,args=(client,addrs))
                    t.start()
        #except keybordinterrupt:
                #raise
            except:
                break

if __name__=="__main__":
    app=Zqfapp()
    st=threading.Thread(target=runs,args=[app.frame.richText])
    st.start()
    app.MainLoop()
    