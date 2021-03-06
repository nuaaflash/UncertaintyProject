# -*- coding: utf-8 -*-

import wx

import NavPanel
import ShowPanel
import src.ModelManage.import_file

"""模型管理"""
class ModelPanel(wx.Panel):
    
    def __init__(self, parent = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()
        
    def InitUI(self):
        bSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_panel5 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)

        """添加菜单按钮"""
        self.button1 = wx.Button(self.m_panel5, wx.ID_ANY, u"模型设置", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        self.button1.SetBitmap(wx.Bitmap('icon/btn_show1.tga'))
        self.button1.Bind(wx.EVT_LEFT_DOWN, self.ClickModelManage)
        tabSizer.Add(self.button1, 0, wx.ALL, 5)
        self.button2 = wx.Button(self.m_panel5, wx.ID_ANY, u"参数设置", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        tabSizer.Add(self.button2, 0, wx.ALL, 5)
        self.button3 = wx.Button(self.m_panel5, wx.ID_ANY, u"数据导入", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)
        self.button4 = wx.Button(self.m_panel5, wx.ID_ANY, u"MyButton", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        tabSizer.Add(self.button4, 0, wx.ALL, 5)
        """"""

        self.m_panel5.SetSizer(tabSizer)
        self.m_panel5.Layout()
        tabSizer.Fit(self.m_panel5)
        bSizer.Add(self.m_panel5, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel6 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        """初始化左侧树状模型对象"""
        self.navPanel = NavPanel.NavPanel(self.m_panel6)
        bSizer4.Add(self.navPanel, 1, wx.EXPAND | wx.ALL, 5)
        """初始化展示界面对象"""
        self.showPanel = ShowPanel.ShowPanel(self.m_panel6)
        bSizer4.Add(self.showPanel, 3, wx.EXPAND | wx.ALL, 5)

        self.m_panel6.SetSizer(bSizer4)
        self.m_panel6.Layout()
        bSizer4.Fit(self.m_panel6)
        bSizer.Add(self.m_panel6, 4, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer)
        self.Layout()
        bSizer.Fit(self)
        
        
    def ClickModelManage(self, event):
        dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            src.ModelManage.import_file.insert_blob(project='一元非线性回归', _dir=dlg.GetPath()) #文件夹路径

        dlg.Destroy()
        