#-*-coding:utf-8-*-
import datetime
import json
import time

# Create your views here.
import traceback


import xlrd
from django.core.paginator import Paginator
from fsspec import transaction
from scrapy import settings

from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse
#######################
#删除单条记录
#######################
def DeleteDB(request):
    if request.method == 'POST':
        get_phone = request.POST.get('username')
    #     print("request",get_phone)
    #get_phone=17348478397
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    sql = "delete from huaian where phone='{0}'".format(get_phone)
    total_info = mysqlutil.deleteOperation(sql)
    print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':True},ensure_ascii=False))
#######################
#删除多条记录
#######################
def DeleteDB_multiple(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    data=json.loads(request.body)
    print(data)
    lenth = len(data)
    print('长度',lenth)
    delete_number=0
    for i in range(0,lenth):
        username=data[i]['username']
        print(username)
        sql = "delete from huaian where phone='{0}'".format(username)
        total_info = mysqlutil.deleteOperation(sql)
        print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': lenth, 'success': True}, ensure_ascii=False))
    # data = get_data['field']
    # get_phone = request.POST.get(request)
    #
    # print(get_phone)
    #     print("request",get_phone)
    #get_phone=17348478397
    # mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    # sql = "delete from huaian where phone='{0}'".format(get_phone)
    # total_info = mysqlutil.deleteOperation(sql)


#######################
#vpn数据库展示
#######################
def vpn_show(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")

    pageIndex = request.GET.get("page")
    print(pageIndex)
    pageSize = request.GET.get("limit")
    print(pageSize)
    sql1 = "SELECT * FROM huaian ORDER BY phone DESC"
         # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)

    for j in range(0,len(total_info)):
        data.append(
            {
                "userId": j,
                "username": total_info[j][0],
                "IMEI1": total_info[j][1],
                "IMEI2": total_info[j][2],
                "IMSI": total_info[j][3],
                "MAC": total_info[j][4],
                "live_pro": total_info[j][5],
                "live_city": total_info[j][6],
                "live_region": total_info[j][7],
                "live_poi": total_info[j][8],
                "job_pro": total_info[j][9],
                "job_city": total_info[j][10],
                "job_region": total_info[j][11],
                "job_poi": total_info[j][12],
                "use_language": total_info[j][13],
                "time_zones": total_info[j][14],
                "lable": total_info[j][15],
                "upload_name":total_info[j][16],
                "upload_time": total_info[j][17],
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
#插入单条数据
#######################
def InsertDB(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # 获取 json 类型数据:
    get_data = json.loads(request.body)
    #print('inserdb',get_data['field'])
    data=get_data['field']
    updata_people=data['upload_name']
    print(updata_people)
    datetime01 = datetime.datetime.now()
    upload_time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    print(upload_time)
    sql = \
        "insert into huaian(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable,upload_name,upload_time)" \
        " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
        % (data["username"], data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"], data["live_pro"], data["live_city"],
           data["live_region"], data["live_poi"], data["job_pro"], data["job_city"], data["job_region"], data["job_poi"],
           data["use_language"], data["time_zones"], data["lable"],data['upload_name'],upload_time)
    total_info = mysqlutil.insertOperation(sql)
    print(total_info)
    if total_info==1:
        success=True
    else:
        success=False
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':success},ensure_ascii=False))
#######################
#插入excel文件
#######################
def InsertExcel(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    excel_file = request.FILES.get('file')  # 获取前端上传的文件
    print('*******************',excel_file)
    file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        book = xlrd.open_workbook(filename=None, file_contents=excel_file.read())

        sheets = book.sheet_names()  # 获取所有sheet表名  s`  q
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print("11111",row_num)
        list = []  # 定义列表用来存放数据
        count=0
        false_number=0
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = {row_data[0], row_data[1], row_data[2], row_data[3],
                     row_data[4], row_data[5], row_data[6], row_data[7],
                     row_data[8], row_data[9], row_data[10], row_data[11],
                     row_data[12], row_data[13], row_data[14], row_data[15],
                     }  # 选择获取第几列

            sql = "insert into huaian(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                % (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6],
                    row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12],
                    row_data[13], row_data[14], row_data[15])
            print("22222",value)
            total_info = mysqlutil.insertOperation(sql)
            print(total_info)
            list.append(value)  # 将数据暂存在列表

            if total_info == 1:
                count+= 1
                print('true', count)
            else:
                false_number+=1
                print('false',false_number)

            # print(i)
        list_len=len(list)
        print("list", list_len)
        if count==list_len:
            success=True
        elif false_number==list_len:
            success=False
        else:
            success='other!'
        print(success)
        return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count':list_len,'true_number':count,'false_number':false_number,'success':success},ensure_ascii=False))

#######################
#修改
#######################
def Edit(request):
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
            # sql1="delete from huaian where phone='{0}'".format(pro_username)
            # total_info = mysqlutil.deleteOperation(sql1)
            print('要更改的条目号码',pro_username)
        else:
            update_data=data_object
            username=update_data['username']
            print('username',username)
            use_language = update_data["use_language"]
            lable =update_data["lable"]
            IMEI1 =update_data["IMEI1"]
            IMEI2 =update_data["IMEI2"]
            IMSI =update_data["IMSI"]
            MAC =update_data["MAC"]
            live_pro =update_data["live_pro"]
            live_city =update_data["live_city"]
            live_region =update_data["live_region"]
            live_poi = update_data["live_poi"]
            job_pro =update_data["job_pro"]
            job_city = update_data["job_city"]
            job_region =update_data["job_region"]
            job_poi = update_data["job_poi"]
            time_zones =update_data["time_zones"]
            print('*********************',username,live_city,IMSI,IMEI2,MAC,live_pro)
            sql2 = 'UPDATE huaian SET phone="{0}",IMEI1="{1}",IMEI2="{2}",IMSI="{3}",MAC="{4}",live_pro="{5}",live_city="{6}",live_region="{7}",live_poi="{8}",job_pro="{9}",job_city="{10}",job_region="{11}",job_poi="{12}",use_language="{13}",time_zones="{14}",lable="{15}" WHERE phone = "{16}"'.format(username, IMEI1, IMEI2, IMSI, MAC, live_pro, live_city, live_region, live_poi, job_pro, job_city, job_region, job_poi,use_language,time_zones,lable,username)
            # sql = \
            #     "insert into huaian(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable)" \
            #     " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            #     % (data["username"], data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"], data["live_pro"],
            #        data["live_city"],
            #        data["live_region"], data["live_poi"], data["job_pro"], data["job_city"], data["job_region"],
            #        data["job_poi"],
            #        data["use_language"], data["time_zones"], data["lable"])
            total_info = mysqlutil.updateOperation(sql2)
            print(total_info)
            if total_info==1:
                success=True
            else:
                success=False
            print("更新数据",success)

    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': 1, 'success': success}, ensure_ascii=False))
#######################
#查询（高级/简单）
#######################
#加入时间段查询
def Query(request):

    mysqlutil = MySQL_util(mysqldb.mysql_conf)

    if request.method == 'GET':
        page = request.GET.get("page")
        limit= request.GET.get("limit")
        username = request.GET.get("username")
        use_language = request.GET.get("use_language")
        lable= request.GET.get("lable")
        IMEI1= request.GET.get("IMEI1")
        IMEI2= request.GET.get("IMEI2")
        IMSI= request.GET.get("IMSI")
        MAC= request.GET.get("MAC")
        live_pro= request.GET.get("live_pro")
        live_city= request.GET.get("live_city")
        live_region= request.GET.get("live_region")
        live_poi= request.GET.get("live_poi")
        job_pro= request.GET.get("job_pro")
        job_city= request.GET.get("job_city")
        job_region= request.GET.get("job_region")
        job_poi= request.GET.get("job_poi")
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
        "username": username,
        "use_language":use_language,
        "lable":lable,
        "IMEI1":IMEI1,
        "IMEI2":IMEI2,
        "IMSI":IMSI,
        "MAC":MAC,
        "live_pro":live_pro,
        "live_city":live_city,
        "live_region":live_region,
        "live_poi":live_poi,
        "job_pro":job_pro,
        "job_city":job_city,
        "job_region":job_region,
        "job_poi":job_poi,
        "time_zones":time_zones,
        "upload_name":upload_name,
        "start":start,
        "end":end,
    }
    print("data",data)
    #print('zaizheli****************************:',type(data['username']))

    #select='select * from huaian where (phone="{0}" or "{0}"="") and (IMEI1="{1}" or "{1}"="")'.format(data["username"], data["IMEI1"])
    select = "select * from huaian where (phone='{0}' or '{0}'='') and (use_language='{1}' or '{1}'='') and (lable ='{2}' or '{2}'='') and (IMEI1 ='{3}' or '{3}'='')" \
             " and (IMEI2 ='{4}' or '{4}'='') and (IMSI ='{5}' or '{5}'='') and (MAC ='{6}' or '{6}'='') and (live_pro ='{7}' or '{7}'='')" \
             " and (live_city ='{8}' or '{8}'='') and (live_region ='{9}' or '{9}'='') and (live_poi ='{10}' or '{10}'='')" \
             " and (job_pro ='{11}' or '{11}'='') and (job_city ='{12}' or '{12}'='') and (job_region ='{13}' or '{13}'='') and (job_poi ='{14}' or '{14}'='')" \
             " and (time_zones ='{15}' or '{15}'='') and (upload_name ='{16}' or '{16}'='') and upload_time in (select upload_time from huaian where upload_time between '{17}' and '{18}')".format(data["username"], data["use_language"], data["lable"],
                                                            data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],
                                                            data["live_pro"], data["live_city"],
                                                            data["live_region"], data["live_poi"], data["job_pro"],
                                                            data["job_city"], data["job_region"], data["job_poi"],
                                                            data["time_zones"],data["upload_name"],data["start"],data["end"])


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
                "username": total_info[j][0],
                "IMEI1": total_info[j][1],
                "IMEI2": total_info[j][2],
                "IMSI": total_info[j][3],
                "MAC": total_info[j][4],
                "live_pro": total_info[j][5],
                "live_city": total_info[j][6],
                "live_region": total_info[j][7],
                "live_poi": total_info[j][8],
                "job_pro": total_info[j][9],
                "job_city": total_info[j][10],
                "job_region": total_info[j][11],
                "job_poi": total_info[j][12],
                "use_language": total_info[j][13],
                "time_zones": total_info[j][14],
                "lable": total_info[j][15],
                "upload_name": total_info[j][16],
                "upload_time": total_info[j][17],
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

#######################
#插入excel文件(上传人，上传时间)
#######################
def InsertExcel_u(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    upload_name=request.POST.get('upload_name')
    print('dafda',upload_name)

    datetime01 = datetime.datetime.now()
    time=datetime01.strftime("%Y-%m-%d %H:%M:%S")
    print(time)
    excel_file = request.FILES.get('file')  # 获取前端上传的文件
    print('*******************',excel_file)
    file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        book = xlrd.open_workbook(filename=None, file_contents=excel_file.read())

        sheets = book.sheet_names()  # 获取所有sheet表名  s`  q
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print("11111",row_num)
        list = []  # 定义列表用来存放数据
        count=0
        false_number=0
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = {row_data[0], row_data[1], row_data[2], row_data[3],
                     row_data[4], row_data[5], row_data[6], row_data[7],
                     row_data[8], row_data[9], row_data[10], row_data[11],
                     row_data[12], row_data[13], row_data[14], row_data[15],
                     }  # 选择获取第几列
            print(time,upload_name)
            sql = "insert into huaian(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable,upload_name,upload_time)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                % (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6],
                    row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12],
                    row_data[13], row_data[14], row_data[15],upload_name,time)
            print("22222",value)
            total_info = mysqlutil.insertOperation(sql)
            print(total_info)
            list.append(value)  # 将数据暂存在列表

            if total_info == 1:
                count+= 1
                print('true', count)
            else:
                false_number+=1
                print('false',false_number)

            # print(i)
        list_len=len(list)
        print("list", list_len)
        if count==list_len:
            success=True
        elif false_number==list_len:
            success=False
        else:
            success='other!'
        print(success)
        return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count':list_len,'true_number':count,'false_number':false_number,'success':success},ensure_ascii=False))



'''全国虚拟货币使用记录表'''


#######################
#删除单条记录
#######################
def all_DeleteDB(request):
    if request.method == 'POST':
        get_phone = request.POST.get('username')
    #     print("request",get_phone)
    #get_phone=17348478397
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    sql = "delete from virtual_currency where phone='{0}'".format(get_phone)
    total_info = mysqlutil.deleteOperation(sql)
    print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info,'success':True},ensure_ascii=False))
