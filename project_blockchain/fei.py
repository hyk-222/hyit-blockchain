import json

# Create your views here.
# from .utils import mysqldb
# from .utils.mysqldb import MySQL_util
from django.http import HttpResponse


def query_vpn_two_all(request):
    # 查看设备数据vpn_two全部数据  Retrieve
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # get_tag = 'test_4nie0uah333bjj2'
    sql = "select * from vpn_cd2"
    data = []
    # 显示设备数据表中的全部信息
    data1_info = mysqlutil.queryOperation(sql)
    for j in range(0, len(data1_info)):
        data.append({'phone': data1_info[j][0], 'IMEI1': data1_info[j][1],
                     'IMEI2': data1_info[j][2],'IMSI': data1_info[j][3],
                     'mac': data1_info[j][4],'live_pro': data1_info[j][5],
                     'live_city':data1_info[j][6],'live_region':data1_info[j][7],
                     'live-poi':data1_info[j][8],'job_pro':data1_info[j][9],
                     'job_city':data1_info[j][10],'job_region':data1_info[j][11],
                     'job_poi':data1_info[j][12]})
    print(data)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': len(data1_info), 'data': data}))

def query_vpn_two_con(request):
    # 查看vpn_two指定数据  Retrieve
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
   # live_pro = '江苏省'
    data = []
    # 展示当前地址标注表中的全部信息
    sql = "SELECT `live_pro`, phone, IMEI1, IMEI2, IMSI,  MAC, live_city, live_region,job_pro,job_city,job_region,use_language,time_zones,lable" \
          "FROM vpn_two WHERE `live_pro` = '{0}'".format(request)
    query_vpn_two_info = mysqlutil.queryOperation(sql)
    query_vpn_two_list = []
    for i in query_vpn_two_info:
        query_vpn_two_list.append({'phone': i[1], 'IMEI1':i[2],'IMEI2':i[3],'IMSI':i[4],
                             'MAC':i[5],'live_city': i[6], 'live_region': i[7],'job_pro': i[8],
                             'job_city': i[9], 'job_region': i[10], 'use_language': i[11], 'time_zones': i[12], 'lable': i[13],
                             '长度': len(i)})
    data.append(query_vpn_two_list)
    print(data)
    return HttpResponse(json.dumps({'code': 0, 'data': data}))  # 'code': 0,

def insert_vpn_all(request):
    #插入数据表vpn_two设备数据
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    data = []
    sql = "insert into vpn_two(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city," \
          "live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable)".format(request)
    insert_info = mysqlutil.insertOperation(sql)
    print(insert_info)#验证是否插入成功
    return HttpResponse(json.dumps({'code': 0, 'data': data}))  # 'code': 0,

def update_vpn_two(request):
    #更新数据表学信息
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    data = []
    sql = "update vpn_two set phone='{0}'".format(request)
    update_info = mysqlutil.updateOperation(sql)
    print(update_info)
    return HttpResponse(json.dumps({'code': 0, 'data': data}))  # 'code': 0,
def delete_vpn_two(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    sql = "delete from huaian where phone='{0}'".format(request)
    data = []
    delete_info = mysqlutil.deleteOperation(sql)
    print(delete_info)
    return HttpResponse(json.dumps({'code': 0, 'data': data}))  # 'code': 0,
