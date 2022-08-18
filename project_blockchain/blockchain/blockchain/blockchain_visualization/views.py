# -*- coding:utf-8 -*-
import json
import traceback
import urllib.request

import urllib3
import xlrd
from django.shortcuts import render
import re
# Create your views here.
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse, JsonResponse
from .utils.decimal_util import DecimalEncoder

def now_transaction(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    transactions_query = "SELECT (sum(output_total)-sum(fee_total)-sum(generation))*POWER(10,-8) as tody_total," \
                         "sum(transaction_count) as today_count," \
                         "(sum(input_count)+sum(output_count)) as today_address " \
                         "FROM bitcoin_blocks WHERE time >= '2022-01-02'"
    today_data = mysqlutil.queryOperation(transactions_query)
    today_total = today_data[0][0]
    today_count = eval(json.dumps(today_data[0][1], cls=DecimalEncoder))
    today_address = eval(json.dumps(today_data[0][2], cls=DecimalEncoder))

    today_dict = {
        'today_total': today_total,
        'today_count': today_count,
        'today_address': today_address
    }

    url = "https://api.nomics.com/v1/currencies/ticker?key=43612c84561385c1fd04dcf535f3f4d31bd32cc2&ids=BTC&interval=1d,30d&convert=EUR&platform-currency=ETH&per-page=100&page=1"
    i = urllib.request.urlopen(url).read()
    print(i)

    return HttpResponse(json.dumps({'data': today_dict}))


def RankValue(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    rank_query = "SELECT recipient,value FROM `outputs-pro` WHERE time LIKE '%03-07%' ORDER BY value desc"
    # rank_query = "SELECT recipient,value FROM output ORDER BY value desc"
    # rank_query = "select id,address from bitcoin_info"
    rank_data = mysqlutil.queryOperation(rank_query)
    rank_list = []
    for i in range(5):
        rank_recipient = rank_data[i][0]  # 地址
        rank_value = rank_data[i][1]  # 值
        rank_list.append({
            'rank_recipient': rank_recipient,
            'rank_value': rank_value
        })
    print(rank_list)

    return HttpResponse(json.dumps({'data': rank_list}))


def Today_trade(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # trade_query = "SELECT output_total,fee_total,generation,transaction_count,input_count,output_count " \
    #               "FROM bitcoin_blocks group by time desc"
    trade_query = "SELECT output_total,fee_total,generation,transaction_count,input_count,output_count " \
                  "FROM bitcoin_blocks where time LIKE '%03-07%'"
    # trade_query = "SELECT output_total,fee_total,generation,transaction_count " \
    #               "FROM bitcoin_test where time LIKE '%2016-01-20%'"
    trade_data = mysqlutil.queryOperation(trade_query)

    # 方式一：python处理：如果要拿到最新一天的数据的逻辑实现：数据按日期降序输出，用for循环遍历判断是不是与上一条数据相同，如果是则加入列表，不是的话终止循环
    # 方式二：mysql处理：select time from bitcoin_test where time > date_sub('2017-06-27', INTERVAL 0 DAY)。curdate()
    # trade_btc_query = "select id from bitcoin_test order by time DESC limit 1"
    trade_btc_query = "select id from bitcoin_blocks order by time DESC limit 1"
    trade_btc_list = mysqlutil.queryOperation(trade_btc_query)
    trade_btc = int(trade_btc_list[0][0])

    trade_list = []
    output_total = 0
    fee_total = 0
    generation = 0
    transaction_count = 0
    input_count = 0
    output_count = 0

    for i in range(len(trade_data)):
        output_total += int(trade_data[i][0])  # 将每行数据都加起来
        fee_total += int(trade_data[i][1])
        generation += int(trade_data[i][2])
        transaction_count += int(trade_data[i][3])
        input_count += int(trade_data[i][4])
        output_count += int(trade_data[i][5])

    today_trade_count = output_total - fee_total - generation  # 计算公式
    today_active = input_count + output_count

    trade_list.append({
        'today_count': today_trade_count,
        'transaction_count': transaction_count,
        'today_active': today_active,
        'trade_btc': trade_btc,
    })
    # print(trade_data)
    return HttpResponse(json.dumps({'data': trade_list}))


def MapData(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    map_query_height = "select height from bitcoin_info GROUP BY height ORDER BY height desc"
    map_height_data = mysqlutil.queryOperation(map_query_height)
    height_list = []
    # print(map_height_data)
    for i in map_height_data[:5]:  # 页面只需显示5个height值列表
        height_list.append(i[0])  # 元组形式为((72769,)),将下标为0的取出即可

    print(height_list)

    map_query = "select height,location from bitcoin_info ORDER BY height desc "
    map_data = mysqlutil.queryOperation(map_query)

    zero_list = []
    one_list = []
    two_list = []
    three_list = []
    four_list = []

    for i in map_data:  # 遍历数据库查询的数据
        for num, j in enumerate(height_list):  # 遍历height值
            if i[0] in j:  # 数据库的height匹配到页面所需的5个值，则加入列表
                if num == 0:
                    zero_list.append(i)
                elif num == 1:
                    one_list.append(i)
                elif num == 2:
                    two_list.append(i)
                elif num == 3:
                    three_list.append(i)
                elif num == 4:
                    four_list.append(i)

    # print(zero_list)
    # print(len(two_list))
    # map_list = [] #出错，数据会保存在这个数组里

    def handle_process(num_list):
        map_list = []  # 清空数组
        # 筛选城市的出现的次数
        for i in num_list:
            with open("./blockchain_visualization/utils/city.json", "r",
                      encoding='utf-8') as city:  # 路径以manage.py为初始开始寻找
                load_dict = json.load(city)
                for test_name in load_dict.keys():
                    if test_name in i[1]:  # 如果城市的拼音匹配到数据库查询的拼音相同，则加入列表。i的输出形式为('727692', 'Zhaobaoshan, China')
                        map_list.append(test_name)

        # 统计重复项
        city_count_list = []
        myset = set(map_list)  # myset是另外一个列表，里面的内容是mylist里面的无重复项
        for item in myset:
            city_name = item
            city_name_count = map_list.count(item)
            city_count_list.append({
                'city_name': city_name,
                'city_name_count': city_name_count
            })

        # 加入列表
        city_info_list = []
        city_info_list.append({
            'height': num_list[0][0],
            'city_count': city_count_list
        })
        # print(city_info_list)
        return city_info_list

    # 加入总列表
    map_info_data = handle_process(zero_list) + handle_process(one_list) + handle_process(two_list) + handle_process(
        three_list) + handle_process(four_list)

    return HttpResponse(json.dumps({'data': map_info_data}))


def Bit_trade(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # curdate()获取当天日期。格式为‘202-03-26’
    bit_trade_query = "select time,output_total from bitcoin_test_recently where time > date_sub('2017-06-27', INTERVAL 14 DAY)"  # 获取15天的数数。表里最新的是2017-06-27
    bit_trade_data = mysqlutil.queryOperation(bit_trade_query)

    bit_trade_time_query = "select SUBSTR(time,'2'-1,10) as sub_time from bitcoin_test_recently where time > date_sub('2017-06-27', INTERVAL 14 DAY) GROUP BY sub_time"
    bit_trade_time_data = mysqlutil.queryOperation(bit_trade_time_query)

    bit_trade_time_list = []
    for i in bit_trade_time_data:
        bit_trade_time_list.append(i[0])

    bit_trade_time_len = len(bit_trade_time_list)
    bit_trade_time_count_list = [0]*bit_trade_time_len

    for i in range(len(bit_trade_time_list)):   #将每天的交易额各自加起来存入列表
        for j in range(len(bit_trade_data)):
            if bit_trade_time_list[i] in bit_trade_data[j][0]:
                # bit_trade_time_count_list[i] += round(float(bit_trade_data[j][1])/(10**8))
                bit_trade_time_count_list[i] += (float(bit_trade_data[j][1])/(10**8))/(10**4)
                # print(type(bit_trade_time_count_list[i]))

    bit_trade_time_list_handle = []
    for i in bit_trade_time_list:       #处理日期，将2017-06-13做成06-13
        time = re.match("\d*-(\d*-\d*)", i).group(1)
        bit_trade_time_list_handle.append(time)

    bit_trade_dict = {
        'bit_trade_time_list':bit_trade_time_list_handle,
        'bit_trade_time_count_list':bit_trade_time_count_list,
    }

    return HttpResponse(json.dumps({'data': bit_trade_dict}))

def MapData2(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    map_query_height = "select height from bitcoin_info ORDER BY height desc limit 1"
    map_height_data = mysqlutil.queryOperation(map_query_height)
    height = map_height_data[0][0]
    print(height)

    map_data_query = "select point from bitcoin_info LIMIT 1000"
    map_data = mysqlutil.queryOperation(map_data_query)
    point_list = []
    for i in map_data:
        if i[0]:
            # handle_xy = re.match('(\d*\D\d*)\W(\d*\D\d*)', i[0])
            # x = re.match('\d{3}', handle_xy.group(1)).group() + '.' + re.match('(\d{3})(\d{4})', handle_xy.group(1)).group(2)
            # y = re.match('\d{2}', handle_xy.group(2)).group() + '.' + re.match('(\d{2})(\d{4})', handle_xy.group(2)).group(2)
            # point = x+', '+y
            point_deal = i[0].split('p')
            s = [float(i) for i in point_deal[0].split(',')]
            point_list.append(s)

    # print(point_list)
    # print(len(point_list))
    map_count_data = {
        "height":height,
        "point_list":point_list
    }
    return HttpResponse(json.dumps({'data':map_count_data}))



##前端首页
def recent_active_address(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")
    get_hash = '31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb'
    sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently ORDER BY time DESC"
         # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)

    for j in range(0, 20):  # for j in range(0,len(total_info)):
        data.append({'id': total_info[j][0], 'hash': total_info[j][1], 'time': total_info[j][2]})

    print(data)
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': data}))  # 'count': len(total_info),




