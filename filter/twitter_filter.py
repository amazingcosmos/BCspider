#-*-coding:utf-8-*-
import tweepy
import random
import urllib,urllib2
from bs4 import BeautifulSoup

list_avail = [['8hfIqM17pBWqRUCIz9GxTd69G','0Lukyb42ez3BC2djh2fRLt8o3HBLsLMsZdp5E9YhHFq8xcXLA6'],['NyWs5aWmJy1CiAixxgezCUL5H','ahTJbpN0ArA54xaT8UM62GLimYI9jcJ6JZkXbYoRGv3YKoKn90'],['8XHzBOoJZGt1Z5U4aXXj2LY6m','e9NKMxNnYHy41YTxMQeggye3PbK5ymhXf9brprOvSG51KEHcSo'],['KA7xWRwM4KYKilLDYz8L9F1WF','l0RUlIB0YccxfWQfBOYXOmoOK8jlXVqYyQkMCKFXCv4DVE8dI8'],['p6yPnBS9LMArh09YzqxRJJs1H','EqPTlugParcgteKCRAzrZpCLYjPJqu2XcArhlZlskO97p0CZ4r'],['blIdG0Esg25PG7nXdJGinBYLL','TgKw1ODTVGzCPt0VVnjD2BQ6tSV35eXhk3l4fptTQIPvh0nNPJ'],['T3uo6URgDaHcULF19QXtlSqX9','Ah4F1dgbQXFbHgzgv66SisQRpV5s9CpoP7lMjVc5DM2EdPETW5']\
,['Xr1B4gqLAoLGB7oxGXrD87YE1','6qN7sQ47ZAzKCD47uLctLVK9hEjTaxKUXo8OGCcbgnr9NsPOJs'],['TEZWfsClVtJHygEttWRg6IAgX','I8nNwBfIfaxdB2wqPCXlp1ykhZOkkSk0BUiuDHMRMoQlX4ErHY']\
,['PYqHOT5IESXNdDOeLrE24QfpX','I80jVaMXG4TxVtDm6e2ibUUvWlrm81WKqROcHpD3tFXqlGm5eX'],['HUDdQgqUbVlS55oyp2ZjjZGld','YCJR4lJlCp331jtpTJyr1uHky9i4eVldMoLssXL44IPEnjvouB']\
,['L58ZdAxUcIPu5PkP06av1NhTB','KZwnciQl57HRIwvxf6zFsqzuOwbF3Blpfo8ZdvdBazcmjGsqG8'],['Pipq2bOualWxjjAfWQjJjb93I','tSOlF6c3tAIuVi9BeNM2hySFxODzUNvCyGtNX0Yp8mVFwJu3XA']\
,['1WdtiO3C1AwcQEcscWb2bunEt','LqdCqjlr4qQtBGPEhMpQgtpO5doLAtC0eTaHY3ANSFMRPCuKa2'],['9M7OkcnrzGu7BgJcUESBUdWKB','TiVeTe4RiO8Xa3fu7ejPRbI7DheMlNFU9rtfqCy9hxDBm8dqyB']\
,['dUPtOaq1bTMtTzfLuI2ChaTqL','k6uBY0UTqdQUEXO04GCOUT6wphkHO3UJDjsWKUOAEkPPZMpMvX'],['GDWoZMGSAjZYenxRjH9JMttJn','BcYTgoR1QA9lvmOSqOhjnxQaojQ9n9fm63DBtKd4EHUAGvnWA6']\
,['NGSYY8SL4qoHUoAcxRLt9v4PA','69GFaeHSea38q2FyYrNfeAfbjGmApjILagSmtUV83FCq5UT58a'],['mnra1WhNDtT6YZRVpg8CwewAN','7Le0MYlLpZoX2XBsBIUY5TkzxRtyHQf3MBKWvaCn0FhwwOCSOl']\
,['Ng7eOR94b3FgzCqFJbP4qMWYC','HdaNvOuYt4CVKwQFPjzNy8fWZVgJBeDuBtlwLhrCfnGd25NIsn'],['Dx4CUYWNIqEGUWO5joCzRaTRN','JO1NFizzJ7NIP2sERWi5had1RMOv71XIZh4ScH0zqNuSbQo4be']\
,['LWkcTewyltNL9DoxGk4PyGviE','TAQi4wUPzjspWkNfibaPEh7Od31YOWHp9lmZT9x971BUhmG6OZ'],['67eZkp2YkcHob4UI9gNUla9LX','VnAcNII6ijYsd2oQgnB8GUPvkUG3dzm5Cg39WjVZCgGVE5xchy']\
,['n4rMJMSWTpEuHpdoqGLXuWhNn','5wuRX6cq4i4fe8bxdszLOQIbhLewF1ZeZ9Of33Jn0mDI0OBJ8P'],['B4BNPMZX7HDZ5FLSV48betYAW','sU0u2dcAF6C8liRgNXyeVOx4W7SgMbP3BlozuNE8zEk36vlrQh']\
,['PGne5fVMywYKvr3s3fU36fXIo','NF2CrF20sZHfTnJVZ48se2gsqOwtusGX3HzhQISZMr0441xzrf'],['M2fXHypvAr5544fyuYWlFE2OV','yTklVwVq15aKCTN6Ya4eRazW3XLvwK6h57OwsTOWVZLLNzweay']\
,['pshbPQgrFul5ZkUr9BXbNCy1n','4sO88Xx2wlZ6CiYRnPNL3YzAlJMFXrYLMZzimtM6oU9sYVktVt'],['Hr545vwxyy3o12O9fa7i9TmMN','XDqVvLDoURkCeCo8ow0H4aMyPMmN6DXxNmrrpcA8VLEZFYt38Y']\
]

def get_api():
    list_now = random.choice(list_avail)
    auth = tweepy.OAuthHandler(list_now[0],list_now[1])
    api = tweepy.API(auth)
    print 'Get authorization succeeded'
    return api

def get_twitter_ID(user_name):
    url = 'http://gettwitterid.com/?user_name=' + user_name + '&submit=GET+USER+ID'
    html = urllib2.urlopen(url).read()
    soup  = BeautifulSoup(html)
    try:
        s=soup.find(class_='profile_info')
        ss=s.find_all('p')[1]
        twitter_ID = int(ss.getText())
        return twitter_ID
    except:
        print 'Not find user'
        return 0

def get_filter(api,user_name):
    seed_nickname = get_twitter_ID(user_name)
    if seed_nickname == 0:
        return api
    while True:
        try:
            id_infor = api.get_user(seed_nickname)
            followers_count = id_infor.followers_count
            friends_count = id_infor.friends_count
            break
        except Exception,e:
            print e
            api = get_api()
    try:
        print str(id_infor.name) + '   followers:' + str(followers_count) + '   friends:' + str(friends_count)
    except:
        print 'encoding error,pass...'
    f = open('filter.txt','a')
    try:
        f.write(user_name+'$||$'+id_infor.name.encode('utf-8')+'$||$'+str(seed_nickname)+'$||$'+str(followers_count)+'$||$'+str(friends_count)+'\n')
    except:
        print 'encoding error,pass...'
    f.close()
    return api
        

if __name__ == '__main__' :
    f = open('user_todo.txt','r')
    user_name_list = []
    for line in f.readlines():
        user_name = line.split('$||$')[0]
        user_name_list.append(user_name)
    api = get_api()
    for user_name in user_name_list:
       api = get_filter(api,user_name)
    



























