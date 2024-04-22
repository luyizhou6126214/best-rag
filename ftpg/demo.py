#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date    :   2024/4/19 10:54
@Author  :   luyizhou
@Desc    :   
"""
import requests

uname = '15050480107'
# pwd = '654a1f7ee790260e882de1634be7f9ef_random_'
pwd = 'Dwzq@1234'

class MianSpider(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self):
        url = 'http://ftpg.dwzq.com.cn:28080/api/hrm/login/checkLogin'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Content-Length': '197',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            # 'Cookie': 'Hm_lvt_a3b958252fb1423cc1d542358e1ba68b=1712907076; Hm_lpvt_a3b958252fb1423cc1d542358e1ba68b=1712907076; ecology_JSessionid=4B57F48E4FB2EA394DCE07E314CECEB6; __clusterSessionCookieName=B25D79732419EF81019AB381720DD08C; SF_cookie_58=15733094; languageidweaver=7; loginuuids=7835; __randcode__=35f4c6ae-5afd-451c-a065-ba068646ee26; extloginid=; __clusterSessionIDCookieName=9d2d93a4-a709-446c-9e12-3c26aa2f0c5f',
            'Host': 'ftpg.dwzq.com.cn:28080',
            'Origin': 'http://ftpg.dwzq.com.cn:28080',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://ftpg.dwzq.com.cn:28080/wui/index.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        payload = {
            'islanguid': '7',
            'loginid': self.username,
            'userpassword': self.password,
            'dynamicPassword': '',
            'tokenAuthKey': '',
            'validatecode': '',
            'validateCodeKey': '',
            'logintype': '1',
            'messages': '',
            'isie': 'false',
            'appid': '',
            'service': '',
        }
        response = self.session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print(response.text)

    def query_work_hour_product(self, keyword):
        url = 'http://ftpg.dwzq.com.cn:28080/api/dwzq/workHour/queryWorkHourProductPbiSelectItem'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Content-Length': '68',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Host': 'ftpg.dwzq.com.cn:28080',
            'Origin': 'http://ftpg.dwzq.com.cn:28080',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://ftpg.dwzq.com.cn:28080/spa/custom/static/index.html?__random__=1713495708852',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        form_data = {
            'searchCondition': keyword,
            'pageSize': '10',
            'pageNo': '1',
            'versionId': 'DD198446753296672',
        }
        response = self.session.post(url, headers=headers, data=form_data)
        if response.status_code == 200:
            print(response.text)


if __name__ == '__main__':
    spider = MianSpider(uname, pwd)
    spider.login()
    spider.query_work_hour_product('AI')
