import json

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
