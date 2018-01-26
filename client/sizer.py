# -*- coding: utf-8 -*-
# @Date:   2018-01-24 17:54:45
# @Last Modified time: 2018-01-24 17:55:08
from client import (
    wx,
    Single,
    COLOR_WHITE,
    COLOR_GREEN,
    COLOR_BLUE,
    FONT12,
    FONT13
)
from .notice_button import NoticeButton
from .record_panel import RecordPanel


class LeftSizer(Single):

    def __init__(self, panel):
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        self.user_list_box = wx.ListBox(
            parent=panel, id=11, name='user_list', choices=[], style=wx.LB_SINGLE
        )
        self.user_list_box.SetFont(FONT12)
        self.user_list_box.SetForegroundColour(COLOR_WHITE)
        self.user_list_box.SetBackgroundColour(COLOR_GREEN)
        self.user_list_box.Insert("group", 0)

        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.Add(
            self.user_list_box, proportion=10, border=0, flag=wx.EXPAND | wx.ALL
        )


class RightTopSizer(NoticeButton):

    def __init__(self, panel):
        super(RightTopSizer, self).__init__(panel)
        self.user_name_text = wx.StaticText(
            parent=panel, id=22, size=(0, 30), label="", style=wx.ALIGN_CENTER
        )
        self.user_name_text.SetFont(FONT13)
        self.user_name_text.SetForegroundColour(COLOR_BLUE)
        self.right_top_sizer = wx.BoxSizer()
        self.right_top_sizer.Add(
            self.notice_button, proportion=4.5, border=240, flag=wx.EXPAND | wx.RIGHT
        )
        self.right_top_sizer.Add(
            self.user_name_text, proportion=5.5, border=0, flag=wx.EXPAND | wx.LEFT
        )


class RightSizer(RecordPanel, RightTopSizer):

    def __init__(self, panel):
        RecordPanel.__init__(self, panel)
        RightTopSizer.__init__(self, panel)

        self.input_field = wx.TextCtrl(
            parent=panel, id=23, value="", style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.send_button = wx.Button(
            parent=panel, id=24, size=(0, 40), label=u"发送"
        )
        self.input_field.SetFont(FONT12)
        self.send_button.SetFont(FONT13)

        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(
            self.right_top_sizer, proportion=0, border=0, flag=wx.EXPAND | wx.LEFT
        )
        self.right_sizer.Add(
            self.record_panel, proportion=8, border=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT
        )
        self.right_sizer.Add(
            self.input_field, proportion=2, border=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
        )
        self.right_sizer.Add(
            self.send_button, proportion=0, border=250, flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
        )


class Sizer(LeftSizer, RightSizer):

    def __init__(self, panel):
        LeftSizer.__init__(self, panel)
        RightSizer.__init__(self, panel)

        self.main_sizer = wx.BoxSizer()
        self.main_sizer.Add(
            self.left_sizer, proportion=2.5, border=5, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM
        )
        self.main_sizer.Add(
            self.right_sizer, proportion=7.5, border=5, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM
        )
        panel.SetSizer(self.main_sizer)
