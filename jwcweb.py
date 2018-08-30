from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, TextAreaField, PasswordField, validators, StringField
import requests
import pytesseract
from PIL import Image
import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys


class Jwc(object):
    def __init__(self, account='10170724', password='064719@a', scoredate='2017-2018-1', zhouli='2018-2019-1',
                 course='2018-2019-2'):
        self.session = requests.Session()
        self.account = account
        self.pwd = password
        self.scoredate = scoredate
        self.zhouli = zhouli
        self.course = course

    def encoded(self, account='', passwd=''):
        max = sys.maxsize
        keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

        def charAt(keystring, num):
            return keystring[int(num)]

        def isNaN(num):
            return num != int(num)

        def encodeInp(inputcode):
            chr1 = chr2 = chr3 = ""
            enc1 = enc2 = enc3 = enc4 = ""
            output = ""
            i = 0
            length = len(inputcode)
            for k in range(max):
                if i < 0 or i >= length:
                    chr1 = "1"
                    i = i + 1
                else:
                    chr1 = int(ord(inputcode[i]))
                    i = i + 1
                if i < 0 or i >= length:
                    chr2 = "1"
                    i = i + 1
                else:
                    chr2 = int(ord(inputcode[i]))
                    i = i + 1
                if i < 0 or i >= length:
                    chr3 = "1"
                    i = i + 1
                else:
                    chr3 = int(ord(inputcode[i]))
                    i = i + 1
                if isNaN(chr1):
                    chr1 = 0
                enc1 = chr1 >> 2
                if (isNaN(chr2)):
                    chr2 = 0
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
                    enc3 = enc4 = 64
                elif (isNaN(chr3)):
                    chr3 = 0
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
                    enc4 = 64
                else:
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
                    enc4 = chr3 & 63
                output = output + charAt(keyStr, enc1) + charAt(keyStr, enc2) + charAt(keyStr, enc3) + charAt(keyStr,
                                                                                                              enc4)
                chr1 = chr2 = chr3 = ""
                enc1 = enc2 = enc3 = enc4 = ""
                if i >= length:
                    break
            return output

        account = encodeInp(account)
        passwd = encodeInp(passwd)
        encoded = account + "%%%" + passwd
        return encoded

    def login(self):
        while True:
            codeurl = 'http://inquiry.ecust.edu.cn/jsxsd/verifycode.servlet'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
            coderep = self.session.get(codeurl, headers=headers)
            with open('code.png', 'wb') as f:
                f.write(coderep.content)
            words = 'abcdefghigklmnopqrstuvwxyz1234567890'
            pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            image = Image.open('code.png')
            img = image.convert('L')
            img = img.resize((124, 44))
            code = pytesseract.image_to_string(img)
            code = code.lower()
            code_cut = ''
            for w in code:
                if w in words:
                    code_cut = code_cut + w
            print(code_cut.lower())
            if len(code_cut) == 4:
                loginurl = 'http://inquiry.ecust.edu.cn/jsxsd/xk/LoginToXk'
                headers['Referer'] = 'http://inquiry.ecust.edu.cn/jsxsd/xk/LoginToXk'
                data = {
                    'encoded': self.encoded(self.account, self.pwd),
                    'RANDOMCODE': str(code_cut)
                }
                loginrep = self.session.post(loginurl, data=data, headers=headers, allow_redirects=True)
                if '用户名或密码错误' in loginrep.text:
                    return u'用户名或密码错误'
                if '个人中心' in loginrep.text:
                    print('\n' + re.findall('<title>(.*?)</title>', loginrep.text)[0] + '\n')
                    break
        return '1'

    def inquiryscore(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
        inquiryurl = 'http://inquiry.ecust.edu.cn/jsxsd/kscj/cjcx_list'
        data = {
            'kksj': self.scoredate,
            'kcxz': '',
            'kcmc': '',
            'xsfs': 'all'
        }
        inquiryrep = self.session.post(inquiryurl, data=data, headers=headers)
        # print(inquiryrep.text)
        print('\n' + re.findall('<title>(.*?)</title>', inquiryrep.text)[0] + '\n')
        if '未查询到数据' in inquiryrep.text:
            print(
                '''++-------------++
                ++未查询到数据! ++
                ++-------------++''')
        else:
            html = BeautifulSoup(inquiryrep.text, 'html.parser')
            course = {'0': '执行计划内课程\n', '1': '执行计划外课程\n'}
            for kk in range(2):
                print(course[str(kk)])
                tablepre = PrettyTable(header=False)
                table = html.find_all('table', id=re.compile(''), class_=re.compile(''))[int(kk)]
                tr_ = BeautifulSoup(str(table), 'html.parser')
                tr = tr_.find_all('tr')
                for i in tr:
                    temp = []
                    for j in i.find_all('th'):
                        temp.append(str(j.text))
                    for j in i.find_all('td'):
                        temp.append(str(j.text))
                    del (temp[-1])
                    a = i.find_all('td', style=re.compile(''))
                    if len(a) == 0:
                        temp.append('期末成绩')
                        temp.append('平时成绩')
                    else:
                        href = re.findall('href="javascript:openWindow\(\'(.*?)\',', str(a[0]))[0]
                        url = 'http://inquiry.ecust.edu.cn' + str(href).replace('amp;', '')
                        urlrep = self.session.get(url, headers=headers)
                        urlhtml = BeautifulSoup(urlrep.text, 'html.parser')
                        # print(urlrep.text)
                        if len(urlhtml.find_all('td')) != 2:
                            temp.append(urlhtml.find_all('td')[1].text)
                            temp.append(urlhtml.find_all('td')[2].text)
                        else:
                            temp.append('--')
                            temp.append('--')
                    tablepre.add_row(temp)
                print(tablepre)
                print('\n')

    def coursetable(self):
        firsturl = 'http://inquiry.ecust.edu.cn/jsxsd/xskb/xskb_list.do'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
        data = {
            'cj0701id': '',
            'demo': '',
            'xnxq01id': self.course,
            'zc': ''
        }
        firstrep = self.session.post(firsturl, data=data, headers=headers)
        print('\n' + re.findall('<title>(.*?)</title>', firstrep.text)[0] + '\n')
        html = BeautifulSoup(firstrep.text, 'html.parser')
        # print(html.find_all('table')[1])
        table = PrettyTable(header=False)
        for i in BeautifulSoup(str(html.find_all('table')[1]), 'html.parser').find_all('tr'):
            temp = []
            for km in i.children:
                try:
                    temp.append(
                        BeautifulSoup(str(km), 'html.parser').text.strip().split('\n')[1].replace('-----------------',
                                                                                                  '\n-----------------------------------\n') + '\n')
                except:
                    temp.append(BeautifulSoup(str(km), 'html.parser').text.strip() + '\n')
            temp_ = []
            for jj in range(1, len(temp), 2):
                temp_.append(temp[jj])
            if len(temp) == 17:
                table.add_row(temp_)
            else:
                strr = ''
                for ll in range(len(temp)):
                    strr += str(temp[ll])
                print(strr.replace('\n', ''))
        print(table)

    def calendar(self):
        url = 'http://inquiry.ecust.edu.cn/jsxsd/jxzl/jxzl_query?Ves632DSdyV=NEW_XSD_WDZM'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
        data = {
            'xnxq01id': self.zhouli
        }
        rep = self.session.post(url, data=data, headers=headers)
        print('\n' + re.findall('<title>(.*?)</title>', rep.text)[0] + '\n')
        html = BeautifulSoup(rep.text, 'html.parser')
        table = PrettyTable(header=False)
        table_ = html.find_all('table')[1]
        for i in table_:
            temp = []
            t_html = BeautifulSoup(str(i), 'html.parser')
            for j in t_html.find_all('th'):
                temp.append(j.text.replace("\n\n", ''))
            for j in t_html.find_all('td'):
                temp.append(j.text)
            if len(temp) != 2 and len(temp) != 0:
                table.add_row(temp)
        print(table)

    def socialtest(self):
        url = 'http://inquiry.ecust.edu.cn/jsxsd/xsdjks/xsdjks_list?Ves632DSdyV=NEW_XSD_KSBM'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
        rep = self.session.get(url, headers=headers)
        print('\n' + re.findall('<title>(.*?)</title>', rep.text)[0] + '\n')
        html = BeautifulSoup(rep.text, 'html.parser')
        table = PrettyTable(header=False)
        table_ = html.find_all('table')[2]
        for i in table_.children:
            temp = []
            for j in BeautifulSoup(str(i), 'html.parser').find_all('th'):
                temp.append(j.text)
            for j in BeautifulSoup(str(i), 'html.parser').find_all('td'):
                temp.append(j.text.replace('\n', ''))
            if len(temp) != 0:
                table.add_row(temp)
        print(table)


app = Flask(__name__)


class LoginForm(Form):
    user = StringField('user', [validators.required()])
    pwd = PasswordField('pwd', [validators.required()])


@app.route('/', methods=['GET', 'POST'])
def main():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.user.data
        password = form.pwd.data
        print(username,password,type(username),type(password))
        p = Jwc(account=username, password=password)
        t = p.login()
        print(t)
        if '用户名或密码错误' in t:
            p.inquiryscore()
            return render_template('jwccheck.html',form=form,msg=t)
        elif t:
            return '<h1>登录成功,{}</h1>'.format(username)
    return render_template('jwccheck.html', form=form,msg='')


if __name__ == '__main__':
    app.run(debug=True, port=8880)