#######################
#删除多条记录
#######################
def all_DeleteDB_multiple(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    data=json.loads(request.body)
    print(data)
    lenth = len(data)
    print('长度',lenth)
    delete_number=0
    for i in range(0,lenth):
        username=data[i]['username']
        print(username)
        sql = "delete from virtual_currency where phone='{0}'".format(username)
        total_info = mysqlutil.deleteOperation(sql)
        print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': lenth, 'success': True}, ensure_ascii=False))
    # data = get_data['field']
    # get_phone = request.POST.get(request)
    #
    # print(get_phone)
    #     print("request",get_phone)
    #get_phone=17348478397
    # mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接
    # sql = "delete from huaian where phone='{0}'".format(get_phone)
    # total_info = mysqlutil.deleteOperation(sql)

#######################
# vpn数据库展示
#######################
def all_vpn_show(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")

    pageIndex = request.GET.get("page")
    print(pageIndex)
    pageSize = request.GET.get("limit")
    print(pageSize)
    sql1 = "SELECT * FROM virtual_currency ORDER BY phone DESC"
    # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)
    print(total_info)

    for j in range(0, len(total_info)):
        data.append(
            {
                "userId": j,
                "username": total_info[j][0],
                "IMEI1": total_info[j][1],
                "IMEI2": total_info[j][2],
                "IMSI": total_info[j][3],
                "MAC": total_info[j][4],
                "live_pro": total_info[j][5],
                "live_city": total_info[j][6],
                "live_region": total_info[j][7],
                "live_poi": total_info[j][8],
                "job_pro": total_info[j][9],
                "job_city": total_info[j][10],
                "job_region": total_info[j][11],
                "job_poi": total_info[j][12],
                "lable": total_info[j][13],
                "use_language": total_info[j][14],
                "time_zones": total_info[j][15],
                "app_name":total_info[j][16],
                "packages_name": total_info[j][17],
                "Install_state": total_info[j][18],
                "first_install_time": total_info[j][19],
                "end_install_time": total_info[j][20],
                "uninstall_number": total_info[j][21],
                "active_time": total_info[j][22],
                "upload_name": total_info[j][23],
                "upload_time": total_info[j][24],

            }
        )
    print(data)
    res = []
    pageInator = Paginator(data, pageSize)
    context = pageInator.page(pageIndex)
    dataCount = len(data)
    for item in context:
        res.append(item)
    print(res)
    print(dataCount)

    print(type(data))
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},
                   default=str))  # 'count': len(total_info)


