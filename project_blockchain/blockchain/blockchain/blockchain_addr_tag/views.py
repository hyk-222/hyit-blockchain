import json
import datetime
import time

import traceback


import xlrd
from django.core.paginator import Paginator
from blockchain_address.views import address
from fsspec import transaction
# from scrapy import settings

# Create your views here.
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse

#
def addrtag_Retrieve(request):
    # 查看全部数据  Retrieve
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # get_tag = 'test_4nie0uah333bjj2'
    sql = "select tag_id, address, tag, update_time, create_time from bitcoin_address_tag"   # sql = "select * from bitcoin_address_tag".format(get_tag)
    data = []
    # 展示当前地址标注表中的全部信息
    addrtag_info = mysqlutil.queryOperation(sql)
    for j in range(0,len(addrtag_info)):
        data.append({'tag_id': addrtag_info[j][0], 'address':addrtag_info[j][1], 'tag': addrtag_info[j][2]}) # 'update_time':addrtag_info[j][3], 'create_time':addrtag_info[j][4]
    print(data)
    return HttpResponse(json.dumps({'code': 0, 'msg':'','count': len(addrtag_info),'data': data}))

    # addrtag_list = []
    # for i in addrtag_info:
    #     addrtag_list.append({'tag_id': i[0], 'address': i[1], 'tag': i[2]})
    # data.append(addrtag_list)  # data.append({'input': input_list})
    # print(data)
    # return HttpResponse(json.dumps({'code': 0,'data': data}))   # return HttpResponse(json.dumps({'code': 0,'data': data}))


    # get_hash = '31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb'
    # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently ORDER BY time DESC".format(get_hash)  # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    # data = []
    # total_info = mysqlutil.queryOperation(sql1)
    
    # for j in range(0,20):   # for j in range(0,len(total_info)):
    #     data.append({'id': total_info[j][0], 'hash':total_info[j][1], 'time': total_info[j][2] })

    # print(data)
    # return HttpResponse(json.dumps({'code': 0, 'msg':'','count': len(total_info),'data': data}))  # 'count': len(total_info),



def addrtag_Search(request):
    # 查看指定数据  Retrieve
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    get_address = 'test_4nie0uah333bjj2'
    data = []
    # 展示当前地址标注表中的全部信息
    sql = "SELECT `address`, tag_id, tag, update_time, create_time FROM bitcoin_address_tag WHERE `address` = '{0}'".format(get_address)
    addrtag_info = mysqlutil.queryOperation(sql)
    addrtag_list = []
    for i in addrtag_info:
        addrtag_list.append({'tag_id': i[1], 'address': i[0], 'tag': i[2],'长度': len(i)}) # , 'update_time': i[3]
    data.append(addrtag_list)  # data.append({'input': input_list})
    print(data)
    return HttpResponse(json.dumps({'code': 0,'data': data}))  # 'code': 0,


def addrtag_show(request):
   
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")

    pageIndex = request.GET.get("page")
    print(pageIndex)
    pageSize = request.GET.get("limit")
    print(pageSize)
    sql1 = "SELECT * FROM address_tag ORDER BY time_update DESC"
         # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)

    for j in range(0, len(total_info)):
        data.append(
            {
                "userId": j,
                "address": total_info[j][0],
                "tag": total_info[j][1],
                "time_update": total_info[j][2],
                "time_create": total_info[j][3],
            }
        )
    res=[]
    pageInator = Paginator(data, pageSize)
    context = pageInator.page(pageIndex)
    dataCount = len(data)
    for item in context:
        res.append(item)
    print(res)
    print(dataCount)

    print(type(data))
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},default=str))  # 'count': len(total_info)


#######################
#删除单条记录
#######################
def addrtag_delete(request):
    if request.method == 'POST':
        get_address = request.POST.get('address')
        print("request",get_address)
    #get_address=17348478397
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    sql = "delete from address_tag where address ='{0}'".format(get_address)
    total_info = mysqlutil.deleteOperation(sql)
    print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':True},ensure_ascii=False))

