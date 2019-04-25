# coding:utf-8
from PIL import Image
from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.append('..')
from sq_info import *
from fy_info import *
from fw_info import *
from  gb_info import *
from chaojiying import *
from get_patent_id import  *
from post import *
import threading
import re,os
import sys
import numpy as np
class Login():
	def __init__(self):
		self.top = 0
		self.bottom = 0
		self.left = 0
		self.right = 0
		self.data = '['
	def open(self,user_name,user_password,browser):
		"""打开网页输入用户名密码
		:return: None
  	"""
		self.browser = browser
		try:
			wait = WebDriverWait(self.browser,10)
			user = wait.until(EC.presence_of_element_located((By.ID, 'username1')))
			password = wait.until(EC.presence_of_element_located((By.ID, 'password1')))
			user.clear()
			password.clear()
			user.send_keys(user_name)
			password.send_keys(user_password)
			# print("加载成功")
			return "加载成功"
		except:
			# print("加载失败")
			time.sleep(10)
			return "加载失败"

	def write_error_log(self,row,thread_inx,error_depict,e):
		with open('logs/log{}  ({}).txt'.format(thread_inx,time.strftime('%m-%d', time.localtime(time.time()))), mode='a', encoding='utf-8') as f:
			except_str = 'time:{} ,thread:{} ,error_row:{} ,error_depict:{} ,e:{} ,'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), thread_inx,row, error_depict, e)
			f.write(str(except_str, ) + '\n')

	def save_screen(self, thread_inx):
		if(IS_ERROR_CUT_SCREEN == 'True'):
			im = ImageGrab.grab()
			error_path = str(r'error_pngs/{}-{}.png').format(thread_inx,time.strftime('%m%d-%H%M%S', time.localtime(time.time())))
			im.save(error_path)
		else:
			pass

	def save_current_screen(self,thread_inx):
		if (IS_ERROR_CUT_SCREEN == 'True'):
			error_path = str(r'error_pngs/{}-{}.png').format(thread_inx,time.strftime('%m%d-%H%M%S', time.localtime(time.time())))
			self.browser.save_screenshot(error_path)
		else:
			pass

	def get_first_captch(self,thread_inx):
		elem = self.browser.find_element(By.CLASS_NAME,'selectyzm_tips')
		location_text = elem.location
		text_size = elem.size
		# print("text",location_text,text_size)
		ActionChains(self.browser).move_to_element(elem).perform()
		elem2 = self.browser.find_element_by_id('jcaptchaimage')
		captcha_size = elem2.size
		while(captcha_size['height']<10):
			captcha_size = elem2.size
			time.sleep(0.3)
			ActionChains(self.browser).move_to_element(elem).perform()
		ActionChains(self.browser).move_to_element(elem2).perform()
		self.top,self.bottom,self.left,self.right = location_text['y']-captcha_size['height'],location_text['y']+text_size['height'],location_text['x'],location_text['x']+text_size['width']
		# print("left,top,right,bottom",self.left,self.top,self.right,self.bottom)
		captcha_path = str(r'captcha_pic\first_captcha'+thread_inx+'.png')
		self.browser.save_screenshot(captcha_path)
		im = Image.open(captcha_path)
		im = im.crop((self.left,self.top,self.right,self.bottom))
		# print("left,top,right,bottom",self.left,self.top,self.right,self.bottom)
		im.save(captcha_path)
		# print("第一张图片验证码保存成功！")

	def get_first_captch_result(self,thread_inx):
		chaojiying = Chaojiying_Client()	#用户中心>>软件ID 生成一个替换 96001
		chaojiying.init_config(CHAOJIYING_USERNAME,CHAOJIYING_PASSWORD)
		try:
			im,code= chaojiying.open_first_captcha_pic(thread_inx)#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
		except BaseException as e:
			self.write_error_log(sys._getframe().f_lineno,thread_inx,'验证码替换错误',e)
			self.browser.quit()
			path = str(r'captcha_pic\first_captcha' + thread_inx + '.png')
			path1 = str(r'captcha_pic\first_captcha' + thread_inx + '.jpg')
			if path in os.listdir(r'captcha_pic'):
				os.remove(path)
			if path1 in os.listdir(r'captcha_pic'):
				os.remove(path1)
			return 0
		json = chaojiying.PostPic(im, code)
		err_str, pic_str = json['err_str'], json['pic_str']
		if err_str == "OK":
			groups = pic_str.split('|')
			try:
				locations = [[int(number) for number in group.split(',')] for group in groups]
				return locations
			except BaseException as e:
				self.write_error_log(sys._getframe().f_lineno,thread_inx,'坐标返回错误',e)
				self.browser.quit()
				return 0
		elif err_str == '无可用题分':
			self.write_error_log(sys._getframe().f_lineno,thread_inx, '超级鹰账号没钱了，超级鹰官网为：http://www.chaojiying.com', '无可用题分')
			print("超级鹰账号没钱了，超级鹰官网为：http://www.chaojiying.com")
			self.browser.quit()
			return "超级鹰账号没钱"
	def reset_captcha_location(self):
		elem = self.browser.find_element_by_id('jcaptchaimage')
		ActionChains(self.browser).move_to_element(elem).perform()
	def touch_click_words(self,locations,thread_inx):
		try:
			for location in locations: #1059*218
				self.reset_captcha_location()
				# print('现在正在点击点',location[0],location[1])
				ActionChains(self.browser).move_by_offset(-153, -109).perform()
				ActionChains(self.browser).move_by_offset(location[0]-1,location[1]-1).click().perform()
		except BaseException as e:
			self.write_error_log(sys._getframe().f_lineno, thread_inx, '点击失败', e)
			# self.save_screen(thread_inx)
			return "登陆失败"
		# print("验证码点击完毕！")
		try:
			time.sleep(0.4)
			wait = WebDriverWait(self.browser,10)
			logbut = wait.until(EC.element_to_be_clickable((By.ID, 'publiclogin')))
			logbut.click()
			time.sleep(0.5)
			wait.until(EC.presence_of_element_located((By.ID, 'backBtn')))
		except BaseException as e:
			e_str = str(e)
			if 'timeout' in e_str:
				self.write_error_log(sys._getframe().f_lineno, thread_inx, '服务器超时未响应', e)
				# self.save_screen(thread_inx)
				time.sleep(600)
				return "服务器超时未响应"
			else:
				self.write_error_log(sys._getframe().f_lineno, thread_inx, '登陆失败', e)
				# self.save_screen(thread_inx)
				return "登陆失败"
	def get_token(self):
		source = self.browser.page_source
		tokens = re.findall(r'<input type="hidden" id=.*?value="(.*?)"', source)
		return tokens
	def get_html(self,url,thread_inx):
		try:
			self.browser.get(url)
			wait = WebDriverWait(self.browser,10)
			wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tab_box')))
			html = self.browser.page_source
			return html
		except BaseException as e:
			html = self.browser.page_source
			# self.save_screen(thread_inx)
			if '/images/reach_top.png' in html:
				self.write_error_log(sys._getframe().f_lineno, thread_inx, '账号查询次数已用完', e)
				return 0
			elif 'publiclogin' in html:
				self.write_error_log(sys._getframe().f_lineno, thread_inx, '请求超时,即将重新登陆', e)
				return 0
			elif '500 Server Error' in html:
				self.write_error_log(sys._getframe().f_lineno, thread_inx, '服务器异常', e)
				self.save_current_screen(thread_inx)
				time.sleep(120)
				return 0
			else:
				self.write_error_log(sys._getframe().f_lineno,thread_inx, '请求超时,已重新请求', e)
				time.sleep(5)
				self.get_html(url, thread_inx)

	def get_page(self,str_index,id,token,isfee,thread_inx):
		if(isfee):
			url = 'http://cpquery.sipo.gov.cn/{}.do?select-key:shenqingh={}&select-key:gonggaobj=0&token={}'.format(str_index, id, token)
		else:
			url = 'http://cpquery.sipo.gov.cn/{}.do?select-key:shenqingh={}&token={}'.format(str_index, id, token)
		result = self.get_html(url,thread_inx)
		return result

	def validate_account(self,id,sq_token,istoken,is_first,thread_inx):
		if(istoken == 1):
			self.tokens = sq_token
			self.sq_token = self.tokens[0]
		self.sq_html = self.get_page("txnQueryBibliographicData", id, self.sq_token, 0,thread_inx)
		# print('self.sq_html:',self.sq_html== '账号查询次数已用完')
		if (self.sq_html != 0):
			self.sq_info = SQ_Info(self.sq_html)
			self.sq_message = self.sq_info.parse_page(self.sq_html)
			try:
				self.tokens = self.get_token()
				self.sq_token = self.tokens[0]
				self.fy_token = self.tokens[3]
				self.fw_token = self.tokens[4]
				self.gb_token = self.tokens[5]
			except Exception as e:
				if(is_first):
					self.write_error_log(sys._getframe().f_lineno, thread_inx, 'tokens获取异常', e)
					return 0
				else:
					pass
		else:
			return 0
		# if sq_message==None:
		# 	self.browser.quit()
		# self.get_page("txnQueryPatentFileData",id, tokens[2],0)
		# wait.until(EC.presence_of_all_elements_located)
		self.fy_html = self.get_page("txnQueryFeeData", id, self.fy_token, 1,thread_inx)
		if (self.fy_html != 0):
			self.fy_info = FY_Info(self.fy_html)
			self.fy_message = self.fy_info.parse_page(self.fy_html)
		else:
			return 0
		self.fw_html = self.get_page("txnQueryDeliveryData", id, self.fw_token, 0,thread_inx)
		if (self.fw_html != 0):
			self.fw_info = FW_Info(self.fw_html)
			self.fw_message = self.fw_info.parse_page(self.fw_html)
		else:
			return 0
		self.gb_html = self.get_page("txnQueryPublicationData", id, self.gb_token, 0,thread_inx)
		if (self.gb_html != 0):
			self.gb_info = GB_Info(self.gb_html)
			self.gb_message = self.gb_info.parse_page(self.gb_html)
		else:
			return 0
		result = {
			'application': self.sq_message,
			'cost': self.fy_message,
			'send_message': self.fw_message,
			'publication_data': self.gb_message
		}
		result = "{'apn':'" + str(id) + "','data':"+ str(result) + "}"
		self.data = self.data + result + ","

	def post(self,data):
		url = 'https://www.hongjianguo.com/public/cpquery'
		try:
			data = data.replace('\'', '"')
			data = {
				"authorization": "CpqueryIsABadGuy",
				"data": data
			}
			response = requests.post(url, data)
			t = json.loads(response.text)
			if(t['status']=='success'):
				return 'success'
			else:
				return t['info']
		except:
			return '接口反应异常'
	def get_page_first(self,id,thread_inx,is_only_one):
		sq_token = self.get_token()
		is_first = 1
		validate = self.validate_account(id,sq_token,1,is_first,thread_inx)
		return validate
	def get_pages(self,id_list,thread_inx):
		index = 1
		try:
			for id in id_list:
				index = index + 1
				is_first = 0
				validate = self.validate_account(id,1,0,is_first,thread_inx)
				if (validate==0):
					if(index!=125):
						index = index - 1
						time.sleep(0.1)
						current_url = self.browser.current_url
						error_depict = str(r'线程异常结束--爬取{}条数据,当前URL为:{},爬取的专利号为:{}'.format(index,current_url,id))
						self.write_error_log(sys._getframe().f_lineno,thread_inx,error_depict," ")#self.browser.page_source
					break
		except BaseException as e:
			current_url = self.browser.current_url
			error_depict = str(r'线程异常结束--爬取{}条数据,当前URL为:{},爬取的专利号为:{}'.format(index, current_url, id))
			self.write_error_log(sys._getframe().f_lineno, thread_inx, error_depict, e)  # self.browser.page_source
		return index
	def login_button(self,user,password,mybrowser,thread_inx):
		open_statue = self.open(user, password, mybrowser)
		if(open_statue == '加载成功'):
			self.get_first_captch(thread_inx)
			locations = self.get_first_captch_result(thread_inx)
			# print(locations)
			if(locations == 0):
				return '登陆失败'
			if(locations == '超级鹰账号没钱'):
				return '超级鹰账号没钱'
			else:
				result = self.touch_click_words(locations,thread_inx)
			# print("login_button:",result)
			if(result =='登陆失败'):
				return '登陆失败'
			elif(result =="服务器超时未响应"):
				return '服务器超时未响应'
			else:
				return "登陆成功"
		else:
			error_path = str(r'error_pngs/{}-{}.png').format(thread_inx,time.strftime('%m%d-%H%M%S', time.localtime(time.time())))
			self.browser.save_screenshot(error_path)
			return '加载失败'
	def work(self,idlist,thread_inx):
		try:
			result_inx = 0
			is_only_one = 0
			if (len(idlist) == 1):
				is_only_one = 1
			page_first_result = self.get_page_first(idlist[0],thread_inx,is_only_one)
			if(page_first_result==0):
				time.sleep(0.1)
				current_url = self.browser.current_url
				error_depict = r'线程异常结束--爬取0条数据,当前URL为:{},爬取的专利号为:{}'.format(current_url, id)
				self.write_error_log(sys._getframe().f_lineno, thread_inx, error_depict, " ")
				self.browser.quit()
				return 0
			result_inx = 1
			if(len(idlist)>1):
				result_inx = self.get_pages(idlist[1:],thread_inx)
			str = ''.join(self.data)
			str = str[:-1] + ']'
			if (IS_WRITE_TXT == 'True'):
				write_txt = 'results/result{}.txt'.format(thread_inx)
				with open(write_txt, mode='a', encoding='utf-8') as f:
					f.write(str)
			if (IS_POST == 'True'):
				start_post_time = time.time()
				response = self.post(data=str)
				end_post_time = time.time()
				seconds = end_post_time - start_post_time
				m, s = divmod(seconds, 60)
				h, m = divmod(m, 60)  # 转化整个过程时间为时分秒
				if(response =='success'):
					post_result = 'thread:{},成功post:{}条数据'.format(thread_inx,result_inx)
					post_result = post_result + "用时%02d分%02d秒"%(m,s)
					print(post_result)
					self.write_error_log(sys._getframe().f_lineno,thread_inx, post_result, "")
				else:
					post_result = 'thread:{},post失败，原因为：{}'.format(thread_inx,response)
					self.write_error_log(sys._getframe().f_lineno, thread_inx, post_result, "")
					print('thread:',thread_inx,response)
			self.browser.quit()
			return result_inx
		except BaseException as e:
			str = '获取页面异常'
			self.write_error_log(sys._getframe().f_lineno, thread_inx, str, e)
			self.browser.quit()
			return result_inx
