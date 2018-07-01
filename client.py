import wx
import telnetlib
from time import sleep
import _thread as thread
from dhdjcrypt import dhdjhash

class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label="服务器地址", pos=(10, 50), size=(120, 25))
        self.userNameLabel = wx.StaticText(self, label="用户名", pos=(40, 100), size=(120, 25))
        self.serverAddress = wx.TextCtrl(self, pos=(120, 47), size=(150, 25))
        self.userName = wx.TextCtrl(self, pos=(120, 97), size=(150, 25))
        self.loginButton = wx.Button(self, label='登录', pos=(80, 145), size=(130, 30))
        # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.Show()

    def login(self, event):
        # 登录处理
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (250, 150))
                return
            name = self.userName.GetLineText(0)
            passwd = dhdjhash(name)
            con.write(('login ' + str(name) + ' ' + str(passwd) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            elif response == b'Bad UserName':
                self.showDialog('Error', 'Bad UserName!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='BoxMoe Chat Client', size=(510, 410))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (200, 100))

    def showDialog(self, title, content, size):
        # 显示错误信息对话框
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()

class ChatFrame(wx.Frame):
    """
    聊天窗口
    """

    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(485, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        #self.message = wx.TextCtrl(self, pos=(5, 320), size=(300, 25))
        self.message = wx.TextCtrl(self,-1,"", pos=(5, 320), size=(300,50), style=wx.TE_MULTILINE)
        self.chatFrame.SetInsertionPoint(0)
        self.sendButton = wx.Button(self, label="发送", pos=(304, 320), size=(58, 50))
        self.usersButton = wx.Button(self, label="在线成员", pos=(367, 320), size=(58, 50))
        self.closeButton = wx.Button(self, label="断开连接", pos=(430, 320), size=(58, 50))
        # 发送按钮绑定发送消息方法
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # Users按钮绑定获取在线用户数量方法
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # 关闭按钮绑定关闭方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        # 发送消息
        contents = ''
        x = 0
        while True:
            line = self.message.GetLineText(x)
            contents = contents + line
            x = x + 1
            if line == '':
                break;
        message = str(contents).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')
        response = con.read_some()
        self.disDialog('线上用户', response, (200, 500))
        # con.write(b'look\n')

    def close(self, event):
        # 关闭窗口
        con.write(b'logout\n')
        con.close()
        self.Close()

    def receive(self):
        # 接受服务器的消息
        while True:
            sleep(0.6)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

    def disDialog(self, title, content, size):
        # 显示在线用户信息对话框
        dialog = wx.Dialog(self, title=title, size=size, style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION)
        dialog.Center()
        wx.StaticText(dialog, label=content).Center()
        dialog.ShowModal()

if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title="登录到BMSCS", size=(325, 250))
    app.MainLoop()
