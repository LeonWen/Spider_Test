# -*- coding:utf-8 -*-

import urllib
import urllib2

values = {
	"username":"wenhecpp@126.com",
	"password":"wenhe07052414",
}
data = urllib.urlencode(values)
## 以下是 POST 方法
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
url = "https://www.zhihu.com/#signin"
request = urllib2.Request(url,data)

## 以下是 GET 方法
# url = "https://passport.csdn.net/account/login"
# url = "https://www.zhihu.com/#signin"
# geturl = url + "?" + data
# request = urllib2.Request(geturl,data)

response = urllib2.urlopen(request)
print response.read()