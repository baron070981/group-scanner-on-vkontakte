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


class MainWindow(tk.Tk):
    
    def __init__(self, bg ='#000000'):
        self.appid_list = list()
        self.owner_list = list()
        
        super(MainWindow, self).__init__()
        
        self.bool_check_save = tk.BooleanVar()
        self.bool_check_mode = tk.BooleanVar()
        self.bool_check_save.set(0)
        self.bool_check_mode.set(1)
        self.geometry('+10+10')
        # init widgets
        # login, password, app_id, owner_id, count_posts
        self.input_frame = tk.Frame(self)
        self.login_label = tk.Label(self.input_frame, text = 'login')
        self.login_entry = tk.Entry(self.input_frame)
        
        self.pass_label = tk.Label(self.input_frame, text = 'password')
        self.pass_entry = tk.Entry(self.input_frame)
        
        self.appid_label = tk.Label(self.input_frame, text = 'application id')
        self.appid_combo = ttk.Combobox(self.input_frame, values = self.appid_list, height = 3)
        
        self.owner_label = tk.Label(self.input_frame, text = 'group id')
        self.owner_combo = ttk.Combobox(self.input_frame, values = self.owner_list, height = 3)
        
        self.posts_label = tk.Label(self.input_frame, text = 'count posts')
        self.posts_entry = tk.Entry(self.input_frame)
        
        # control widgets
        self.control_frame = tk.Frame(self)
        self.save_check = tk.Checkbutton(self.control_frame, text = 'with preservation',
                                         variable = self.bool_check_save)
        self.mode_check = tk.Checkbutton(self.control_frame, text = 'auto/manual',
                                         variable = self.bool_check_mode)
        
        self.start_btn = tk.Button(self.control_frame, text = 'scaning')
        self.save_btn = tk.Button(self.control_frame, text = 'save')
        self.next_btn = tk.Button(self.control_frame, text = 'next')
        
        
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
        
        self.save_check.grid(row=0, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.mode_check.grid(row=0, column=1, columnspan=2, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        
        self.start_btn.grid(row=1, column=0, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.save_btn.grid(row=1, column=1, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        self.next_btn.grid(row=1, column=2, pady=5, padx=5, sticky='w'+'s'+'n'+'e')
        
        
        
        #self.mode_check.select()
        

    
    # class methods
    
    def check_processing(self, event):
        
        state_mode = self.bool_check_mode.get()
        if state_mode:
            self.bool_check_save.set(0)
            print('auto')
        else:
            print('manual')
        state_save = self.bool_check_save.get()
        if state_save:
            print('save')
        else:
            print('no save')
    
    
    def get_data_from_widget(self):
        pass
        
    
    def set_default_params(self):
        if not os.path.isfile(globvars.appdata):
            return False
        









if __name__ == '__main__':
    root = MainWindow()
    
    root.start_btn.bind('<Button 1>', root.check_processing)
    
    root.mainloop()


