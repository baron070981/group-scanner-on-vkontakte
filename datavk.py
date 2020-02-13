import os
import sys
import vk_requests
from pprint import pprint


import globalvars

# 7211649


class VkData:
    def __init__(self):
        self.__login = ''
        self.__password = ''
        self.app_id = 0
        self.owner_id = 0
        self.INIT_APP_DATA = False
        self.INIT_API = False
        self.GROUP_DATA = False
        self.api = None
        self.urls_ids = list() # [[id, url],[id, url]]
        self.cash_id = list()
        
    
    def init_app_data(self, login:str, password:str, app_id:int, owner_id:int):
        self.__login = login
        self.__password = password
        self.app_id = app_id
        owner_id = int(owner_id)
        app_id = int(app_id)
        if owner_id == 0:
            self.INIT_APP_DATA = False
            return
        elif owner_id > 0:
            self.owner_id = -owner_id
            self.INIT_APP_DATA = True
            return
        else:
            self.owner_id = owner_id
            self.INIT_APP_DATA = True
            return
    
    
    def init_api(self):
        if self.INIT_APP_DATA == False:
            self.INIT_API = False
            return
        try:
            self.api = vk_requests.create_api(app_id = self.app_id,
                                              login = self.__login,
                                              password = self.__password)
            self.INIT_API = True
        except:
            print('Error init API')
            self.INIT_API = False
    
    
    def get_data_from_group(self, offset = 0, count =  5):
        print('Get data from group')
        if self.INIT_API == False:
            self.GROUP_DATA = False
            return
        data = self.api.wall.get(owner_id=self.owner_id, offset = offset, count = count)
        if len(data['items']) > 0:
            self.GROUP_DATA = True
            self.urls_ids.clear()
            for item_data in data['items']:
                if 'attachments' in item_data:
                    url_a = item_data['attachments'][0]
                    if 'photo' in url_a:
                        url = url_a['photo']['sizes'][-1]['url']
                        _id = url_a['photo']['id']
                        if _id not in globalvars.cach_ids:
                            globalvars.cach_ids.append(_id)
                        self.urls_ids.append(list([_id, url]))
        else:
            self.GROUP_DATA = False
            return








    
    
    
    
    


