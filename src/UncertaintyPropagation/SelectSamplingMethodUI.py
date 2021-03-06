# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################

import wx
import wx.xrc

from SamplingMethod import *
from MySqlManager import Oursql as oursql


class SelectSamplingMethodFrame(wx.Frame):

    def __init__(self, parent, kind='normal', *para):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"选择抽样方法", pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.kind = kind  # 分布类型
        self.para = para  # 参数

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        ''' 样本大小的panel begins '''
        self.m_panel_size = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_size.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        bSizer_size = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_size = wx.StaticText(self.m_panel_size, wx.ID_ANY, u"数    量", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.m_staticText_size.Wrap(-1)
        bSizer_size.Add(self.m_staticText_size, 0, wx.ALL, 5)

        self.m_textCtrl_size = wx.TextCtrl(self.m_panel_size, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        bSizer_size.Add(self.m_textCtrl_size, 0, wx.ALL, 5)

        self.m_panel_size.SetSizer(bSizer_size)
        self.m_panel_size.Layout()
        bSizer_size.Fit(self.m_panel_size)
        ''' 样本大小的panel ends '''

        bSizer_main.Add(self.m_panel_size, 1, wx.EXPAND | wx.ALL, 5)

        ''' 选择抽样方法的panel begins '''
        self.m_panel_method = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_method.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        bSizer_method = wx.BoxSizer(wx.VERTICAL)

        self.m_radioBtn_random = wx.RadioButton(self.m_panel_method, wx.ID_ANY, u"随机抽样", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        bSizer_method.Add(self.m_radioBtn_random, 0, wx.ALL, 5)

        self.m_radioBtn_LHS = wx.RadioButton(self.m_panel_method, wx.ID_ANY, u"拉丁超立方抽样", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        bSizer_method.Add(self.m_radioBtn_LHS, 0, wx.ALL, 5)

        self.m_radioBtn_MC = wx.RadioButton(self.m_panel_method, wx.ID_ANY, u"蒙特卡洛方法", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        bSizer_method.Add(self.m_radioBtn_MC, 0, wx.ALL, 5)

        self.m_panel_method.SetSizer(bSizer_method)
        self.m_panel_method.Layout()
        bSizer_method.Fit(self.m_panel_method)
        ''' 选择抽样方法的panel ends '''

        bSizer_main.Add(self.m_panel_method, 3, wx.EXPAND | wx.ALL, 5)

        ''' 确认和重置按钮的panel begins '''
        self.m_panel_ok = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_ok.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        bSizer_ok = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button_ok = wx.Button(self.m_panel_ok, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_ok.Add(self.m_button_ok, 0, wx.ALL, 5)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.create_sample)

        bSizer_ok.AddSpacer(70)

        self.m_button_reset = wx.Button(self.m_panel_ok, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_ok.Add(self.m_button_reset, 0, wx.ALL, 5)
        self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)

        self.m_panel_ok.SetSizer(bSizer_ok)
        self.m_panel_ok.Layout()
        bSizer_ok.Fit(self.m_panel_ok)
        ''' 确认和重置按钮的panel ends '''

        bSizer_main.Add(self.m_panel_ok, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        self.set_method_enable()  # 初始设置可用的抽样方法

    def __del__(self):
        pass

    def set_kind_and_para(self, kind, *para):
        """ 外部设置分布类型和参数 """
        self.kind = kind
        self.para = para
        self.set_method_enable()  # 重新设置可选的抽样方法

    def set_method_enable(self):
        """ 根据样本服从的分布来设置可用的抽样方法 """
        if self.kind == 'normal':
            self.m_radioBtn_MC.Enable(False)
            self.m_radioBtn_LHS.Enable(False)
        elif self.kind == 'exponential':
            self.m_radioBtn_MC.Enable(False)
            self.m_radioBtn_LHS.Enable(False)
        elif self.kind == 'uniform':
            self.m_radioBtn_LHS.Enable(False)
        elif self.kind == 'other':
            self.m_radioBtn_random.Enable(False)
            self.m_radioBtn_LHS.Enable(False)
        else:
            self.m_radioBtn_random.Enable(False)
            self.m_radioBtn_LHS.Enable(False)
            self.m_radioBtn_MC.Enable(False)

    def create_sample(self, event):
        """ 用户点击确定按钮后开始抽样并写入数据库 """
        size = int(self.m_textCtrl_size.GetValue())
        print self.para[0]
        stra = 0  # 具体策略编号
        method_name = 'random'  # 具体方法的名称
        result = None
        if self.m_radioBtn_random.GetValue():
            stra = 1
            method_name = 'random'
        elif self.m_radioBtn_LHS.GetValue():
            stra = 2
            method_name = 'LHS'
        elif self.m_radioBtn_MC.GetValue():
            stra = 3
            method_name = 'MC'

        # FIXME: 这里由于元组的问题，必须传入足够多的参数，传入para的数量是现有分布所需参数个数的最大值
        result = strategy[stra].GetResult(size, kind_dict[self.kind],
                                          self.para[0], self.para[1], self.para[2])
        oursql.clear_sampling_result()
        oursql.insert_sampling_result(result, self.kind, method_name)
        print 'Finished creating samples.'

    def reset_settings(self, event):
        """ 重置窗口中以输入的数据 """
        self.m_textCtrl_size.Clear()
        self.m_radioBtn_random.SetValue(False)
        self.m_radioBtn_MC.SetValue(False)
        self.m_radioBtn_LHS.SetValue(False)

'''
if __name__ == '__main__':
    app = wx.App(False)
    paras = [1.0, 0.5]
    frame = SelectSamplingMethodFrame(None, 'exponential', paras[0], paras[1])
    frame.Show()
    app.MainLoop()
'''