def thread(mylogion,thread_inx,patent_id_list):
	try:
		start_time = time.time()
		result_inx = mylogion.work(patent_id_list,thread_inx)
		end_time = time.time()
		seconds = end_time - start_time
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)  # 转化整个过程时间为时分秒
		print('thread:', thread_inx,'共爬取%d条数据' % result_inx, "所花费总时间为%02d分%02d秒" % (m, s))
		str = '线程运行结束，共爬取%d条数据,所花费总时间为%02d分%02d秒:'% (result_inx,m, s)
		mylogion.write_error_log(sys._getframe().f_lineno,thread_inx, str, "")
		if(RESTART == 'True'):
			go_login(thread_inx)
	except BaseException as e:
		str = 'thread异常'
		mylogion.write_error_log(sys._getframe().f_lineno, thread_inx, str, e)
		mylogion.browser.quit()
		if (RESTART == 'True'):
			go_login(thread_inx)
def get_text(login,thread_inx,patent_id_list):
	my_thread = threading.Thread(target=thread, args=(login,thread_inx,patent_id_list,))
	my_thread.start()
def set_ip():
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	path = r"chromedriver/chromedriver.exe"
	options.add_argument('disable-infobars')  # 谷歌不出现在被自动化工具控制
	options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
	# chrome_options.add_argument('Referer="http://cpquery.sipo.gov.cn/txnIndex.do"')
	# chrome_options.add_argument('Host=" cpquery.sipo.gov.cn"')
	options.add_argument('Connection= '+'close')
	user_agent_list = [
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
	]
	User_Agent = 'User-Agent' + '=' + np.random.choice(user_agent_list)
	options.add_argument(User_Agent)
	# options.add_argument(r'--proxy-server=http://117.57.38.9:4226')
	browser = webdriver.Chrome(executable_path=path,chrome_options=options)
	browser.get('http://cpquery.sipo.gov.cn/txnIndex.do')
	# browser.get('https://www.baidu.com/')
	browser.set_page_load_timeout(50)
	browser.maximize_window()
	return browser
