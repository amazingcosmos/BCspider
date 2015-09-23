# -*- coding:utf-8 -*-

import ConfigParser
import BCspider

if __name__ == '__main__':
    fp = open('./data/user_basic_info.txt', 'r')
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
    print sorted(seed_user.iteritems(), key = lambda asd:asd[1][1], reverse = True)

