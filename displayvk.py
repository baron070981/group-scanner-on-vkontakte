#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.ttk as ttk
import os
import os.path
import requests
import time
from tkinter import messagebox
import re
import sys


import globalvars
import fileprocc


class MainWindow(tk.Tk):
    
    def __init__(self, bg ='#000000'):
        self.appid_list = list()
        self.owner_list = list()
        
        super(MainWindow, self).__init__()
        
        self.bool_check_save = tk.BooleanVar()
        self.bool_check_mode = tk.BooleanVar()
        self.bool_check_show = tk.BooleanVar()
        self.bool_check_save.set(0)
        self.bool_check_mode.set(1)
        self.bool_check_show.set(1)
        self.geometry('+10+10')
        self.title('Scanning VKontakte')
        
        self.subwindow = None
        
        # init widgets
        # login, password, app_id, owner_id, count_posts
        self.input_frame = tk.Frame(self)
        self.login_label = tk.Label(self.input_frame, text = 'login')
        self.login_entry = tk.Entry(self.input_frame)
        
        self.pass_label = tk.Label(self.input_frame, text = 'password')
        self.pass_entry = tk.Entry(self.input_frame)
        
        self.appid_label = tk.Label(self.input_frame, text = 'application id')
        self.appid_combo = ttk.Combobox(self.input_frame, values = globalvars.app_id_list, height = 3)
        
        self.owner_label = tk.Label(self.input_frame, text = 'group id')
        self.owner_combo = ttk.Combobox(self.input_frame, values = globalvars.owner_list, height = 3)
        
        self.posts_label = tk.Label(self.input_frame, text = 'count posts')
        self.posts_entry = tk.Entry(self.input_frame)
        self.path_label = tk.Label(self.input_frame, text = 'path images')
        self.path_entry = tk.Entry(self.input_frame)
        
        # control widgets
        self.control_frame = tk.Frame(self)
        self.save_check = tk.Checkbutton(self.control_frame, text = 'with preservation',
                                         variable = self.bool_check_save)
        self.mode_check = tk.Checkbutton(self.control_frame, text = 'manual',
                                         variable = self.bool_check_mode)
        self.show_check = tk.Checkbutton(self.control_frame, text = 'show',
                                         variable = self.bool_check_show)
        
        self.start_btn = tk.Button(self.control_frame, text = 'start')
        self.save_btn = tk.Button(self.control_frame, text = 'save')
        self.next_btn = tk.Button(self.control_frame, text = 'next')
        self.stop_btn = tk.Button(self.control_frame, text = 'stop')
        
        
        #setting positions widgets
        self.input_frame.pack()
        self.control_frame.pack()
        self.login_label.grid(row=0, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.login_entry.grid(row=0, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.pass_label.grid(row=1, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.pass_entry.grid(row=1, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.appid_label.grid(row=2, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.appid_combo.grid(row=2, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.owner_label.grid(row=3, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.owner_combo.grid(row=3, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.posts_label.grid(row=4, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.posts_entry.grid(row=4, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.path_label.grid(row=5, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.path_entry.grid(row=5, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        
        self.save_check.grid(row=0, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.mode_check.grid(row=0, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.show_check.grid(row=0, column=2, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        
        self.start_btn.grid(row=1, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.save_btn.grid(row=1, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.next_btn.grid(row=1, column=2, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.stop_btn.grid(row=1, column=3, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        
        self.panel = None
        
        
        
        #self.mode_check.select()
        

    
    # class methods
    
    
    def performance_mode_selection(self):
        
        state_mode = self.bool_check_mode.get()
        if state_mode:
            self.bool_check_save.set(0)
            self.bool_check_show.set(1)
            globalvars.manual = True
            globalvars.auto = False
            globalvars.show_bool = True
            globalvars.save_img = False
        else:
            globalvars.auto = True
            globalvars.manual = False
        
        state_show = self.bool_check_show.get()
        if state_show:
            globalvars.show_bool = True
        else:
            globalvars.show_bool = False
        
        state_save = self.bool_check_save.get()
        if state_save:
            globalvars.save_img = True
        else:
            globalvars.save_img = False
        print('State mode:', state_mode, 'State save:', state_save)
        print('Auto:', globalvars.auto, 'Manual:', globalvars.manual, 'Save:', globalvars.save_img)
        
    
    
    def get_appdata_from_widgets(self):
        login = self.login_entry.get().strip()
        password = self.pass_entry.get().strip()
        owner = self.owner_combo.get()
        appid = self.appid_combo.get()
        globalvars.img_path = self.path_entry.get()
        if login == '' or password == '' or owner == '' or appid == '':
            messagebox.showinfo('Info', 'один из параметров пустой')
            return False
        globalvars.login = login
        globalvars.password = password
        try:
            globalvars.count_posts = int(self.posts_entry.get())
            globalvars.owner_id = int(owner)
            globalvars.app_id = int(appid)
            if globalvars.app_id not in globalvars.app_id_list:
                with open(globalvars.appdata, 'a') as f:
                    f.write('appid:'+str(globalvars.app_id)+'\n')
            if globalvars.owner_id not in globalvars.owner_list:
                with open(globalvars.appdata, 'a') as f:
                    f.write('owner:'+str(globalvars.owner_id)+'\n')
            globalvars.app_id_list.append(globalvars.app_id)
            globalvars.owner_list.append(globalvars.owner_id)
            
        except:
            messagebox.showerror('error', 'не корректный ввод')
            return False
        return True
    

    
    def set_default_params(self):
        self.login_entry.insert(0, globalvars.login)
        self.pass_entry.insert(0, globalvars.password)
        self.appid_combo['values'] = globalvars.app_id_list
        self.owner_combo['values'] = globalvars.owner_list
        self.appid_combo.set(value = globalvars.app_id_list[0])
        self.owner_combo.set(value = globalvars.owner_list[0])
        self.posts_entry.insert(0, '99')
        self.path_entry.insert(0, 'current')

    
    def create_subwindow(self, posx = 1, posy = 1):
        self.subwindow = tk.Toplevel()
        self.subwindow.title('images')
        self.subwindow.geometry('+{}+{}'.format(posx, posy))
        self.panel = tk.Label(self.subwindow)
        self.panel.pack()
    
    
    def set_image_size(self, width, height, set_size):
        if width > height:
            delta = width / height
            width = set_size
            height = set_size / delta
        elif height > width:
            delta = height / width
            height = set_size
            width = set_size / delta
        elif height == width:
            height = set_size
            width = set_size
        else:
            width = 100
            height = 100
        return int(width), int(height)
    
    
    def show_photo(self, img_path):
        #size_img = (200,200)
        image_original = Image.open(img_path)
        width, height = image_original.size
        size_img = self.set_image_size(width, height, 400)
        resized = image_original.resize(size_img, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.panel.configure(image = self.image)
        self.panel.image = self.image
        self.panel.update()







if __name__ == '__main__':
    root = MainWindow()
    
    root.start_btn.bind('<Button 1>', root.check_processing)
    
    root.mainloop()


