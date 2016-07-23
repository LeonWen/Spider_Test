# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# set the headers
user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
headers = {'User-Agent':user_agent}
try:
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request)

    # content = response.read().decode('utf-8')
    # pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
    #                      '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    # items = re.findall(pattern,content)
    # for item in items:
    #     print item[0],item[1],item[2],item[3],item[4]

    content = response.read().decode('utf-8')
    # '<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>'
    # authorPattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?title=(.*?)>.*?</a>')
    authorPattern = re.compile('<div.*?class="content".*?title="(.*?)">(.*?)</div>',re.S)
    author = re.findall(authorPattern,content)
    # 这里的正则匹配一直搞不明白啊
except urllib2.URLError,e:
    # hasattr means if has the attribution
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason