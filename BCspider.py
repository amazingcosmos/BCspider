#-*- coding:utf-8 -*-
""" 
This module provide method to get twitter, following, followers, discussions info in www.blogcatalog.com 
Authors: Alex Lee(amazingcosmos@163.com) 
Date: 2015/09/23 11:19:06 
"""

import urllib2
import re
import types
from bs4 import BeautifulSoup
import os
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('BCspider.conf')
# the website's url
url = cf.get('basic','url')
# the infomation about the different tasks, contain the key html element.
task_info = {}
task_info['following'] = dict(cf.items('following'))
task_info['followers'] = dict(cf.items('followers'))
task_info['discussions'] = dict(cf.items('discussions'))
# define the task you want to be taken this time.
basic_task = list(eval(cf.get("basic", "basic_task")))
# define how many people gathered is the time to save info to txt.
saving_threshold = int(cf.get("basic", "saving_threshold"))
# define the seed user
seed_users = list(eval(cf.get("basic", "seed_users")))
# define where to store the data file.
file_path = os.getcwd() + '\\data\\'
if not os.path.exists(file_path):
    os.mkdir(file_path)
if not os.path.exists(file_path + 'info\\'):
    os.mkdir(file_path + 'info\\')
basic_info_path = file_path + 'user_basic_info.txt'
user_done_path = file_path + 'user_done.txt'


def read_from_txt(file_path):
    result = []
    try:
        if os.path.exists(file_path):
            fp = open(file_path, 'r')
            try:
                while True:
                    line = fp.readline()[:-1]
                    if len(line) == 0:
                        break
                    elif line.count('\n') == len(line):
                        continue
                    else:
                        result.append(line)
            finally:
                fp.close()
        else:
            result = []
    except IOError:
        print("fail to open file")
    return result


