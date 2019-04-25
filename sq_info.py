# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 16:29
# @Author  : ForthEspada

#申请信息界面
import sys,re
sys.path.append('..')
from lxml import etree

class SQ_Info(object):
	def __init__(self,html):
		pass
		#self.parse_page(html)
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
		apn = selector.xpath('//*[@id="zlxid"]/div[1]/table/tbody/tr[1]/td[2]/span/@title')
		apd = selector.xpath('//*[@id="zlxid"]/div[1]/table/tbody/tr[2]/td[2]/span/@title')
		title = selector.xpath('//*[@id="zlxid"]/div[2]/table/tbody/tr[1]/td[2]/text()')
		if len(title)==1:
			title[0] = title[0].strip('\t').strip()
		main_ipc = selector.xpath('//*[@id="zlxid"]/div[2]/table/tbody/tr[2]/td[2]/span/@title')
		division_apd = selector.xpath('//*[@id="zlxid"]/div[2]/table/tbody/tr[3]/td[2]/span/@title')
		status = selector.xpath('//*[@id="zlxid"]/div[1]/table/tbody/tr[3]/td[2]/span/@title')
		biblo = {
			'apn':self.get_value(apn),
			'apd':self.get_value(apd),
			'title':self.get_value(title),
			'main_ipc':self.get_value(main_ipc),
			'division_apd':self.get_value(division_apd),
			'status':self.get_value(status),
		 }
		name = selector.xpath('//*[@id="sqrid"]/table/tbody/tr[2]/td[1]/span/@title')
		citizenship = selector.xpath('//*[@id="sqrid"]/table/tbody/tr[2]/td[2]/span/@title')
		postcode = selector.xpath('//*[@id="sqrid"]/table/tbody/tr[2]/td[3]/span/@title')
		address = selector.xpath('//*[@id="sqrid"]/table/tbody/tr[2]/td[4]/span/@title')
		applicants = {
			'name':self.get_value(name),
			'citizenship':self.get_value(citizenship),
			'postcode':self.get_value(postcode),
			'address':self.get_value(address)
		}
		names = selector.xpath('//*[@id="fmrid"]/table/tbody/tr/td[2]/span/@title')
		inventors = {
			'names':self.get_value(names)
		}

		name = selector.xpath('//*[@id="lxrid"]/div[1]/table/tbody/tr[1]/td[2]/span/@title')
		address = selector.xpath('//*[@id="lxrid"]/div[2]/table/tbody/tr/td[2]/span/@title')
		postcode = selector.xpath('//*[@id="lxrid"]/div[1]/table/tbody/tr[2]/td[2]/span/@title')
		contact = {

			'name':self.get_value(name),
			'address':self.get_value(address),
			'postcode':self.get_value(postcode)
		}
		name = selector.xpath('//*[@id="zldlid"]/div[1]/table/tbody/tr/td[2]/span/@title')
		agent = selector.xpath('//*[@id="zldlid"]/div[2]/table/tbody/tr/td[2]/span/@title')
		agency = {
			'name':self.get_value(name),
			'agent':self.get_value(agent)
		}
		apn = selector.xpath('//*[@id="yxqid"]/table/tbody/tr[2]/td[1]/span[@name="record_yxq:zaixiansqh"]/@title')
		apd = selector.xpath('//*[@id="yxqid"]/table/tbody/tr[2]/td[1]/span[@name="record_yxq:zaixiansqrq"]/@title')
		ipo = selector.xpath('//*[@id="yxqid"]/table/tbody/tr[2]/td[1]/span[@name="record_yxq:zaixiansqgb"]/@title')
		priorities = {
			'apn':self.get_value(apn),
			'apd':self.get_value(apd),
			'ipo':self.get_value(ipo)
		}
		pct_apn = selector.xpath('//*[@id="pctid"]/div[1]/table/tbody/tr[1]/td[2]/span/@title')
		pct_pn = selector.xpath('//*[@id="pctid"]/div[2]/table/tbody/tr[1]/td[2]/span/@title')
		pct_apd= selector.xpath('//*[@id="pctid"]/div[1]/table/tbody/tr[2]/td[2]/span/@title')
		pct_pd = selector.xpath('//*[@id="pctid"]/div[2]/table/tbody/tr[2]/td[2]/span/@title')
		national_stage = {
			'pct_apn':self.get_value(pct_apn),
			'pct_pn':self.get_value(pct_pn),
			'pct_apd':self.get_value(pct_apd),
			'pct_pd':self.get_value(pct_pd)
		}

		amendmentitems = selector.xpath('//*[@id="bgid"]/table/tbody/tr')
		amendmentlist = []
		for item in amendmentitems:
			effective_date = item.xpath('td/span[@name="record_zlxbg:biangengrq"]/@title')
			type = item.xpath('td/span[@name="record_zlxbg:biangengsx"]/@title')
			before = item.xpath('td/span[@name="record_zlxbg:biangengqnr"]/@title')
			after = item.xpath('td/span[@name="record_zlxbg:biangenghnr"]/@title')
			amendment = {
				'effective_date':self.get_value(effective_date),
				'type':self.get_value(type),
				'before':self.get_value(before),
				'after':self.get_value(after)
			}
			amendmentlist.append(amendment)
		amendments = self.get_element(amendmentlist)

		sq_info = {
			'biblo':biblo,
			'applicants':applicants,
			'inventors':inventors,
			'contact':contact,
			'agency':agency,
			'priorities':priorities,
			'national_stage':national_stage,
			'amendments':amendments
		}
		return sq_info