#######################
# 插入单条数据
#######################
def all_InsertDB(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # 获取 json 类型数据:
    get_data = json.loads(request.body)
    # print('inserdb',get_data['field'])
    data = get_data['field']
    print(data)
    updata_people = data['upload_name']
    #print(updata_people)
    datetime01 = datetime.datetime.now()
    upload_time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    #print(upload_time)
    sql = \
        "insert into virtual_currency(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,lable,use_language,time_zones,app_name,packages_name,Install_state,first_install_time,end_install_time,uninstall_number,active_time,upload_name,upload_time)" \
        " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
        % (
        data["username"], data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"], data["live_pro"], data["live_city"],
        data["live_region"], data["live_poi"], data["job_pro"], data["job_city"], data["job_region"], data["job_poi"],
        data["lable"],data["use_language"], data["time_zones"], data['app_name'],data['packages_name'],data['Install_state'],
        data['first_install_time'],data['end_install_time'],data['uninstall_number'],data['active_time'],data['upload_name'], upload_time)
    total_info = mysqlutil.insertOperation(sql)
    print(total_info)
    if total_info == 1:
        success = True
    else:
        success = False
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': total_info, 'success': success}, ensure_ascii=False))


#######################
# 插入excel文件
#######################
def all_InsertExcel(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    excel_file = request.FILES.get('file')  # 获取前端上传的文件
    print('*******************', excel_file)
    file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        book = xlrd.open_workbook(filename=None, file_contents=excel_file.read())

        sheets = book.sheet_names()  # 获取所有sheet表名  s`  q
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print("11111", row_num)
        list = []  # 定义列表用来存放数据
        count = 0
        false_number = 0
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = {row_data[0], row_data[1], row_data[2], row_data[3],
                     row_data[4], row_data[5], row_data[6], row_data[7],
                     row_data[8], row_data[9], row_data[10], row_data[11],
                     row_data[12], row_data[13], row_data[14], row_data[15],
                     row_data[16], row_data[17], row_data[18], row_data[19],
                     row_data[20], row_data[21], row_data[22], row_data[23],
                     }  # 选择获取第几列

            sql = "insert into virtual_currency(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  % (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6],
                     row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12],
                     row_data[13], row_data[14], row_data[15])
            print("22222", value)
            total_info = mysqlutil.insertOperation(sql)
            print(total_info)
            list.append(value)  # 将数据暂存在列表

            if total_info == 1:
                count += 1
                print('true', count)
            else:
                false_number += 1
                print('false', false_number)

            # print(i)
        list_len = len(list)
        print("list", list_len)
        if count == list_len:
            success = True
        elif false_number == list_len:
            success = False
        else:
            success = 'other!'
        print(success)
        return HttpResponse(json.dumps(
            {'code': 0, 'msg': '', 'count': list_len, 'true_number': count, 'false_number': false_number,
             'success': success}, ensure_ascii=False))


