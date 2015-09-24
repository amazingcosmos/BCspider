# -*- coding:utf-8 -*-

import ConfigParser
import BCspider

def find_popular_user(file_path = './data/user_basic_info.txt'):
    fp = open(file_path, 'r')
    seed_user = {}
    try:
        while True:
            line = fp.readline()
            if len(line) == 0:
                break
            elif line.count('\n') == len(line):
                continue
            else:
                user_info = eval(line)
                following_num = int(user_info['following'])
                followers_num = int(user_info['followers'])
                if followers_num > 1000 or following_num > 1000:
                    seed_user[user_info['username']] = [following_num, followers_num]
    finally:
        fp.close()
    return sorted(seed_user.iteritems(), key = lambda asd:asd[1][1], reverse = True)

