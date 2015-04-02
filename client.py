#!/usr/bin/env python
#coding:gbk
import socket,time,os,sys,threading,random,re,wx
class chatdlg(wx.Dialog): 
    def cht(self):
        self.sendButton = wx.Button(self, -1, "发送", pos=(490, 430)) 
        self.sendButton.Enable(False)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)  
        self.DisplayText = wx.TextCtrl(self, -1, '', size=(450, 350), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_LINEWRAP)
        self.friend = wx.ListCtrl(self, wx.NewId(),size=(133, 322),style=wx.LC_REPORT|wx.LC_HRULES | wx.LC_VRULES,pos=(460,0))
        self.friend.InsertColumn(0, "活跃用户名",width=115)
        self.friend.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.OnDclick)
        self.usercount=wx.StaticText(self, -1, "当前在线用户：10", size=(150, 20),pos=(465,333))
        self.prinmess = wx.TextCtrl(self, -1, "小方，您好？", pos=(5, 360), size=(580, 60))
        self.DisplayText.SetFont(font) 
        self.prinmess.SetFont(font)
        self.namestr=""
        self.Bind(wx.EVT_BUTTON, self.bnsnd, self.sendButton)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(("localhost",1111))
        zqfdia = wx.TextEntryDialog(None,"请输入你要登陆的用户名？","小方聊天室", "", style=wx.OK|wx.CANCEL,pos=(self.screenmm[0]/3,self.screenmm[1]/4))
        if zqfdia.ShowModal() == wx.ID_OK:
            if not len(zqfdia.GetValue().encode("gbk")):
                strrss="z张%s-client" % random.sample(range(100000),1)
            else:
                strrss=zqfdia.GetValue().encode("gbk")+"-client"
                zqfdia.Destroy()
        else:
            strrss="z张%s-client" % random.sample(range(100000),1)
        self.DisplayText.AppendText("请等待5秒钟\n")
        tdf=threading.Thread(target=self.sjcl,args=[self])
        tdf.start()
        self.client.send(bytes(strrss))
    def sjcl(self,obj):
         while 1:
             data=obj.client.recv(4096)
             mstr=re.match(r"(.*?)\#(.*?)",data)
             obj.sendButton.Enable(True)
             muser=re.match(r"(.*?)\:(.*?)",data)
             if not len(data):break
             else:
                 if muser:
                     data_user=data.split(":")
                     obj.friend.ClearAll()
                     obj.friend.InsertColumn(0, "活跃用户名",width=115)
                     for f in data_user:
                         if len(f):
                             obj.friend.InsertStringItem(sys.maxint,f)
                     obj.usercount.SetLabelText("当前在线用户：%s"  % obj.friend.GetItemCount())
                 elif mstr:
                     data_result=data.split("#")
                     obj.namestr=data_result[0]
                     data=data_result[0] + "说：" +data_result[1]+"\n"
                     obj.DisplayText.AppendText(data)
                 else:
                     data=data + "\n" 
                     obj.DisplayText.AppendText(data)
    def __init__(self):  
        self.screenmm=wx.DisplaySize()
        wx.Dialog.__init__(self, None, -1,"小方聊天室" ,size=(600, 500),style=wx.DEFAULT_DIALOG_STYLE ^ (wx.MINIMIZE_BOX),pos=(self.screenmm[0]/3,self.screenmm[1]/4))
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.icon = wx.Icon('ico/ss16.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)  
        t=threading.Thread(target=self.cht(),name="zqf6")
        t.start()
    def OnClose(self,evt):
        self.client.send(self.namestr +"#tc")
        evt.Skip()
    def OnDclick(self,event):
        #nr=event.GetItem()
        #wx.MessageBox(nr.GetText(),"小方聊天室",wx.YES_NO)
        wx.MessageBox("私聊窗口正在开发中，请等待...","小方聊天室",wx.YES_NO)
    def bnsnd(self,event):  
        data = self.prinmess.GetValue().encode("gbk")
        try:
            #data=str(data)
            data=data.replace("#"," ")
            data=data.replace(":"," ")
        except:
            self.DisplayText.AppendText("系统提示说：字符串处理出现错误，请重新打开\n") 
        #data1=data + "\n"
        #self.DisplayText.AppendText(data1) 
        data=bytes(data)
        if not len(data):self.DisplayText.AppendText("系统提示说：发布内容不能为空\n")
        else:
            self.client.send(data)
            self.prinmess.SetLabelText("")
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    app.MainLoop()   
    dialog = chatdlg()
    result = dialog.ShowModal()  
    if result == wx.ID_OK:  
        print "OK"  
    else:  
        print "Cancel"  
    dialog.Destroy() 