import time
import random

import pymysql
import urllib3
import json

db = pymysql.connect(host='172.20.37.201', port=3306, user='test', passwd='123456', db='bitcoin_data', charset='utf8')
cursor = db.cursor()

def query():
    try:
        sql = "select id,address from bitcoin_info order by id desc limit 50"
        # sql = "select id,address from bitcoin_info ORDER BY id desc LIMIT 50"
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        db.rollback()
        print(e)
    return results

def insertDB(id,point):
    #插入数据
    try:
        sql = "update bitcoin_info set point='{0}'where id={1}".format(point,id)
        print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

def ip_located(ip):
    """
    根据IP定位
    :param ip:
    :return:
    """

    # url = 'http://api.map.baidu.com/location/ip?ak=ZXlgu62mIHNza5AO8WtGea44EhsDMYKm&ip=' + ip + '&coor = gcj02'
    url = 'http://api.map.baidu.com/location/ip?ak=oGC2fIA4PC5x2Q7GhqHK8fVRbxaw3Zlj&ip='+ ip + '&coor=bd09ll'
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    msg_json = json.loads(r.data.decode())
    address  = ''
    point = ''
    print(msg_json)
    try:
        x = msg_json['content']['point']['x']
        y = msg_json['content']['point']['y']
        point = x+','+y
        # for item in msg_json.items():
        # address = msg_json['content']['address_detail']['province']
        # print(address)
        print(point)


    except:
        print('ip地址格式错误或者当前并发量已经超过约定并发配额，限制访问')
    return point


if __name__ == '__main__':
    """
    更新：2022.3.30
    百度地图API每天限额请求2000次,不能直接调用，需配合定时运行，将新爬取到的数据进行限额解析
    如定时爬取50条，则解析地址为50条。
    """
    results = query()
    for i in results:
        ipaddress = i[1].split(':')[0]
        point = ip_located(ipaddress)
        insertDB(i[0],point)
        sleeptime = random.randint(1,2)
        time.sleep(sleeptime)