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
cf.read('LiYi.conf')
# define the task you want to be taken this time.
task = list(eval(cf.get("BC", "task")))
# define how many people gathered is the time to save info to txt.
saving_threshold = int(cf.get("BC", "saving_threshold"))
# define the seed user
seed_users = list(eval(cf.get("BC", "seed_users")))

# build up the path of txt file
filepath = os.getcwd() + '\\data\\'
if not os.path.exists(filepath):
    os.mkdir(filepath)
info_txt_path = filepath + 'user_basic_info.txt'
username_txt_path = filepath + 'username.txt'

# get the list of used username
user_list = []
try:
    if os.path.exists(username_txt_path):
        fp = open(username_txt_path, 'r')
        try:
            while True:
                line = fp.readline()[:-1]
                if len(line) == 0:
                    break
                elif line.count('\n') == len(line):
                    continue
                else:
                    user_list.append(line)
        finally:
            fp.close()
    else:
        user_list = []
except IOError:
    print("fail to open file")

# print type(task), task
# print type(saving_threshold), saving_threshold
# print type(seed_users), seed_users
# print user_list


if __name__ == '__main__':
    # a dict contains the user's infomation, once reach threshould, write file and clean.
    user_info = {}
    # a list contains used username, once reach threshould, write file and clean.
    username_temp = []


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
                username_temp.append(u)
                twitter_url = BCspider.get_twitter_url(u)
                if twitter_url != None:
                    user_list.append(u)
                    response = BCspider.get_basic_info(u, task)
                    response['twitter'] = twitter_url
                    user_info[u] = response
            j = j + 1
            # save the buffer username and user_info to txt file 
            if len(user_info) > saving_threshold:
                BCspider.write_to_txt(username_temp, username_txt_path)
                BCspider.write_to_txt(user_info, info_txt_path)
                username_temp = []
                user_info = {}
        i = i + 1
        print '\n'

    BCspider.write_to_txt(username_temp, username_txt_path)
    BCspider.write_to_txt(user_info, info_txt_path)