def write_to_txt(data, file_path):
    """Write a list to a txt file.

    Write a list/dict to a txt file, with each item occupy a line.

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
                for item in data:
                    if type(data) is types.ListType:
                        fp.write(str(item) + '\n')
                    if type(data) is types.DictType:
                        fp.write(str(data[item]) + '\n')
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
        return None

    bc_service_img = soup.find_all('td', 'bc_service_img')

    for img in bc_service_img:
        href = img.find('a', href=re.compile("twitter"))
        if href:
            twitter_url = href['href'].encode('utf-8')
            return twitter_url
    return None


def get_page_content(url, task_type):
    """Get the content you want to find in a page according to the task type.

    With three kinds of task type: following, followers, discussions, there are two
    different strategys. On the head of this module I define a dict named task_info,
    which contains the variables we need to deal with different task. Then, the program
    will search the html code to find the content you need.

    Args:
        url: The string url needed to be processed.
        task_type: the type of the task.

    Returns:
        content: a list store all the result on this url's page. 
    """
    content = []
    content_class = task_info[task_type]['content_class']
    soup = get_soup(url)

    if soup == None:
        return None

    if task_type == 'following' or task_type == 'followers':
        soup = soup.find('div', class_ = 'page_column_568')
        c_list = soup.find('ul', class_ = content_class)
        c_list = c_list.find_all('p', string = True)

        for friend in c_list:
            name = friend.string.extract().encode("utf-8")
            content.append(name)
    elif task_type == 'discussions':
        soup = soup.find('div', class_ = 'page_column_568')
        c_list = soup.find_all('div', class_ = content_class)

        for thread in c_list:
            thread_url = thread.find('h3').find('a')['href']
            thread_url = 'http://www.blogcatalog.com' + thread_url
            content.append(thread_url)
    return content


def get_basic_info(username, task_type):
    """get a user's basic info depended on what task u want to take.

    We can gather the user's basic infomation on the user's homepage. There 
    is a 'profile_nav' button area, showing how many blogs, reading, following,
    followers, discussions. The twitter can be wrote the result if task contains.
    Username is the defalt info.

    Args:
        username: the username to be searched.
        task_type: dict contains what info wanted.

    Returns:
        result: dict stored the user info result.
    """
    result = {}

    homepage = url + 'user/' + username
    soup = get_soup(homepage)
    if soup == None:
        return None 

    profile = soup.find('div', id = 'profile_nav')
    if 'blog' in task_type:
        blog = profile.find('a', 'blog_button rounded_4')
        blog_num = int(blog.find('div', class_ = 'button_count').string.extract())
        result['blog'] = blog_num
    if 'following' in task_type:
        following = profile.find('a', 'following_button rounded_4')
        following_num = int(following.find('div', class_ = 'button_count').string.extract())
        result['following'] = following_num
    if 'followers' in task_type:
        followers = profile.find('a', 'followers_button rounded_4')
        followers_num = int(followers.find('div', class_ = 'button_count').string.extract())
        result['followers'] = followers_num
    if 'reading' in task_type:
        reading = profile.find('a', 'favs_button rounded_4')
        reading_num = int(reading.find('div', class_ = 'button_count').string.extract())
        result['reading'] = reading_num
    if 'discussions' in task_type:
        discussions = profile.find('a', 'discussions_button rounded_4')
        discussions_num = int(discussions.find('div', class_ = 'button_count').string.extract())
        result['discussions'] = discussions_num
    if 'twitter' in task_type:
        twitter_url = get_twitter_url(username)
        result['twitter'] = twitter_url
    result['username'] = username

    return result


def get_detail_info(username, task_type):
    """Process a specific task of a blogcatalog user.

    On the homepage of a user, the program analysis page's source code.
    Get the number of a type(following, followers, discussions) and count 
    how many pages it has to search. It send each page's url to the 
    get_page_content function, get function's return.

    Args:
        username: blogcatalog username.
        task_type: the type of the task.

    Returns:
        result: a list contains all the data you want to get from a user.
    """
    # init the local variable according to the task type
    task_url = url + 'user/' + username + task_info[task_type]['task_url']
    page_capacity = int(task_info[task_type]['page_capacity'])
    button_a_class = task_info[task_type]['button_a_class']
    button_div_class = task_info[task_type]['button_div_class']

    # get the number of task_type
    soup = get_soup(task_url)

    if soup == None:
        return None

    button = soup.find('a', class_ = button_a_class)
    button_count = button.find('div', class_ = button_div_class)
    num_task = int(button_count.string.extract())

    result = []

    if num_task > page_capacity:
        num_page = num_task / page_capacity + 1
        response = get_page_content(task_url, task_type)
        if response != None:
            result += response
        for i in range(2, num_page + 1):
            print 100.0 * i / num_page, "%"
            response = get_page_content(task_url + str(i), task_type)
            if response != None:
                result += response
    elif num_task > 0:
        response = get_page_content(task_url,task_type)
        if response != None:
            result += response
    elif num_task == 0:
        return None
    # result += get_page_content(task_url,task_type)

    return result


if __name__ == '__main__':
    twitter_url = get_twitter_url('TonyB')
    print twitter_url
    task = ['blog', 'followers', 'following', 'reading', 'discussions', 'twitter']
    while(True):
        username = raw_input('Please enter the blogcatalog username(0 for exit): ')

        if username == '0':
            break
        following = get_detail_info(username, task_type = 'following')     
        write_to_txt(following, file_path + 'info\\' + str(username) + '_following.txt')
        print str(username), 'following finished!'

        followers = get_detail_info(username, task_type = 'followers')
        write_to_txt(followers, file_path + 'info\\' + str(username)  + '_followers.txt')
        print str(username), 'followers finished!'

        discussions = get_detail_info(username, task_type = 'discussions')
        write_to_txt(discussions, file_path + 'info\\' + str(username)  + '_discussions.txt')
        print str(username), 'discussions finished!'
    print get_basic_info('houseonthetree', task)