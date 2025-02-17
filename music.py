import urllib.request
import requests
import threading
import os
import re
import wx
import wx.xrc
from bs4 import BeautifulSoup

headers = {
    'Referer': 'https://music.163.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 "
                  "Safari/537.36"
}
class MyFrame1(threading.Thread, wx.Frame):
    musicData = []

    def __init__(self, threadID, name, counter):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=u"网易云音乐歌曲批量下载", pos=wx.DefaultPosition,
                          size=wx.Size(450, 409), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Url", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        self.m_staticText3.SetFont(
            wx.Font(13, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        bSizer5.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.url_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer5.Add(self.url_text, 0, wx.ALL, 5)

        self.down_button = wx.Button(self, wx.ID_ANY, u"下载歌单", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.down_button, 0, wx.ALL, 5)

        bSizer4.Add(bSizer5, 1, wx.EXPAND, 4)

        self.output_text = wx.TextCtrl(self, wx.ID_ANY, u" \
网易云音乐歌单下载，网页中复制URL\n \
https://music.163.com/#/playlist?id=xxxxxxxxxx\n \
保存目录：D:\\music\n \
线程只能执行一次，下载后如需重新下载其他需要重启\n \
可多开下载同个歌单或者不同歌单\n \
-------------------------------------------------------\n \
支持歌单和排名榜 - ccphamy\n \
-------------------------------------------------------\n" \
                                       , wx.DefaultPosition, wx.Size(450, 320), wx.TE_MULTILINE)

        bSizer4.Add(self.output_text, 0, wx.ALL, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.down_button.Bind(wx.EVT_BUTTON, self.main_button_click)

        # 多线程
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

        if not os.path.exists("d:/music"):
            os.mkdir('d:/music')

    def main_button_click(self, event):
        self.musicData = []
        # print(self.url_text.GetValue().replace("#/", ""))
        ue = self.url_text.GetValue().replace("#/", "")
        res = requests.get(ue, headers=headers)
        for i in re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res.text):
            download_url = "http://music.163.com/song/media/outer/url?id=%s" % i[0]
            try:
                with open('d:/music/' + i[1] + '.mp3', 'wb') as f:
                    f.write(requests.get(download_url, headers=headers).content)
                    self.output_text.AppendText('***** ' + i[1] + '.mp3 ***** Downloading...\n')
            except:
                self.output_text.AppendText(i[1] + u'.mp3 *****Download wrong~\n')
        self.output_text.AppendText('Download complete ' + ' files !\n')

    # event.Skip()

def main():
    app = wx.App(False)
    frame = MyFrame1(1, "Thread-1", 1)
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()
