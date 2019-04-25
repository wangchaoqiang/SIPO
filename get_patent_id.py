import requests
import json
import time
class Get_Patent_Id(object):
    # def __init__(self):
        # self.id_list = self.get_id()
    def get_id(self,num):
        url = 'https://www.hongjianguo.com/public/apns/?authorization=CpqueryIsABadGuy&count='+str(num)
        patent_id_str = requests.get(url)
        patent_id_str = patent_id_str.text
        # print(patent_id_str)
        patent_id_json = json.loads(patent_id_str)
        # print(patent_id_json['status'])
        patent_id_list1 = []
        if (patent_id_json['status'] == 'success'):
            apn_list = patent_id_json['data']
            for apn in apn_list:
                # print(apn['apn'])
                patent_id_list1.append(apn['apn'])
            return patent_id_list1
        else:
            # print(patent_id_json['info'])
            return patent_id_json['info']
    def get_account(self):
        url = 'https://www.hongjianguo.com/public/accounts?authorization=CpqueryIsABadGuy&count=1'
        accounts_str = requests.get(url).text
        # print(accounts_str)
        accounts_json = json.loads(accounts_str)
        # print(accounts_json['status'])
        if (accounts_json['status'] == 'success'):
            accounts_list = accounts_json['data']
            # print(accounts_list)
            for account in accounts_list:
                # print(account['username'], account['password'])
                return account['username'],account['password']
        else:
            return 'failed','failed'