def login_circulation(login,browser,ThreadNeedLogin,user,password,thread_inx,patent_id_list):
	i = 1
	while (ThreadNeedLogin):
		login_result = login.login_button(user, password, browser, thread_inx)
		if (login_result=="服务器超时未响应"):
			browser.quit()
			browser = set_ip()
			i = 1
		elif (login_result == '登陆成功'):
			ThreadNeedLogin = False
			get_text(login, thread_inx, patent_id_list)
		elif (login_result == '超级鹰账号没钱'):
			ThreadNeedLogin = False
		elif (login_result == '加载失败'):
			# login.save_current_screen(thread_inx)
			error_depict = r'加载失败,网站超时未响应....'
			login.write_error_log(sys._getframe().f_lineno, thread_inx, error_depict, " ")
			browser.quit()
			browser = set_ip()
		else:
			time.sleep(i)
			i += 5
			if i>15:
				error_path = str(r'error_pngs/{}-{}.png').format(thread_inx, time.strftime('%m%d-%H%M%S',time.localtime(time.time())))
				browser.save_screenshot(error_path)
				browser.quit()
				i = i/0
			browser.quit()
			browser = set_ip()

def get_patent_id_account(thread_inx,login):
		global condition_sqh ,condition_zh
		condition_sqh = True
		condition_zh  = True
		print_sqh = True
		print_zh = True
		while(condition_sqh):
			getid = Get_Patent_Id()
			patent_id_list = getid.get_id(ID_NUM)
			# patent_id_list = Patent_Id().get_patent()
			if (patent_id_list!='没有需要抓取的申请号'):
				condition_sqh = False
				while(condition_zh):
					user, password = getid.get_account()
					# print(user != 'failed')
					if (user != 'failed' and user!=""):
						condition_zh = False
						return patent_id_list,user,password
					else:
						if(print_zh):
							print('登陆账号已用完,程序将暂停至有可用登陆账号继续运行')
							str = '登陆账号已用完'
							login.write_error_log(sys._getframe().f_lineno, thread_inx, str, "")
							time.sleep(Request_interval_account)
							print_zh = False
						else:
							time.sleep(Request_interval_account)
			else:
				if(print_sqh):
					print('没有需要爬取的申请号，程序将暂停至有需要爬取的申请号继续运行')
					str = '没有需要爬取的申请号'
					login.write_error_log(sys._getframe().f_lineno, thread_inx, str, "")
					time.sleep(Request_interval_patent_number)
					print_sqh = False
				else:
					time.sleep(Request_interval_patent_number)