#######################
#删除多条记录
#######################
def addrtag_delete_M(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    data=json.loads(request.body)
    print(data)
    lenth = len(data)
    print('长度',lenth)
    delete_number=0
    for i in range(0,lenth):
        username=data[i]['address']
        print(username)
        sql = "delete from address_tag where address ='{0}'".format(username)
        total_info = mysqlutil.deleteOperation(sql)
        print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': lenth, 'success': True}, ensure_ascii=False))

#######################
#修改
#######################
def addrtag_edit(request):
    #后期需要做调整，此处设置为电话号码不可更改
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    #获取 json 类型数据:
    methodname = ""
    if request.method == 'POST':
        methodname=request.POST.get('methodname')
        data=request.POST.get('data')
        data_object = json.loads(data)
        print('methodname',methodname)
        if methodname=='del':
            pro_username=data_object["username"]
            
            print('要更改的地址',pro_username)
        else:
            update_data=data_object
            username=update_data['username']
            print('username',username)
            
            address = update_data["address"]
            tag =update_data["tag"]
            time_update =update_data["time_update"]
            time_create =update_data["time_create"]
            
            # time_zones =update_data["time_zones"]
            print('*********************',username,address,tag,time_update,time_create)
            sql2 = 'UPDATE address_tag SET address="{0}",tag="{1}",time_update="{2}",time_create="{3}"'.format(address, tag, time_update, time_create)
            
            total_info = mysqlutil.updateOperation(sql2)
            print(total_info)
            if total_info==1:
                success=True
            else:
                success=False
            print("更新数据",success)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': 1, 'success': success}, ensure_ascii=False))

#######################
#插入单条数据
#######################
def addrtag_insert(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # 获取 json 类型数据:
    get_data = json.loads(request.body)
    #print('inserdb',get_data['field'])
    data=get_data['field']
    # updata_people=data['upload_name']
    # print(updata_people)
    datetime01 = datetime.datetime.now()
    time_update = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    time_create = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    print(time_update)
    sql = \
        "insert into address_tag(address,tag,time_update,time_create)" \
        " values ('%s','%s','%s','%s')" \
        % (data["address"], data["tag"], time_update, time_create)

    total_info = mysqlutil.insertOperation(sql)
    print(total_info)
    if total_info==1:
        success=True
    else:
        success=False
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':success},ensure_ascii=False))



#######################
#查询（高级/简单）
#######################
#加入时间段查询
def addrtag_query(request):

    mysqlutil = MySQL_util(mysqldb.mysql_conf)

    if request.method == 'GET':
        page = request.GET.get("page")
        limit= request.GET.get("limit")
        address = request.GET.get("address")
        tag = request.GET.get("tag")

        time_zones= request.GET.get("time_zones")
        upload_name=request.GET.get("upload_name")
        print('上传人名字',upload_name)
        start_time=request.GET.get("start_time")

        end_time=request.GET.get("end_time")
        print('*************************************',start_time,end_time)

        if start_time=='':
            start=''
            end=''
        else:
            b='00:00:00'

            a = start_time+' '
            start =(a + b)
            print('我在哪里再55555555555555555555555',start)
            d='23:59:59'
            c=end_time+' '
            end = (c + d)
            # end="'"+(c+d)+"'"
            print('又到哪里去了￥￥￥￥￥￥￥￥￥￥￥￥￥￥',end)

    data={
        "userId": '1',
        "address": address,
        "tag": tag,

        
        
        "time_zones":time_zones,
        "upload_name":upload_name,
        "start":start,
        "end":end,
    }
    print("data",data)
    select = "select * from address_tag where (address='{0}' or '{0}'='') and (tag='{1}' or '{1}'='') and (lable ='{2}' or '{2}'='')" .format(data["address"], data["tag"])


    #select1 = "select * from huaian where upload_time between "+ start +" and "+ end+" in (select * from huaian where phone='17348478375') "
    #select1 = "select * from huaian where ='17348478353' and upload_time in (select upload_time from huaian where upload_time between '' and '')"
    #select1 = "select upload_time from huaian where upload_time between '2022-08-09 00:00:00' and '2022-08-11 00:00:00'"

    result_data = []

    total_info = mysqlutil.queryOperation(select)
    print('_____________________________________',total_info)
    for j in range(0, len(total_info)):
        result_data.append(
            {
                "userId": j,
                # "page": page,
                # "limit": limit,
                "address": total_info[j][0],
                "tag": total_info[j][1],
                # "IMEI2": total_info[j][2],
                # "IMSI": total_info[j][3],
                # "MAC": total_info[j][4],
                # "live_pro": total_info[j][5],
                # "live_city": total_info[j][6],
                # "live_region": total_info[j][7],
                # "live_poi": total_info[j][8],
                # "job_pro": total_info[j][9],
                # "job_city": total_info[j][10],
                # "job_region": total_info[j][11],
                # "job_poi": total_info[j][12],
                # "use_language": total_info[j][13],
                # "time_zones": total_info[j][14],
                # "lable": total_info[j][15],
                # "upload_name": total_info[j][16],
                # "upload_time": total_info[j][17],
            }
        )
    res = []
    pageInator = Paginator(result_data, limit)
    context = pageInator.page(page)
    dataCount = len(data)
    for item in context:
        res.append(item)
    # print(res)
    # print(dataCount)
    # print('query_data___________',result_data)
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},default=str))  # 'count': len(total_info),