#######################
# 修改
#######################
def all_Edit(request):
    # 后期需要做调整，此处设置为电话号码不可更改
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # 获取 json 类型数据:
    methodname = ""
    if request.method == 'POST':
        methodname = request.POST.get('methodname')
        data = request.POST.get('data')
        data_object = json.loads(data)
        print(data_object)
        print('methodname', methodname)
        if methodname == 'del':
            pro_username = data_object["username"]
            # sql1="delete from huaian where phone='{0}'".format(pro_username)
            # total_info = mysqlutil.deleteOperation(sql1)
            print('要更改的条目号码', pro_username)

        else:
            update_data = data_object
            username = update_data['username']
            print('username', username)
            use_language = update_data["use_language"]
            lable = update_data["lable"]
            IMEI1 = update_data["IMEI1"]
            IMEI2 = update_data["IMEI2"]
            IMSI = update_data["IMSI"]
            MAC = update_data["MAC"]
            live_pro = update_data["live_pro"]
            live_city = update_data["live_city"]
            live_region = update_data["live_region"]
            live_poi = update_data["live_poi"]
            job_pro = update_data["job_pro"]
            job_city = update_data["job_city"]
            job_region = update_data["job_region"]
            job_poi = update_data["job_poi"]
            time_zones = update_data["time_zones"]
            app_name=update_data["app_name"]
            packages_name = update_data["packages_name"]
            Install_state = update_data["Install_state"]
            first_install_time = update_data["first_install_time"]
            end_install_time = update_data["end_install_time"]
            uninstall_number = update_data["uninstall_number"]
            active_time = update_data["active_time"]

            print('*********************', username, live_city, IMSI, IMEI2, MAC, live_pro,active_time)
            sql2 = 'UPDATE virtual_currency SET phone="{0}",IMEI1="{1}",IMEI2="{2}",IMSI="{3}",MAC="{4}",live_pro="{5}",live_city="{6}",live_region="{7}",live_poi="{8}",job_pro="{9}",job_city="{10}",job_region="{11}",job_poi="{12}",lable="{13}",use_language="{14}",time_zones="{15}",app_name="{16}",packages_name="{17}",Install_state="{18}",first_install_time="{19}",end_install_time="{20}",uninstall_number="{21}",active_time="{22}" WHERE phone = "{23}"'.format(
                username, IMEI1, IMEI2, IMSI, MAC, live_pro, live_city, live_region, live_poi, job_pro, job_city,
                job_region, job_poi, lable,use_language, time_zones, app_name,packages_name,Install_state,first_install_time,end_install_time,uninstall_number,active_time,username)

            total_info = mysqlutil.updateOperation(sql2)
            print(total_info)
            if total_info == 1:
                success = True
            else:
                success = False
            print("更新数据", success)

    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': 1, 'success': success}, ensure_ascii=False))


