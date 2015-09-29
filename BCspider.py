#-*- coding:utf-8 -*-
""" 
This module provide method to get twitter, following, followers, discussions info in www.blogcatalog.com 
Authors: Alex Lee(amazingcosmos@163.com) 
Date: 2015/09/26 17:19:06 
"""

import urllib2
import re
import types
from bs4 import BeautifulSoup
import os
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read('./BCspider.conf')
# the website's url
url = cf.get('basic','url')
# the infomation about the different tasks, contain the key html element.
task_info = {}
task_info['following'] = dict(cf.items('following'))
task_info['followers'] = dict(cf.items('followers'))
task_info['discussions'] = dict(cf.items('discussions'))
# define how many people gathered is the time to save info to txt.
saving_threshold = int(cf.get("basic", "saving_threshold"))
# define the seed user
seed_users = list(eval(cf.get("basic", "seed_users")))
# define where to store the data file.
file_path = os.getcwd()
if not os.path.exists(file_path + '/data/'):
    os.mkdir(file_path + '/data/')


def read_from_txt(file_path, split_char, split_index):
    """read a list from txt 

    In the file, there are lines of data. The program split the line by split_char.
    get the string u want in split_index and store it into a list and then return this list.

    Args:
        file_path: the file to be extracted.
        split_char: the specific char used to split the line.
        split_index: the index of the string after splitted.

    Returns:
        result: a list contains the data in file.
    """
    result = []
    try:
        fp = open(file_path, 'r')
        try:
            while True:
                line = fp.readline()[:-1]
                if len(line) == 0:
                    break
                elif line.count('\n') == len(line):
                    continue
                elif split_index == 'all':
                    line = line.split(split_char)
                    result += line 
                else:
                    line = line.split(split_char)[split_index].encode('utf-8')
                    result.append(line)
        finally:
            fp.close()
    except IOError:
        print("fail to open file")
    return result


def write_to_txt(data, file_path):
    """Write data to a txt file.

    Write a list/dict/string to a txt file, with each item occupy a line.

    Args:
        data: the list_obj you want to write to the file.
        file_path: the path of the file.

    Returns:
        None
    """
    if data == None:
        fp = open(file_path, 'a')
        fp.close()
    else:
        try:
            fp = open(file_path, 'a')
            try:
                if type(data) is types.ListType:
                    for item in data:
                        fp.write(str(item) + '\n')
                elif type(data) is types.DictType:
                    for item in data:
                        fp.write(str(data[item]) + '\n')
                elif type(data) is types.StringType:
                    fp.write(data + '\n')
                print("write file success")
            finally:
                fp.close()
        except IOError:
            print("fail to open file")


def get_soup(url):
    """Fetch the BeautifulSoup object from a url

    Args:
        url: The makeup url you want to deal with.

    Returns:
        soup: BeautifulSoup object
    """
    soup = None

    try:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html.read(), "html.parser")
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request"
        print "Error code:", e.code
        # print "Return content:", e.read()
    except urllib2.URLError, e:
        print "Failed to reach the server"
        print "The reason:", e.reason

    return soup


def get_twitter_url(username):
    """find the user's twitter page in blogcatalog's bio page.

    There is a twitter link button on user's bio page. To detect 
    if this button is exist, we can find the twitter link in it.

    Args:
        username: the blogcatalog username you want to find.

    Returns:
        twitter_url: user's twitter homepage url.
    """
    bio_url = url + 'user/' + username + '/bio/'
    soup = get_soup(bio_url)

    if soup == None:
        return ""
    try:
        bc_service_img = soup.find_all('td', 'bc_service_img')

        for img in bc_service_img:
            href = img.find('a', href=re.compile("twitter"))
            if href:
                twitter_url = href['href'].encode('utf-8')
                return twitter_url
    except:
        print 'get twitter error'
    return ""


