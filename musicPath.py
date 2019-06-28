import requests
import re
import sys
from multiprocessing import Pool
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget

headers = {
    'Referer': 'https://music.163.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 "
                  "Safari/537.36"
}
class DS(QWidget):
    def download_song(self):
        ur = "https://music.163.com/#/song?id=34228719"
        song_id = ur[ur.find("id=") + 3:]
        # print(song_id)
        download_url = "http://music.163.com/song/media/outer/url?id=%s" % song_id
        try:
            directory1 = QFileDialog.getExistingDirectory(self,"选择文件夹", "/")
            print(directory1)
            # with open('d:/music/' + song_id + '.mp3', 'wb') as f:
            with open(directory1+'/' + song_id + '.mp3', 'wb') as f:
                f.write(requests.get(download_url, headers=headers).content)
        except FileNotFoundError:
            pass
        except OSError:
            pass


def get_songs():
    playlist_url = "https://music.163.com/playlist?id=530011217"
    res = requests.get(playlist_url, headers=headers)
    for i in re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res.text):
        download_url = "http://music.163.com/song/media/outer/url?id=%s" % i[0]
        try:
            with open('d:/music/' + i[1] + '.mp3', 'wb') as f:
                f.write(requests.get(download_url, headers=headers).content)
        except FileNotFoundError:
            pass
        except OSError:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ds = DS()
    ds.download_song()
    

