#!/usr/bin/env python
# coding:utf-8

import requests,os
from hashlib import md5
import config
class Chaojiying_Client(object):

    def __init__(self):
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'
        }
    def init_config(self,user,psd):
        self.username = user
        password = psd.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = '897922'
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
    def open_first_captcha_pic(self,thread_inx):
        # os.remove(r'captcha_pic\first_captcha.jpg')
        captcha_path = str(r'captcha_pic\first_captcha' + thread_inx + '.png')
        captcha_path1 = str(r'captcha_pic\first_captcha' + thread_inx + '.jpg')
        os.rename(captcha_path,captcha_path1)
        first_im = open(captcha_path1, 'rb').read()
        os.remove(captcha_path1)
        return first_im,9103

    def open_second_captcha_pic(self):
        os.remove(r'captcha_pic\second_captcha.jpg')
        os.rename(r'captcha_pic\second_captcha.png',r'captcha_pic\second_captcha.jpg')
        second_im = open(r'captcha_pic\second_captcha.jpg', 'rb').read()
        return second_im,6001


    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


# if __name__ == '__main__':
#     chaojiying = Chaojiying_Client()	#用户中心>>软件ID 生成一个替换 96001
#     im,code= chaojiying.open_first_captcha_pic('0')										#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
#     json = chaojiying.PostPic(im, code)
#     print(type(json))
#     print(json['err_str'])
#     print(json['pic_str'])													#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