def get_page_content(url, task_type):
    """Get the content you want to find in a page according to the task type.

    With three kinds of task type: following, followers, discussions, there are two
    different strategys. On the head of this module I define a dict named task_info,
    which contains the variables needed to deal with different task. Then, the program
    will search the html code to find the content you want.

    Args:
        url: The string url needed to be processed.
        task_type: the type of the task.

    Returns:
        content: a string store all the result on this url's page. 
    """
    content = ""
    error_str = 'get %s error'
    content_class = task_info[task_type]['content_class']
    soup = get_soup(url)

    if soup == None:
        return ""

    if task_type == 'following' or task_type == 'followers':
        try:
            soup = soup.find('div', class_ = 'page_column_568')
            c_list = soup.find('ul', class_ = content_class)
            c_list = c_list.find_all('p', string = True)
        except:
            print error_str % task_type
        else:
            for friend in c_list:
                name = friend.string
                content = content + name + '$||$'
        if len(content) > 0:
            content = content[:-4]
    elif task_type == 'discussions':
        try:
            soup = soup.find('div', class_ = 'page_column_568')
            c_list = soup.find_all('div', class_ = content_class)
        except:
            print error_str % task_type
        else:
            for thread in c_list:
                try:
                    thread_url = thread.find('h3').find('a')['href']
                    thread_url = 'http://www.blogcatalog.com' + thread_url
                    thread_title = thread.find('h3').find('a').string.replace("\n", "")
                    thread_comment_num = thread.find('h5').find('a').string
                    thread_comment_num = thread_comment_num.split(' ')[0][1:]
                except:
                    print error_str % task_type
                else:
                    line = thread_title + '$||$' + thread_url + '$||$' + thread_comment_num
                    content = content + line + '\n'
        if len(content) > 0:
            content = content[:-1]
    return content.encode('utf-8')


def get_basic_info(username):
    """get a user's basic info depended on what task u want to take.

    We can gather the user's basic infomation on the user's homepage. There 
    is a 'profile_nav' button area, showing how many blogs, reading, following,
    followers, discussions. The twitter_url is gathered by func get_twitter_url.
    Username is the defalt info.
    data structure:
        username$||$twitter_url$||$follower_num$||$following_num$||$blog_num$||$reading_num$||$discussions_num

    Args:
        username: the username to be searched.

    Returns:
        result: string stored the user info result.
    """
    result = ""
    error_str = 'get %s error'
    homepage = url + 'user/' + username + '/discussions/'
    soup = get_soup(homepage)
    if soup == None:
        return ""

    result += username + '$||$'
    try:
        profile = soup.find('div', id = 'profile_nav')
    except:
        print error_str % 'profile'

    twitter_url = get_twitter_url(username)
    result += twitter_url + '$||$'

    try:
        followers = profile.find('a', 'followers_button rounded_4')
        followers_num = followers.find('div', class_ = 'button_count').string.encode('utf-8')
        result += followers_num + '$||$'
    except:
        print error_str % 'followers'

    try:
        following = profile.find('a', 'following_button rounded_4')
        following_num = following.find('div', class_ = 'button_count').string.encode('utf-8')
        result += following_num + '$||$'
    except:
        print error_str % 'following'
    
    try:
        blog = profile.find('a', 'blog_button rounded_4')
        blog_num = blog.find('div', class_ = 'button_count').string.encode('utf-8')
        result += blog_num + '$||$'
    except:
        print error_str % 'blog'
    
    try:
        reading = profile.find('a', 'favs_button rounded_4')
        reading_num = reading.find('div', class_ = 'button_count').string.encode('utf-8')
        result += reading_num + '$||$'
    except:
        print error_str % 'reading'
    
    try:
        discussions = profile.find('a', 'discussions_button rounded_4')
        discussions_num = discussions.find('div', class_ = 'button_count').string.encode('utf-8')
        result += discussions_num + '$||$'
    except:
        print error_str % 'discussions'
    
    result = result[:-4]
    return result.encode('utf-8')


