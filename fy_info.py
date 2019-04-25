# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 16:33
# @Author  : ForthEspada

#费用信息界面
#滞纳金信息与收据发文信息因为没有样本，无法写模板抓取

import sys
sys.path.append('..')
# from login import *
from lxml import etree

class FY_Info(object):
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

		fees_to_payitems = selector.xpath('//*[@id="djfid"]/table/tbody/tr')
		fees_to_paylist = []
		for item in fees_to_payitems:
			name = item.xpath('td/span[@name="record_yingjiaof:yingjiaofydm"]/@title')
			amount = item.xpath('td/span[@name="record_yingjiaof:shijiyjje"]/@title')
			deadline = item.xpath('td/span[@name="record_yingjiaof:jiaofeijzr"]/@title')
			fees_to_payinfo = {
				'name':self.get_value(name),
				'amount':self.get_value(amount),
				'deadline':self.get_value(deadline),

			}
			fees_to_paylist.append(fees_to_payinfo)
		fees_to_pay = self.get_element(fees_to_paylist[1:])

		fees_payeditems = selector.xpath('//*[@id="yjfid"]/table/tbody/tr')
		fees_payedlist = []
		for item in fees_payeditems:
			name = item.xpath('td/span[@name="record_yijiaof:feiyongzldm"]/@title')
			amount = item.xpath('td/span[@name="record_yijiaof:jiaofeije"]/@title')
			pay_mentdate = item.xpath('td/span[@name="record_yijiaof:jiaofeisj"]/@title')
			payer = item.xpath('td/span[@name="record_yijiaof:jiaofeirxm"]/@title')
			receipt_no = item.xpath('td/span[@name="record_yijiaof:shoujuh"]/@title')
			fees_payedinfo = {
				'name':self.get_value(name),
				'amount':self.get_value(amount),
				'pay_mentdate':self.get_value(pay_mentdate),
				'payer':self.get_value(payer),
				'receipt_no':self.get_value(receipt_no),

			}
			fees_payedlist.append(fees_payedinfo)
		fees_payed = self.get_element(fees_payedlist[1:])

		refundsitems = selector.xpath('//*[@id="tfid"]/table/tbody/tr')
		refundslist = []
		for item in refundsitems:
			name = item.xpath('td/span[@name="record_tuifei:feiyongzldm"]/@title')
			amount = item.xpath('td/span[@name="record_tuifei:tuifeije"]/@title')
			date = item.xpath('td/span[@name="record_tuifei:tuifeirq"]/@title')
			payee = item.xpath('td/span[@name="record_tuifei:tuifeirxm"]/@title')
			receipt_no = item.xpath('td/span[@name="record_tuifei:shoujuh"]/@title')
			refundsinfo = {
				'name':self.get_value(name),
				'amount':self.get_value(amount),
				'date':self.get_value(date),
				'payee':self.get_value(payee),
				'receipt_no':self.get_value(receipt_no),

			}
			refundslist.append(refundsinfo)
		refunds = self.get_element(refundslist[1:])

		late_feesitems = selector.xpath('//*[@id="znjid"]/table/tbody/tr')
		late_feeslist = []
		for item in late_feesitems:
			date = item.xpath('td/span[@name="record_zhinaj:zhinajrq"]/@title')
			renewal_fee = item.xpath('td/span[@name="record_zhinaj:tuifeirxm"]/@title')
			late_fee = item.xpath('td/span[@name="record_zhinaj:shoujuh"]/@title')
			sum = item.xpath('td/span[@name="record_zhinaj:shoujuh"]/@title')
			late_feesinfo = {
				'date':self.get_value(date),
				'renewal_fee':self.get_value(renewal_fee),
				'late_fee':self.get_value(late_fee),
				'sum':self.get_value(sum),

			}
			late_feeslist.append(late_feesinfo)
		late_fees = self.get_element(late_feeslist)

		receiptsitems = selector.xpath('//*[@id="sjfw"]/table/tbody/tr')
		receiptslist = []
		for item in receiptsitems:
			type = item.xpath('td/span[@name="record_shoujufaw:shoujufawrq"]/@title')
			amount = item.xpath('td/span[@name="record_shoujufaw:shoujufawrxm"]/@title')
			payer = item.xpath('td/span[@name="record_shoujufaw:shoujuh"]/@title')
			payment_date = item.xpath('td/span[@name="record_shoujufaw:shoujuh"]/@title')
			receipt_no = item.xpath('td/span[@name="record_shoujufaw:tuifeirq"]/@title')
			receipt_title = item.xpath('td/span[@name="record_shoujufaw:tuifeirxm"]/@title')
			mail_address = item.xpath('td/span[@name="record_shoujufaw:shoujuh"]/@title')
			remittance_date = item.xpath('td/span[@name="record_shoujufaw:shoujuh"]/@title')
			is_sent = item.xpath('td/span[@name="record_shoujufaw:tuifeirq"]/@title')
			mail_date = item.xpath('td/span[@name="record_shoujufaw:tuifeirxm"]/@title')
			mail_serial = item.xpath('td/span[@name="record_shoujufaw:shoujuh"]/@title')
			refund_remitance_date = item.xpath('td/span[@name="record_shoujufaw:tuifeirq"]/@title')
			receiptsinfo = {
				'type':self.get_value(type),
				'amount':self.get_value(amount),
				'payer':self.get_value(payer),
				'payment_date':self.get_value(payment_date),
				'receipt_no':self.get_value(receipt_no),
				'receipt_title':self.get_value(receipt_title),
				'mail_address':self.get_value(mail_address),
				'remittance_date':self.get_value(remittance_date),
				'is_sent':self.get_value(is_sent),
				'mail_date':self.get_value(mail_date),
				'mail_serial':self.get_value(mail_serial),
				'refund_remitance_date':self.get_value(refund_remitance_date),

			}
			receiptslist.append(receiptsinfo)
		receipts = self.get_element(receiptslist)

		fy_info = {
			'fees_to_pay':fees_to_pay,
			'fees_payed':fees_payed,
			'refunds':refunds,
			'late_fees':late_fees,
			'receipts':receipts,
		}
		return fy_info