#######################
# 查询（高级/简单）
#######################
# 加入时间段查询
def all_Query(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)

    if request.method == 'GET':
        page = request.GET.get("page")
        print(page)
        limit = request.GET.get("limit")
        username = request.GET.get("username")
        use_language = request.GET.get("use_language")
        lable = request.GET.get("lable")
        IMEI1 = request.GET.get("IMEI1")
        IMEI2 = request.GET.get("IMEI2")
        IMSI = request.GET.get("IMSI")
        MAC = request.GET.get("MAC")
        live_pro = request.GET.get("live_pro")
        live_city = request.GET.get("live_city")
        live_region = request.GET.get("live_region")
        live_poi = request.GET.get("live_poi")
        job_pro = request.GET.get("job_pro")
        job_city = request.GET.get("job_city")
        job_region = request.GET.get("job_region")
        job_poi = request.GET.get("job_poi")
        time_zones = request.GET.get("time_zones")
        app_name = request.GET.get("app_name")
        packages_name = request.GET.get("packages_name")
        Install_state = request.GET.get("Install_state")
        first_install_time = request.GET.get("first_install_time")
        end_install_time = request.GET.get("end_install_time")
        uninstall_number = request.GET.get("uninstall_number")
        active_time = request.GET.get("active_time")
        upload_name = request.GET.get("upload_name")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        active_start=request.GET.get("active_start")
        active_end=request.GET.get("active_end")
        print('*************************************', active_start, active_end)
        first_install_start=request.GET.get("first_install_start")
        first_install_end=request.GET.get("first_install_end")
        end_install_start=request.GET.get("end_install_start")
        end_install_end=request.GET.get("end_install_end")
        print(first_install_start,first_install_end,end_install_start,end_install_end)

        if start_time == '':
            start = ''
            end = ''
        else:
            b = '00:00:00'
            a = start_time + ' '
            start = (a + b)
            d = '23:59:59'
            c = end_time + ' '
            end = (c + d)
            # end="'"+(c+d)+"'"
        if active_start == '':
            active_start = ''
            active_end = ''
        else:
            b = '00:00:00'
            a = active_start + ' '
            active_start = (a + b)
            d = '23:59:59'
            c = active_end + ' '
            active_end = (c + d)
            # end="'"+(c+d)+"'"
            print(active_start)
        if first_install_start == '':
            first_install_start = ''
            first_install_end = ''
        else:
            b = '00:00:00'
            a = first_install_start + ' '
            first_install_start= (a + b)
            d = '23:59:59'
            c = first_install_end + ' '
            first_install_end = (c + d)
            # end="'"+(c+d)+"'"
            print(active_start)
        if end_install_start == '':
            end_install_start = ''
            end_install_end = ''
        else:
            b = '00:00:00'
            a = end_install_start + ' '
            end_install_start= (a + b)
            d = '23:59:59'
            c = end_install_end + ' '
            end_install_end = (c + d)
            # end="'"+(c+d)+"'"
            print(active_start)
        print('^^^^^',first_install_start,first_install_end,end_install_start,end_install_end)
    data = {
        "userId": '1',
        "username": username,
        "use_language": use_language,
        "lable": lable,
        "IMEI1": IMEI1,
        "IMEI2": IMEI2,
        "IMSI": IMSI,
        "MAC": MAC,
        "live_pro": live_pro,
        "live_city": live_city,
        "live_region": live_region,
        "live_poi": live_poi,
        "job_pro": job_pro,
        "job_city": job_city,
        "job_region": job_region,
        "job_poi": job_poi,
        "time_zones": time_zones,
        "app_name": app_name,
        "packages_name": packages_name,
        "Install_state": Install_state,
        "first_install_time": first_install_time,
        "end_install_time": end_install_time,
        "uninstall_number": uninstall_number,
        "active_time": active_time,
        "upload_name": upload_name,
        "start": start,
        "end": end,
        "active_start":active_start,
        "active_end":active_end,
        "first_install_start":first_install_start,
        "first_install_end":first_install_end,
        "end_install_start":end_install_start,
        "end_install_end":end_install_end,
    }
    print("data", data)
    print(data["username"], data["use_language"], data["lable"],
        data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],
        data["live_pro"], data["live_city"],
        data["live_region"], data["live_poi"], data["job_pro"],
        data["job_city"], data["job_region"], data["job_poi"],
        data["time_zones"], data["app_name"],data["packages_name"],
        data["Install_state"],data["first_install_time"],data["end_install_time"],
        data["uninstall_number"],data["active_time"],
        data["upload_name"], data["start"], data["end"])
    # print('zaizheli****************************:',type(data['username']))

    # select='select * from huaian where (phone="{0}" or "{0}"="") and (IMEI1="{1}" or "{1}"="")'.format(data["username"], data["IMEI1"])
    # select = "select * from virtual_currency where (phone='{0}' or '{0}'='') and (use_language='{1}' or '{1}'='') and (lable ='{2}' or '{2}'='') and (IMEI1 ='{3}' or '{3}'='')" \
    #          " and (IMEI2 ='{4}' or '{4}'='') and (IMSI ='{5}' or '{5}'='') and (MAC ='{6}' or '{6}'='') and (live_pro ='{7}' or '{7}'='')" \
    #          " and (live_city ='{8}' or '{8}'='') and (live_region ='{9}' or '{9}'='') and (live_poi ='{10}' or '{10}'='')" \
    #          " and (job_pro ='{11}' or '{11}'='') and (job_city ='{12}' or '{12}'='') and (job_region ='{13}' or '{13}'='') and (job_poi ='{14}' or '{14}'='')" \
    #          " and (time_zones ='{15}' or '{15}'='') and (app_name ='{16}' or '{16}'='') and (packages_name ='{17}' or '{17}'='') and (Install_state ='{18}' or '{18}'='') and (first_install_time ='{19}' or '{19}'='')" \
    #          " and (end_install_time='{20}' or '{20}'='') and (uninstall_number ='{21}' or '{21}'='') and (active_time ='{22}' or '{22}'='') and (upload_name ='{23}' or '{23}'='')  and upload_time in (select upload_time from virtual_currency where upload_time between '{24}' and '{25}')" \
    #          " and upload_time in (select upload_time from virtual_currency where upload_time between '{26}' and '{27}')".format(
    #     data["username"], data["use_language"], data["lable"],
    #     data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],
    #     data["live_pro"], data["live_city"],
    #     data["live_region"], data["live_poi"], data["job_pro"],
    #     data["job_city"], data["job_region"], data["job_poi"],
    #     data["time_zones"], data["app_name"],data["packages_name"],
    #     data["Install_state"],data["first_install_time"],data["end_install_time"],
    #     data["uninstall_number"],data["active_time"],
    #     data["upload_name"], data["start"], data["end"],data["active_start"],data["active_end"])

    select = "select * from virtual_currency where (phone='{0}' or '{0}'='') and (use_language='{1}' or '{1}'='') and (lable ='{2}' or '{2}'='') and (IMEI1 ='{3}' or '{3}'='')" \
             " and (IMEI2 ='{4}' or '{4}'='') and (IMSI ='{5}' or '{5}'='') and (MAC ='{6}' or '{6}'='') and (live_pro ='{7}' or '{7}'='')" \
             " and (live_city ='{8}' or '{8}'='') and (live_region ='{9}' or '{9}'='') and (live_poi ='{10}' or '{10}'='')" \
             " and (job_pro ='{11}' or '{11}'='') and (job_city ='{12}' or '{12}'='') and (job_region ='{13}' or '{13}'='') and (job_poi ='{14}' or '{14}'='')" \
             " and (time_zones ='{15}' or '{15}'='') and (app_name ='{16}' or '{16}'='') and (packages_name ='{17}' or '{17}'='') and (Install_state ='{18}' or '{18}'='')" \
             " and (uninstall_number ='{19}' or '{19}'='') and (upload_name ='{20}' or '{20}'='')" \
             " and upload_time in (select upload_time from virtual_currency where upload_time between '{21}' and '{22}')" \
             " and active_time in (select active_time from virtual_currency where active_time between '{23}' and '{24}')" \
             " and first_install_time in (select first_install_time from virtual_currency where first_install_time between '{25}' and '{26}')" \
             " and end_install_time in (select end_install_time from virtual_currency where end_install_time between '{27}' and '{28}')".format(
        data["username"], data["use_language"], data["lable"],
        data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],
        data["live_pro"], data["live_city"],
        data["live_region"], data["live_poi"], data["job_pro"],
        data["job_city"], data["job_region"], data["job_poi"],
        data["time_zones"], data["app_name"], data["packages_name"],
        data["Install_state"],
        data["uninstall_number"],
        data["upload_name"], data["start"], data["end"], data["active_start"], data["active_end"],
        data["first_install_start"],data["first_install_end"],data["end_install_start"],data["end_install_end"])
    #select1="select * from virtual_currency where first_install_time in (select first_install_time from virtual_currency where first_install_time between '{0}' and '{1}')".format('2017-10-28 00:14:25','2017-10-29 00:14:25')
    #select1="select * from virtual_currency where end_install_time in (select end_install_time from virtual_currency where end_install_time between '{0}' and '{1}')".format('2018-03-01 00:14:25','2018-03-29 00:14:25')
    result_data = []
    total_info = mysqlutil.queryOperation(select)
    print('_____________________________________', total_info)
    for j in range(0, len(total_info)):
        result_data.append(
            {
                "userId": j,
                # "page": page,
                # "limit": limit,
                "username": total_info[j][0],
                "IMEI1": total_info[j][1],
                "IMEI2": total_info[j][2],
                "IMSI": total_info[j][3],
                "MAC": total_info[j][4],
                "live_pro": total_info[j][5],
                "live_city": total_info[j][6],
                "live_region": total_info[j][7],
                "live_poi": total_info[j][8],
                "job_pro": total_info[j][9],
                "job_city": total_info[j][10],
                "job_region": total_info[j][11],
                "job_poi": total_info[j][12],
                "use_language": total_info[j][13],
                "time_zones": total_info[j][14],
                "lable": total_info[j][15],
                "app_name":total_info[j][16],
                "packages_name":total_info[j][17],
                "Install_state": total_info[j][18],
                "first_install_time": total_info[j][19],
                "end_install_time":total_info[j][20],
                "uninstall_number": total_info[j][21],
                "active_time": total_info[j][22],
                "upload_name": total_info[j][23],
                "upload_time": total_info[j][24],
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
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},
                   default=str))  # 'count': len(total_info),