def go_login(thread_inx):
	login = Login()
	try:
		patent_id_list, user, password = get_patent_id_account(thread_inx, login)
	except BaseException as e:
		login.write_error_log(sys._getframe().f_lineno, thread_inx, "获取登陆账号，专利号异常", e)
		time.sleep(Request_interval_patent_number)
		go_login(thread_inx)
		return 0
	browser = set_ip()
	try:
		ThreadNeedLogin = True
		login_circulation(login,browser,ThreadNeedLogin,user,password,thread_inx,patent_id_list)
	except BaseException as e:
		login.write_error_log(sys._getframe().f_lineno, thread_inx, "登陆循环异常", e)
		browser.quit()
		time.sleep(Request_interval_patent_number)
		go_login(thread_inx)

def thread_work(thread_num):
	for i in range(thread_num):
		thread_inx = str(i)
		go_login(thread_inx)
def del_file(path):
	ls = os.listdir(path)
	for i in ls:
		c_path = os.path.join(path, i)
		if os.path.isdir(c_path):
			del_file(c_path)
		else:
			os.remove(c_path)
def del_files():
	try:
		del_file(r'results')
	except:
		pass
if __name__ == '__main__':
	thread_num = 8
	try:
		del_file(r'captcha_pic')
		del_file(r'error_pngs')
		del_file(r'results')
		# del_file(r'logs')
		f = open(r'config/config.txt')
		config_txt = json.loads(str(f.read()))
		config_dict = dict(config_txt)
		thread_num = int(config_dict['thread_num'])
		CHAOJIYING_USERNAME = config_dict['chaojiying_user']
		CHAOJIYING_PASSWORD = config_dict['chaojiying_password']
		ID_NUM = int(config_dict['id_num'])
		IS_WRITE_TXT = config_dict['is_write_txt']
		RESTART = config_dict['restart']
		IS_POST = config_dict['is_post']
		IS_ERROR_CUT_SCREEN = config_dict['is_error_cut_screen']
		Request_interval_account = int(config_dict['request_interval_account'])
		Request_interval_patent_number = int(config_dict['request_interval_patent_number'])
		thread_work(thread_num)
	except BaseException as e:
		print(e)
		time.sleep(2000)