# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 16:29
# @Author  : ForthEspada

#公布公告信息界面
import sys
sys.path.append('..')
# from login import *
from lxml import etree

class GB_Info(object):
		def __init__(self,html):
			pass
		def get_value(self, content):
			if len(content) == 1:
				return content[0]
			else:
				return ''

		def get_element(self, content):
			if len(content) == 0:
				return ''
			elif len(content) == 1:
				return content[0]
			else:
				return content

		def parse_page(self,html):
			selector = etree.HTML(html)
			publicationsitems = selector.xpath('//*[@id="gkggid"]/table/tbody/tr')
			publicationslist = []
			for item in publicationsitems:
				number = item.xpath('td/span[@name="record_gkgg:gonggaoh"]/@title')
				type = item.xpath('td/span[@name="record_gkgg:gongkaigglx"]/@title')
				volume = item.xpath('td/span[@name="record_gkgg:juanqih"]/@title')
				date = item.xpath('td/span[@name="record_gkgg:gonggaor"]/@title')
				publication = {
					'number':self.get_value(number),
					'type':self.get_value(type),
					'volume':self.get_value(volume),
					'date':self.get_value(date),
				}
				publicationslist.append(publication)
			publications = self.get_element(publicationslist[1:])

			affairsitems = selector.xpath('//*[@id="swggid"]/table/tbody/tr')
			affairslist = []
			for item in affairsitems:
				type = item.xpath('td/span[@name="record_swgg:shiwugglxdm"]/@title')
				volume = item.xpath('td/span[@name="record_swgg:juanqih"]/@title')
				date = item.xpath('td/span[@name="record_swgg:gonggaor"]/@title')
				affair = {
					'type':self.get_value(type),
					'volume':self.get_value(volume),
					'date':self.get_value(date),
				}
				affairslist.append(affair)
			affairs = self.get_element(affairslist[1:])

			gb_info = {
				'publications':publications,
				'affairs':affairs,
			}
			return gb_info



