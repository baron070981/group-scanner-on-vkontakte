import sys
import os
import os.path
import shutil
import requests
from pprint import pprint

import globalvars




def check_appdata():
    with open(globalvars.images_names, 'w') as f:
        pass
    if not os.path.isfile(globalvars.appdata):
        globalvars.OLD_APP = False
        print(False)
        return False
    else:
        globalvars.OLD_APP = True
        print(True)
        return True


def get_default_params():
    if globalvars.OLD_APP and globalvars.APP_DATA == False:
        with open(globalvars.appdata, 'r') as f:
            while True:
                line = f.readline().strip()
                print('From appdata.txt:', line)
                if not line:
                    break
                if 'log' in line[:4]:
                    globalvars.login = line.split(':')[1].strip()
                elif 'pas' in line[:4]:
                    globalvars.password = line.split(':')[1].strip()
                elif 'own' in line[:4]:
                    temp_owner = int(line.split(':')[1].strip())
                    if temp_owner > 0:
                        temp_owner = 0 - temp_owner 
                    if temp_owner not in globalvars.owner_list:
                        globalvars.owner_list.append(temp_owner)
                elif 'app' in line[:4]:
                    temp_app = int(line.split(':')[1].strip())
                    globalvars.app_id_list.append(temp_app)
        globalvars.APP_DATA = True
        return True
    else:
        globalvars.APP_DATA = False
        return False


def init_new_app(login, password, app_id:int, owner_id:int):
    if login == '' or password == '' or app_id == 0 or owner_id == 0:
        return False
    if globalvars.APP_DATA == False:
        print('Init new application:')
        with open(globalvars.appdata, 'w') as f:
            f.write('login:'+login+'\n')
            f.write('password:'+password+'\n')
            f.write('owner:'+str(owner_id)+'\n')
            f.write('appid:'+str(app_id)+'\n')
            print('  Login:', login)
            print('  Password:', password)
            print('  Owner id:', owner_id)
            print('  App id:', app_id)
    return True


def get_cach_ids():
    print('1.Given location:', os.getcwd())
    globalvars.cach_ids.clear()
    if os.path.isdir(globalvars.club):
        print('2.Given location:', os.getcwd())
        os.chdir(globalvars.club)
        print('3.Given location:', os.getcwd())
        if os.path.isfile(globalvars.club_ids):
            print('4.Given location:', os.getcwd())
            with open(globalvars.club_ids) as f:
                print('Read cach ods')
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    globalvars.cach_ids.append(line)
        else:
            return False
        os.chdir('..')
        print('5.Given location:', os.getcwd())
    else:
        return False
    if len(globalvars.cach_ids) > 0:
        globalvars.last_id = globalvars.cach_ids[-1]
    print('Last id:', globalvars.last_id)
    print('Id amount:', len(globalvars.cach_ids))
    return True


def set_paths_data():
    path_to_img = globalvars.img_path
    owner = str(abs(globalvars.owner_id))
    globalvars.club = 'club_'+owner
    os.makedirs(globalvars.club, exist_ok = True)
    globalvars.club_ids = 'cache_'+owner+'.txt'
    if path_to_img == '' or path_to_img == 'current':
        os.chdir(globalvars.club)
        globalvars.path_to_ids = os.getcwd()
        with open(globalvars.club_ids, 'a') as f:
            pass
        os.chdir('..')
        globalvars.img_path = globalvars.club
    else:
        os.chdir(globalvars.club)
        globalvars.path_to_ids = os.getcwd()
        with open(globalvars.club_ids, 'a') as f:
            pass
        os.chdir('..')
        globalvars.img_path = path_to_img+'/'
    

def save_img_and_id(url_img, id_img):
    req = requests.get(url_img)
    with open(globalvars.img_path+'/'+str(id_img)+'.jpg', 'wb') as f:
        print('Saving', str(id_img)+'.jpg', 'in', globalvars.img_path)
        f.write(req.content)
    if str(id_img) not in globalvars.cach_ids:
        print('Add id', id_img, 'to file')
        with open(globalvars.path_to_ids+'/'+globalvars.club_ids, 'a') as f:
            f.write(str(id_img)+'\n')
    #globalvars.image_cache.append(globalvars.img_path+'/'+str(id_img)+'.jpg')
    return globalvars.img_path+'/'+str(id_img)+'.jpg'


def save_temp_img(url, id_img):
    os.makedirs('tempimage', exist_ok = True)
    req = requests.get(url)
    with open('tempimage'+'/'+'tmp_'+str(id_img)+'.jpg', 'wb') as f:
        print('saving', 'tmp_'+str(id_img)+'.jpg', 'in a temporary folder')
        f.write(req.content)
    return 'tempimage'+'/'+'tmp_'+str(id_img)+'.jpg'
    
    
def delete_photo(img):
    print('Deleted', img)
    os.remove(img)






if __name__ == '__main__':
    pass



