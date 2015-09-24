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


def get_basic():
    # a dict contains the user's infomation, once reach threshould, write file and clean.
    user_info = {}
    # a list contains used username, once reach threshould, write file and clean.
    user_done = []

    i = 1
    seed_num = len(seed_users)
    for seed in seed_users:
        # print seed
        print i, '/', seed_num
        following = BCspider.get_result(seed, task_type = 'following')
        followers = BCspider.get_result(seed, task_type = 'followers')
        total_user = followers + following
        total_user = list(set(total_user))
        total_num = len(total_user)
        j = 1
        for u in total_user:
            print 100.0 * j / total_num, '%'
            if not u in user_list:
                user_done.append(u)
                twitter_url = BCspider.get_twitter_url(u)
                if twitter_url != None:
                    user_list.append(u)
                    response = BCspider.get_basic_info(u, basic_task)
                    response['twitter'] = twitter_url
                    user_info[u] = response
            j = j + 1
            # save the buffer username and user_info to txt file 
            if len(user_info) > saving_threshold:
                BCspider.write_to_txt(user_done, user_done_path)
                BCspider.write_to_txt(user_info, basic_info_path)
                user_done = []
                user_info = {}
        i = i + 1
        print '\n'

    BCspider.write_to_txt(user_done, user_done_path)
    BCspider.write_to_txt(user_info, basic_info_path)


def get_detail():
    # a dict contains the user's infomation, once reach threshould, write file and clean.
    user_info = {}
    # a list contains used username, once reach threshould, write file and clean.
    user_done = []

    i = 1
    seed_num = len(seed_users)
    for seed in seed_users:
        # print seed
        print i, '/', seed_num
        following = BCspider.get_result(seed, task_type = 'following')
        followers = BCspider.get_result(seed, task_type = 'followers')
        total_user = followers + following
        total_user = list(set(total_user))
        total_num = len(total_user)
        j = 1
        for u in total_user:
            print 100.0 * j / total_num, '%'
            if not u in user_list:
                user_done.append(u)
                twitter_url = BCspider.get_twitter_url(u)
                if twitter_url != None:
                    user_list.append(u)
                    response = BCspider.get_basic_info(u, task)
                    response['twitter'] = twitter_url
                    user_info[u] = response
            j = j + 1
            # save the buffer username and user_info to txt file 
            if len(user_info) > saving_threshold:
                BCspider.write_to_txt(user_done, user_done_path)
                BCspider.write_to_txt(user_info, basic_info_path)
                user_done = []
                user_info = {}
        i = i + 1
        print '\n'

    BCspider.write_to_txt(user_done, user_done_path)
    BCspider.write_to_txt(user_info, basic_info_path)