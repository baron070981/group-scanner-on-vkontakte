#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from tkinter import messagebox
import time
from pprint import pprint


import displayvk
import datavk
import globalvars
import fileprocc


ACTION = True
STOPED = False
STOP_SCAN = False
DATA_LIST_BOOL = False # 
count_step = 0 # 
URL = None
ID = None


#
vk = datavk.VkData()
# создание главного окна приложения
root = displayvk.MainWindow()

# получение данных для приложения
def get_data_application():
    global root
    # получение данных из виджетов(логин,пароль и т.п.)
    root.get_appdata_from_widgets()
    # создание необходимых файлов и директорий, определение путей до них
    fileprocc.set_paths_data()
    # загрузка списка id из файла
    fileprocc.get_cach_ids()
    # определение режима исполнения
    root.performance_mode_selection()


# 
def step_to_next(limit_iter, data_list):
    global ACTION
    print(data_list[globalvars.iter_count])
    globalvars.iter_count += 1
    
    if globalvars.iter_count > limit_iter:
        globalvars.iter_count = 0
    

# сохранение фото при нажатии на кнопку save
def saving(event):
    global URL
    global ID
    global ACTION
    if not ACTION:
        return
    fileprocc.save_img_and_id(URL, ID)
    

# переход к следующему фото при нажатии кнопки next
def next_image(event):
    global vk
    global DATA_LIST_BOOL
    global count_step
    global URL
    global ID
    global ACTION
    
    if ACTION == False:
        globalvars.manual = False
        # root.start_btn.grid()
        # root.subwindow.destroy()
        return
    
    if DATA_LIST_BOOL == False:    # если можно получить данные из api
        # получение списка url и id
        vk.get_data_from_group(globalvars.offset, globalvars.count_posts)
        globalvars.offset += globalvars.count_posts
        DATA_LIST_BOOL = True
        
    if vk.GROUP_DATA:
        if count_step >= len(vk.urls_ids):
            count_step = 0
            DATA_LIST_BOOL = False
            
        url = vk.urls_ids[count_step][1]
        _id = vk.urls_ids[count_step][0]
        count_step += 1
        URL = url
        ID = _id
        img = fileprocc.save_temp_img(url, _id)
        root.show_photo(img)
        fileprocc.delete_photo(img)
        
    

def stop_action(event):
    global root
    global vk
    global STOP_SCAN
    global ACTION
    STOP_SCAN = True
    ACTION = False
    root.start_btn.grid()
    if root.subwindow != None:
        root.subwindow.destroy()
    vk.urls_ids.clear()
    print('Stop scan:', STOP_SCAN)
    print('Action:', ACTION)


def action(event):
    global STOPED
    global STOP_SCAN
    global ACTION
    ACTION = True
    STOP_SCAN = False
    get_data_application()
    if globalvars.APP_DATA:
        vk.init_app_data(globalvars.login, globalvars.password,
                         globalvars.app_id, globalvars.owner_id)
        vk.init_api()
        print(vk.api)
        
    if vk.INIT_API:
        root.create_subwindow(370,10)
        root.start_btn.grid_remove()
        
        if globalvars.manual:
            if ACTION == True:
                root.next_btn.bind('<Button 1>', next_image)
                root.save_btn.bind('<Button 1>', saving)
            else:
                messagebox.showinfo('info', 'STOPED')
                
        
        elif globalvars.auto:
            globalvars.image_cache.clear()
            
            while True:
                time.sleep(.400)
                if globalvars.offset >= 1000:
                    messagebox.showinfo('info', 'Offset limit')
                    root.start_btn.grid()
                    root.subwindow.destroy()
                    break
                
                vk.get_data_from_group(globalvars.offset, globalvars.count_posts)
                if len(vk.urls_ids) == 0:
                    messagebox.showinfo('info', 'not data vk')
                    root.start_btn.grid()
                    root.subwindow.destroy()
                    break
                    
                if STOPED:
                    messagebox.showinfo('info', 'not new images or end get data')
                    root.start_btn.grid()
                    root.subwindow.destroy()
                    STOPED = False
                    break
                    
                if STOP_SCAN:
                    messagebox.showinfo('info', 'stoped')
                    root.start_btn.grid()
                    root.subwindow.destroy()
                    STOP_SCAN = False
                    break
                    
                for data in vk.urls_ids:
                    #time.sleep(.70)
                    if STOP_SCAN:
                        break
                        
                    print(data)
                    url = data[1]
                    _id = data[0]
                    img = fileprocc.save_img_and_id(url, _id)
                    
                    if img in globalvars.image_cache:
                        STOPED = True
                        break
                        
                    globalvars.image_cache.append(img)
                    root.show_photo(img)
                    if not globalvars.save_img:
                        fileprocc.delete_photo(img)
                        
                globalvars.offset += globalvars.count_posts

        globalvars.offset = 0







if __name__ == '__main__':

    # проверка наличия файла appdata.txt
    fileprocc.check_appdata()

    # если файл существует
    if globalvars.OLD_APP:
        # получение данных из файла
        fileprocc.get_default_params()
    if globalvars.APP_DATA:
        # заполнение виджетов значениями из файла
        root.set_default_params()
    
    
    root.start_btn.bind('<Button 1>', action)
    root.stop_btn.bind('<Button 1>', stop_action)
    
    
    
    
    root.mainloop()




