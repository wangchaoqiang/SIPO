# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 16:35
# @Author  : ForthEspada

#发文信息界面
# 退信信息因为没有模板 没做

import sys
sys.path.append('..')
# from login import *
from lxml import etree

class FW_Info(object):
	def __init__(self,html):
		pass
		# self.parse_page(html)
	def get_value(self,content):
		if len(content)==1:
			return content[0]
		else:
			return ''
	def get_element(self,content):
		if len(content) == 0:
			return ''
		elif len(content) ==1:
			return content[0]
		else:
			return content


	def parse_page(self,html):
		selector = etree.HTML(html)
		noticeitems = selector.xpath('//*[@id="fwid"]/table/tbody/tr')
		noticeslist = []
		for item in noticeitems:
			name = item.xpath('td/span[@name="record_fawen:tongzhislx"]/@title')
			mail_date = item.xpath('td/span[@name="record_fawen:fawenrq"]/@title')
			recipient = item.xpath('td/span[@name="record_fawen:shoujianrxm"]/@title')
			postcode = item.xpath('td/span[@name="record_fawen:shoujianyzbm"]/@title')
			download_date = item.xpath('td/span[@name="record_fawen:xiazaisj"]/@title')
			download_ip = item.xpath('td/span[@name="record_fawen:xiazaiip"]/@title')
			manner = item.xpath('td/span[@name="record_fawen:fawenlx"]/@title')
			notice = {
				'name':self.get_value(name),
				'mail_date':self.get_value(mail_date),
				'recipient':self.get_value(recipient),
				'postcode':self.get_value(postcode),
				'download_date':self.get_value(download_date),
				'download_ip':self.get_value(download_ip),
				'manner':self.get_value(manner)

			}
			noticeslist.append(notice)
		notices = self.get_element(noticeslist[1:])

		certificateitems = selector.xpath('//*[@id="zsid"]/table/tbody/tr')
		certificateslist = []
		for item in certificateitems:
			mail_date = item.xpath('td/span[@name="record_zhengshu:fawenrq"]/@title')
			recipient = item.xpath('td/span[@name="record_zhengshu:shoujianrxm"]/@title')
			postcode = item.xpath('td/span[@name="record_zhengshu:shoujianyzbm"]/@title')
			certificate = {
				'mail_date':self.get_value(mail_date),
				'recipient':self.get_value(recipient),
				'postcode':self.get_value(postcode),

			}
			certificateslist.append(certificate)
		certificates =self.get_element(certificateslist[1:])


		faliure_noticeitems = selector.xpath('//*[@id="txid"]/table/tbody/tr')
		faliure_noticeslist = []
		for item in faliure_noticeitems:
			name = item.xpath('td/span[@name="record_fawen:tongzhislx"]/@title')
			original_recipient = item.xpath('td/span[@name="record_fawen:fawenrq"]/@title')
			original_mail_date = item.xpath('td/span[@name="record_fawen:shoujianrxm"]/@title')
			faliure_reason = item.xpath('td/span[@name="record_fawen:shoujianyzbm"]/@title')
			resent_recipient = item.xpath('td/span[@name="record_fawen:xiazaisj"]/@title')
			resent_mail_date = item.xpath('td/span[@name="record_fawen:xiazaiip"]/@title')
			pub_del_volume = item.xpath('td/span[@name="record_fawen:fawenlx"]/@title')
			pub_del_date = item.xpath('td/span[@name="record_fawen:fawenlx"]/@title')
			notice = {
				'name':self.get_value(name),
				'original_recipient':self.get_value(original_recipient),
				'original_mail_date':self.get_value(original_mail_date),
				'faliure_reason':self.get_value(faliure_reason),
				'resent_recipient':self.get_value(resent_recipient),
				'resent_mail_date':self.get_value(resent_mail_date),
				'pub_del_volume':self.get_value(pub_del_volume),
				'pub_del_date':self.get_value(pub_del_date)

			}
			faliure_noticeslist.append(notice)
		faliure_notices = self.get_element(faliure_noticeslist[1:])

		fw_info = {
			'notices':notices,
			'certificates':certificates,
			'faliure_notices':faliure_notices,

		}
		return fw_info



