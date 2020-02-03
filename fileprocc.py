import sys
import os
import os.path




import globalvars


#APP_DATA = False



def get_default_params():
    if not os.path.isfile(globalvars.appdata):
        globalvars.APP_DATA = False
        return False
    with open(globalvars.appdata, 'r') as f:
        while True:
            line = f.readline().strip()
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
                globalvars.owner_list.append(temp_owner)
            elif 'app' in line[:4]:
                temp_app = int(line.split(':')[1].strip())
                globalvars.app_id_list.append(temp_app)
    globalvars.APP_DATA = True
    return True


def init_new_app(login, password, owner_id, app_id):
    if globalvars.APP_DATA == False:
        with open(globalvars.appdata, 'w') as f:
            f.write('login:'+login+'\n')
            f.write('password:'+password+'\n')
            f.write('owner:'+)

    










if __name__ == '__main__':
    pass



