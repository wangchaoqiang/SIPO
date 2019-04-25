import requests

'''国家知识产权局，登陆及爬取  2013105833248'''
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36",
    "Cookie": "JSESSIONID=db43183b75608c489a5044ae1ec3"

}
url = 'http://cpquery.sipo.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=2013105833248&select-key:zhuanlimc=&select-key:shenqingrxm=&select-key:zhuanlilx=&select-key:shenqingr_from=&select-key:shenqingr_to=&verycode=12&inner-flag:open-type=window&inner-flag:flowno=1543192790256'

def get_html(url):
	response = requests.get(url,headers=headers)
	if response.status_code == 200:
		return True
	else:
		return False

def main():
	i = 0
	try:
		while(get_html(url)):
			i += 1
	except:
		return i

if __name__ == '__main__':
	print(main())