def addr_monitor_show(request):
   
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")

    pageIndex = request.GET.get("page")
    print(pageIndex)
    pageSize = request.GET.get("limit")
    print(pageSize)
    sql1 = "SELECT * FROM addr_monitor ORDER BY recent_alert_time DESC"
         # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)

    for j in range(0, len(total_info)):
        data.append(
            {
                "userId": j,
                "incident": total_info[j][0],
                "monitor_addr_number": total_info[j][1],
                "alert_number": total_info[j][2],
                "state": total_info[j][3],
                "recent_alert_time": total_info[j][4],
                "createTime": total_info[j][5],
            }
        )
    res=[]
    pageInator = Paginator(data, pageSize)
    context = pageInator.page(pageIndex)
    dataCount = len(data)
    for item in context:
        res.append(item)
    print(res)
    print(dataCount)

    print(type(data))
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},default=str))  # 'count': len(total_info)


#######################
#删除单条记录
#######################
def addr_monitor_delete(request):
    if request.method == 'POST':
        get_address = request.POST.get('incident')
        print("request",get_address)
    #get_address=17348478397
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    sql = "delete from addr_monitor where incident ='{0}'".format(get_address)
    total_info = mysqlutil.deleteOperation(sql)
    print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':True},ensure_ascii=False))

#######################
#删除多条记录
#######################
def addr_monitor_delete_M(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    data=json.loads(request.body)
    print(data)
    lenth = len(data)
    print('长度',lenth)
    delete_number=0
    for i in range(0,lenth):
        username=data[i]['incident']
        print(username)
        sql = "delete from addr_monitor where incident ='{0}'".format(username)
        total_info = mysqlutil.deleteOperation(sql)
        print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': lenth, 'success': True}, ensure_ascii=False))

#######################
#修改
#######################
def addr_monitor_edit(request):
    #后期需要做调整，此处设置为电话号码不可更改
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    #获取 json 类型数据:
    methodname = ""
    if request.method == 'POST':
        methodname=request.POST.get('methodname')
        data=request.POST.get('data')
        data_object = json.loads(data)
        print('methodname',methodname)
        if methodname=='del':
            pro_username=data_object["username"]
            
            print('要更改的地址',pro_username)
        else:
            update_data=data_object
            username=update_data['username']
            print('username',username)
            
            incident = update_data["incident"]
            monitor_addr_number =update_data["monitor_addr_number"]
            state = update_data['state']
            recent_alert_time =update_data["recent_alert_time"]
            createTime =update_data["createTime"]
            
            print('*********************',username,incident,state,monitor_addr_number,recent_alert_time,createTime)
            sql2 = 'UPDATE addr_monitor SET incident="{0}",monitor_addr_number="{1}",state="{2}",recent_alert_time="{3}",createTime="{4}"'.format(incident, state, monitor_addr_number, recent_alert_time, createTime)
            
            total_info = mysqlutil.updateOperation(sql2)
            print(total_info)
            if total_info==1:
                success=True
            else:
                success=False
            print("更新数据",success)

    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': 1, 'success': success}, ensure_ascii=False))

#######################
#插入单条数据
#######################
def addr_monitor_insert(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # 获取 json 类型数据:
    get_data = json.loads(request.body)
    
    data=get_data['field']
    
    datetime01 = datetime.datetime.now()
    recent_alert_time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    createTime = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    print(recent_alert_time)
    sql = \
        "insert into addr_monitor(incident,monitor_addr_number,state,recent_alert_time,createTime)" \
        " values ('%s','%s','%s','%s','%s')" \
        % (data["incident"], data["monitor_addr_number"], data["state"], recent_alert_time, createTime)

    total_info = mysqlutil.insertOperation(sql)
    print(total_info)
    if total_info==1:
        success=True
    else:
        success=False
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':success},ensure_ascii=False))