def get_detail_info(username, task_type):
    """get specific detail info of a blogcatalog user.

    On the homepage of a user, the program analysis page's source code.
    Get the number of a type(following, followers, discussions) and count 
    how many pages it has to search. It sends each page's url to the 
    get_page_content function and get info returned.

    Args:
        username: blogcatalog username.
        task_type: the type of the task.

    Returns:
        result: a string contains all the data you want to get from a user.
                the followers/following name will be split by '$||$'
                the discussion data's each line is a thread(title$||$url$||$comment_num)
    """
    # init the local variable according to the task type
    task_url = url + 'user/' + username + task_info[task_type]['task_url']
    page_capacity = int(task_info[task_type]['page_capacity'])
    button_a_class = task_info[task_type]['button_a_class']
    button_div_class = task_info[task_type]['button_div_class']

    result = "" 
    # get the number of task_type
    soup = get_soup(task_url)
    if soup == None:
        return ""
    try:
        button = soup.find('a', class_ = button_a_class)
        button_count = button.find('div', class_ = button_div_class)
        num_task = int(button_count.string.extract())
    except:
        print 'get num_task error'
    if num_task > page_capacity:
        num_page = num_task / page_capacity + 1
        response = get_page_content(task_url, task_type)
        if response != None:
            result += response
        for i in range(2, num_page + 1):
            # print 100.0 * i / num_page, "%"
            response = get_page_content(task_url + str(i), task_type)
            if response != None:
                result += response
    elif num_task > 0:
        response = get_page_content(task_url,task_type)
        if response != None:
            result += response
    # result += get_page_content(task_url,task_type)
    print task_type, 'done!'
    return result.encode('utf-8')


def get_info(work_dir):
    """get all user's info in a user_todo.txt

    This module first get a list of user_todo and user_done. With the list, it 
    traversal the user_todo list and compare the user_done to find which user
    to get info. The program will setup a 'data' folder and store each user's 
    info as a txt file named by 'username.txt'. At the same time, it will save 
    the username done before to 'user_done.txt', and the next layer username to 
    'user_next.txt'.

    Args:
        work_dir: the dir of the program.

    Returns:
        None 
    """
    user_done_path = work_dir + '/filter/' + 'user_done.txt'
    user_todo_path = work_dir + '/filter/' + 'user_todo.txt'
    user_next_path = work_dir + '/filter/' + 'user_next.txt'
    # a list contains used username.
    user_done = read_from_txt(user_done_path, ' ', 0)
    # a list contains the username to be done.
    user_todo = read_from_txt(user_todo_path, ' ', 0)

    i = 1
    user_num = len(user_todo)
    for username in user_todo:
        print i, '/', user_num
        if not username in user_done:
            user_info = ""
            user_file_path = work_dir + '/data/' + username + '.txt'
            basic_info = get_basic_info(username)
            followers = get_detail_info(username, task_type = 'followers')
            following = get_detail_info(username, task_type = 'following')
            discussions = get_detail_info(username, task_type = 'discussions')
            user_info += basic_info + '\n' + followers + '\n' + following + '\n' + discussions
            write_to_txt(user_info, user_file_path)
            write_to_txt(username, user_done_path)
            write_to_txt(followers + '$||$' + following, user_next_path)
        i = i + 1
    return 1


def test():
    """test this module

    Test whether this module's most function woring well
    """
    print get_twitter_url('TonyB')

    print get_basic_info('TonyB')

    if not os.path.exists(file_path + '/test/'):
        os.mkdir(file_path + '/test/')

    username = 'timethief'
    following = get_detail_info(username, task_type = 'following')
    write_to_txt(following, file_path + '/test/' + str(username) + '_following.txt')
    print str(username), 'following finished!'
    followers = get_detail_info(username, task_type = 'followers')
    write_to_txt(followers, file_path + '/test/' + str(username) + '_followers.txt')
    print str(username), 'followers finished!'
    discussions = get_detail_info(username, task_type = 'discussions')
    write_to_txt(discussions, file_path + '/test/' + str(username) + '_discussions.txt')
    print str(username), 'discussions finished!'
    

if __name__ == '__main__':
    # test()
    get_info(file_path)
    print 'finish!\n'
