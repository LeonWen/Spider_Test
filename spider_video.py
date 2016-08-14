# -*- coding:utf-8 -*-
__author__ = 'LeonWen'

import re
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getMP4(html):
    r = r'data-video="(http.*\.mp4)"'
    re_mp4 = re.compile(r)
    mp4list = re.findall(re_mp4,html)
    filename = 1
    for mp4url in mp4list:
        urllib.urlretrieve(mp4url,"%s.mp4" % filename)
        filename += 1

url = 'http://www.meipai.com/media/566328335'
html = getHtml(url)
getMP4(html)