#######################
# 插入excel文件(上传人，上传时间)
#######################
def all_InsertExcel_u(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    upload_name = request.POST.get('upload_name')
    print('dafda', upload_name)

    datetime01 = datetime.datetime.now()
    time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
    print(time)
    excel_file = request.FILES.get('file')  # 获取前端上传的文件
    print('*******************', excel_file)
    file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        book = xlrd.open_workbook(filename=None, file_contents=excel_file.read())

        sheets = book.sheet_names()  # 获取所有sheet表名  s`  q
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print("11111", row_num)
        list = []  # 定义列表用来存放数据
        count = 0
        false_number = 0
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = {row_data[0], row_data[1], row_data[2], row_data[3],
                     row_data[4], row_data[5], row_data[6], row_data[7],
                     row_data[8], row_data[9], row_data[10], row_data[11],
                     row_data[12], row_data[13], row_data[14], row_data[15],
                     row_data[16], row_data[17], row_data[18], row_data[19],
                     row_data[20], row_data[21], row_data[22],
                     }  # 选择获取第几列
            print(time, upload_name)
            sql = "insert into virtual_currency(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,lable,use_language,time_zones,app_name,packages_name,Install_state,first_install_time,end_install_time,uninstall_number,active_time,upload_name,upload_time)" \
                  " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  % (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6],
                     row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12],
                     row_data[13], row_data[14], row_data[15], row_data[16], row_data[17], row_data[18], row_data[19],
                     row_data[20], row_data[21], row_data[22],  upload_name, time)
            print("22222", value)
            total_info = mysqlutil.insertOperation(sql)
            print(total_info)
            list.append(value)  # 将数据暂存在列表

            if total_info == 1:
                count += 1
                print('true', count)
            else:
                false_number += 1
                print('false', false_number)

            # print(i)
        list_len = len(list)
        print("list", list_len)
        if count == list_len:
            success = True
        elif false_number == list_len:
            success = False
        else:
            success = 'other!'
        print(success)
        return HttpResponse(json.dumps(
            {'code': 0, 'msg': '', 'count': list_len, 'true_number': count, 'false_number': false_number,
             'success': success}, ensure_ascii=False))


