import requests,json,time
from requests.exceptions import ConnectTimeout
class Post(object):
	def __init__(self):
		pass
	def post(self,data,id):
		self.data = data
		self.data = json.dumps(self.data)
		url = 'https://www.hongjianguo.com/public/cpquery'
		result = {
			'authorization':'CpqueryIsABadGuy',
			'apn':id,
			'data':self.data
		}
		try:
			response = requests.post(url,result,timeout = 1)
			t = json.loads(response.text)
			print('post:',t['status'],id,result)
			return t['status']
		except:
			return '接口反应时间超过1秒'


