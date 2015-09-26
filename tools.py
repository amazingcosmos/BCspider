# -*- coding:utf-8 -*-

import ConfigParser
import BCspider
import sys


def get_user(file_path , index_from, index_to):
    """
    """
    user_todo = BCspider.read_from_txt(file_path + 'filter.txt', '$||$', 0)[index_from:index_to]
    BCspider.write_to_txt(user_todo, file_path + 'user_todo.txt')


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


def count_user(file_path = './data/user_next.txt'):
    total_user = []
    users = BCspider.read_from_txt(file_path)
    for line in users:
        total_user += line.split('$**$')
        total_user = list(set(total_user))
    return len(total_user)

if __name__ == '__main__':
    # user_num = count_user('./data/user_next.txt')
    # print 'the number of next layer user is:', user_num, '\n'
    # sys.exit(1)
    # user_todo = find_popular_user()
    # # print len(user_todo)
    # BCspider.write_to_txt(user_todo, './data/user_todo.txt')

    get_user('./filter/', 3, 13)

