# -*- coding:utf-8 -*-

import ConfigParser
import BCspider

def find_popular_user(file_path = './data/user_basic_info.txt'):
    fp = open(file_path, 'r')
    users = []
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
                discussions_num = int(user_info['discussions'])
                if followers_num > 3 and following_num > 3 and discussions_num > 0:
                    line = user_info['username'] + '$||$' + user_info['twitter']
                    users.append(line)
    finally:
        fp.close()
    return users

def get_username(file_path = './data/user_basic_info.txt'):
    fp = open(file_path, 'r')
    username = []
    try:
        while True:
            line = fp.readline()
            if len(line) == 0:
                break
            elif line.count('\n') == len(line):
                continue
            else:
                user_info = eval(line)
                name = user_info['username']
                username.append(name)
    finally:
        fp.close()
    BCspider.write_to_txt(username, './data/user_todo.txt')


if __name__ == '__main__':
    # user_todo = find_popular_user()
    # # print len(user_todo)
    # BCspider.write_to_txt(user_todo, './data/user_todo.txt')

