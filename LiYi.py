#-*- coding:utf-8 -*-
""" 
This file used as a control center, if you put some 'seed users',
it will search their friends and followers.
Authors: Alex Lee(amazingcosmos@163.com) 
Date: 2015/09/22 14:19:06 
"""

import BCspider
import os
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('BCspider.conf')
# define the task you want to be taken this time.
basic_task = list(eval(cf.get("basic", "basic_task")))
# define how many people gathered is the time to save info to txt.
saving_threshold = int(cf.get("basic", "saving_threshold"))
# define the seed user
seed_users = list(eval(cf.get("basic", "seed_users")))

# build up the path of txt file
file_path = os.getcwd() + '\\data\\'
if not os.path.exists(file_path):
    os.mkdir(file_path)
basic_info_path = file_path + 'user_basic_info.txt'
user_done_path = file_path + 'user_done.txt'

# get the list of used username
user_list = BCspider.read_from_txt(user_done_path)





