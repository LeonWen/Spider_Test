# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
from bs4 import BeautifulSoup

class OUC:
    def __init__(self,username,password):
        self.loginUrl = "http://graduate.ouc.edu.cn/j_acegi_security_check"
        # self.leftFrameUrl = "http://graduate.ouc.edu.cn/listLeft.do?"
        self.frameGradeUrl = "http://graduate.ouc.edu.cn/accessModule.do?moduleId=25011&amp;groupId="
        # self.gradeUrl = "http://graduate.ouc.edu.cn/listMyBulletin.do?"
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'j_username':username,
            'j_password':password,
            'groupId':''
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def getPage(self):
        user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        headers = {'User-Agent':user_agent}
        request = urllib2.Request(
            url=self.loginUrl,
            data=self.postdata,
            headers=headers
        )
        result = self.opener.open(request)
        gradeResult = self.opener.open(self.frameGradeUrl)
        btfsp = BeautifulSoup(gradeResult.read())
        # print  btfsp.prettify()

        content = btfsp.body.find_all("tr")
        resultTable = [[0 for col in range(3)] for row in range(14)]
        print u'专业名称'.rjust(15),'\t',u'成绩','\t',u'学分'
        i = 0
        for item in content[1:]:
            itemList = item.find_all("td")
            classname = itemList[1].text.split(' ')[0].strip()
            score = itemList[6].text.split('\n')[7].strip()
            weight = itemList[7].text
            resultTable[i][0] = classname
            resultTable[i][1] = float(score)
            resultTable[i][2] = float(weight)
            print classname.rjust(15),'\t',score.rjust(3),'\t',weight.rjust(3)
            i += 1
            # print '%10s' % classname,'%-3s' % score.split('\n')[7],'\t',weight
        # 计算GPA
        sumGPA = 0
        sumWeight = 0
        for k in range(14):
            sumWeight += resultTable[k][2]
            sumGPA += resultTable[k][1] * resultTable[k][2]
            gpa = sumGPA / sumWeight

        print u'\n学分绩点为:',gpa


    # def writeInfo(self,text):
    #     for items in text:
    #         pass

if __name__ == '__main__':
    # ouc_stu = OUC()
    print '================ Welcome ===================='
    print u'Please enter your login messages:'
    username = input('username:')
    password = input('password:')
    print u'Waiting...'
    ouc_stu = OUC(username,password)
    ouc_stu.getPage()