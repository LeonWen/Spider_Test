# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

url = 'http://graduate.ouc.edu.cn/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
print response.read()