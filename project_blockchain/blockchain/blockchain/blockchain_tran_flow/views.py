#-*-coding:utf-8-*-
import datetime
import json
import os
import time
import pandas as pd
# Create your views here.
import traceback
import xlwt

import xlrd
from django.core.paginator import Paginator
from fsspec import transaction
from scrapy import settings

from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta

def tans_flow(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)  # 打开数据库连接

#######################
#vpn数据库展示
#######################
def flow_show(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")

    pageIndex = request.GET.get("page")
    print(pageIndex)
    pageSize = request.GET.get("limit")
    print(pageSize)
    sql1 = "SELECT * FROM transaction_flow ORDER BY create_time DESC"
         # sql1 = "SELECT id, `hash`, time FROM bitcoin_test_recently WHERE `hash` = '{0}'".format(get_hash)
    data = []
    total_info = mysqlutil.queryOperation(sql1)

    #print(total_info[1][5])
    for j in range(0,len(total_info)):
        print(total_info[j][1])
        data.append(
            {
                "userId": j,
                "currency_type": total_info[j][0],
                "address": total_info[j][1],
                "time_range": total_info[j][2],
                "trade_direction": total_info[j][3],
                "record_number": total_info[j][4],
                "amount_range":total_info[j][5],
                "create_time": total_info[j][6],
                "create_people": total_info[j][7],

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
                # "upload_name":total_info[j][16],
                # "upload_time": total_info[j][17],
            }
        )
        print(data)
    res=[]
    pageInator = Paginator(data, pageSize)
    context = pageInator.page(pageIndex)
    dataCount = len(data)
    for item in context:
        res.append(item)
    #print(res)
    print(dataCount)



    print(type(data))
    return HttpResponse(
        json.dumps({'code': 0, 'msg': '', 'count': len(total_info), 'data': res},default=str))  # 'count': len(total_info)

def to_view(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)

    pageIndex = request.GET.get("page")
    # print("1111111111111",pageIndex)
    pageSize = request.GET.get("limit")
    create_time = request.GET.get("create_time")
    print(create_time)
    trade_direction=request.GET.get("trade_direction")
    print(trade_direction)
    #以创建时间查询文件
    create_time=str(create_time)
    create_time_str=create_time[0:10]+create_time[11:13]+create_time[14:16]+create_time[17:19]
    current_dir = os.path.abspath(os.path.dirname(__file__)) + "\\file_store\\"
   # current_dir = 'D:/blockchain_test/project_blockchain/File_store/'
    file_name=current_dir + "File_"+create_time_str+'.xls'
    print(file_name)
    excel_data = pd.read_excel(file_name)
    one_row_keys = excel_data.keys()  # 读取出来的首行数据
    row_keys = [i for i in one_row_keys]  # 首行遍历形成的列表格式
    sum_rows = excel_data.index.values  # 读取所有行数形成列表
    df_list = []
    print(excel_data.iloc[2, :].to_dict())
    for i in sum_rows:  # 遍历所有行号
        # loc为按列名索引 iloc 为按位置索引，使用的是 [[行号], [列名]]
        row_dict = excel_data.loc[i, row_keys].to_dict()  #
        df_list.append(row_dict)
    #分页
    # print(df_list)
    res = []
    pageInator = Paginator(df_list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': len(df_list), 'data': res},default=str))  # 'count': len(total_info),

def delete_records(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    create_time = request.POST.get('create_time')
    sql_create_time=create_time
    # 以创建时间查询文件
    create_time = str(create_time)
    create_time_str = create_time[0:10] + create_time[11:13] + create_time[14:16] + create_time[17:19]
    current_dir = os.path.abspath(os.path.dirname(__file__)) + "\\file_store\\"
    #current_dir = 'D:/blockchain_test/project_blockchain/File_store/'
    file_name = current_dir + "File_" + create_time_str + '.xls'
    print('有值你就成功咯',file_name)
    if os.path.exists(file_name):  # 如果文件存在
        os.remove(file_name)  # 则删除
    print(sql_create_time)
    sql="delete from transaction_flow where create_time='{0}'".format(sql_create_time)
    total_info = mysqlutil.deleteOperation(sql)
    print(total_info)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'success':True},ensure_ascii=False))

def expore_file(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    data=json.loads(request.body)
    currency_type=int(data['currency_type'])
    print(currency_type)
    time_lable=int(data['time_lable'])
    print(time_lable)
    value_lable=int(data['value_lable'])
    print(value_lable)
    direction_lable=int(data['direction_lable'])
    address=data['address']
    start_time_4=data['start_time']
    end_time_4=data['end_time']
    low_value=float(data['low_value'])*pow(10,8)
    high_value=float(data['high_value'])*pow(10,8)
    # low_value=50000000
    # high_value=110000000
    if currency_type==0:
        currency_type='比特币'
    else:
        print('功能尚未开发！')
        return HttpResponse(json.dumps({'code': 0, 'msg': '只能选择比特币，其他币种功能尚未开发！', 'success': False}, ensure_ascii=False))
    if value_lable == 0:
        low_amount = 0
        high_amount = 10000*pow(10,8)
    elif value_lable==1:
        low_amount = low_value
        high_amount = 10000*pow(10,8)
    elif value_lable==2:
        low_amount=0
        high_amount = high_value
    else:
        low_amount = low_value
        high_amount = high_value
    low_amount=int(low_amount)
    high_amount=int(high_amount)


    print(low_amount, high_amount)
    # 时间范围
    #近半年
    if time_lable == 2:
        end_time = datetime.date.today()
        print(end_time)
        start_time = end_time - relativedelta(months=6)
        print(start_time)
    #近一年
    elif time_lable == 3:
        end_time = datetime.date.today()
        print(end_time)
        start_time = end_time - relativedelta(years=1)

        print(start_time)
    #近一周
    elif time_lable == 0:
        end_time = datetime.date.today()
        print(end_time)
        start_time = end_time - relativedelta(days=7)
        print(start_time)
    #近一月
    elif time_lable == 1:
        end_time = datetime.date.today()
        print(end_time)
        start_time = end_time - relativedelta(days=30)
        print(start_time)
    #自定义
    else:
        end_time = end_time_4
        start_time = start_time_4
    print(type(start_time),end_time)
    end_time=str(end_time)
    start_time=str(start_time)
    conditions = {
        "address": address,
        "start_time": start_time,
        "end_time": end_time,
        "low_amount": low_amount,
        "high_amount": high_amount,
    }
    print(conditions)
    # 流入查询updata_outputs

    current_dir = os.path.abspath(os.path.dirname(__file__)) + "\\file_store\\"
    #current_dir = '.\\File_store\\'
    print(current_dir)
    # current_dir='D:/blockchain_test/project_blockchain/File_store/'
    style_datetme = xlwt.XFStyle()
    style_datetme.num_format_str = 'YYYY-MM-DD hh:mm:ss'
    # style_datetme.num_format_str = 'M/D/YY hh:mm'
    # datetime01.strftime("%Y-%m-%d %H:%M:%S")
    '''
    流入流出分条件查询
    '''
    if direction_lable==0:
        trade_direction='流入'
    else:
        trade_direction = '流出'
    if trade_direction == '流入':
        select1 = "SELECT updata_inputs.recipient,updata_inputs.spending_transaction_hash, updata_inputs.output_time,updata_inputs.output_value*POWER(10,-8),updata_outputs.recipient,updata_outputs.output_value*POWER(10,-8) FROM updata_inputs,updata_outputs " \
                  "where updata_outputs.transaction_hash=updata_inputs.spending_transaction_hash and updata_inputs.spending_transaction_hash in " \
                  "(select transaction_hash from updata_outputs where recipient='{0}') and updata_outputs.recipient='{1}' " \
                  "and spending_time IN (SELECT spending_time FROM updata_inputs WHERE spending_time BETWEEN '{2}' AND '{3}') " \
                  "AND updata_inputs.output_value IN ( SELECT updata_inputs.output_value FROM updata_inputs WHERE updata_inputs.output_value BETWEEN '{4}' AND '{5}')".format(
            conditions["address"], conditions["address"], conditions["start_time"], conditions["end_time"],
            conditions["low_amount"], conditions["high_amount"])
        L = ('发送方地址', 'TXID', '流入时间', '发送金额', '统计地址', '流入金额')  # 将列名称定义

        total_info = mysqlutil.queryOperation(select1)
        print(total_info)
        # L=cursor.description
        print(type(L))
        fields = [field for field in L]

        print(fields)

        record_number = len(total_info)
        print(len(total_info))
        print(total_info)
        # 写入excel
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')

        for col, field in enumerate(fields):
            sheet.write(0, col, field)
        row = 1
        for data in total_info:
            for col, field in enumerate(data):
                if col == 2:
                    sheet.write(row, col, field, style_datetme)
                else:
                    sheet.write(row, col, field)
            row += 1
        datetime01 = datetime.datetime.now()
        file_index = datetime01.strftime("%Y-%m-%d%H%M%S")
        file_name = current_dir + "File_" + "%s.xls" % file_index
        book.save(current_dir + "File_" + "%s.xls" % file_index)
        print("Export to excel success!")
        time_range = str(start_time[0:10]) + '——' + str(end_time[0:10])
        print(time_range)
        # datetime01 = datetime.datetime.now()
        create_time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
        print(create_time)
        create_people = '李四'

        if record_number > 0:
            low_amount = low_amount * pow(10, -8)
            high_amount = high_amount * pow(10, -8)
            amount_range = str(low_amount) + '~' + str(high_amount)
            massage = {
                "currency_type": currency_type,
                "address": address,
                "time_range": time_range,
                "trade_direction": trade_direction,
                "amount_range": amount_range,
                "record_number": record_number,
                "create_time": create_time
            }
            print(massage)
            # 如果文件导出成功，将相关信息插入数据表
            sql = "insert into transaction_flow(currency_type,address,time_range,trade_direction,amount_range,record_number,create_time,create_people) values('%s','%s','%s','%s','%s','%s','%s','%s')" \
                % (currency_type,address,time_range,trade_direction,amount_range,record_number,create_time,create_people)
            mysqlutil.insertOperation(sql)
            print('信息插入成功！')
            return HttpResponse(json.dumps({'code': 0, 'msg': '查询到记录并插入成功', 'success': True}, ensure_ascii=False))
        else:
            print('未查询到符合条件的记录！')
            os.remove(file_name)
            return HttpResponse(json.dumps({'code': 1, 'msg': '未查询到符合条件的记录！', 'success': True}, ensure_ascii=False))
    # 流出查询updata_inputs表
    else:
        select2 = "SELECT updata_inputs.recipient,updata_inputs.spending_transaction_hash, updata_inputs.output_time,updata_inputs.output_value*POWER(10,-8),updata_outputs.recipient,updata_outputs.output_value*POWER(10,-8) FROM updata_inputs,updata_outputs " \
                  "where updata_outputs.transaction_hash=updata_inputs.spending_transaction_hash and " \
                  "updata_outputs.transaction_hash in (select spending_transaction_hash from updata_inputs where recipient='{0}') " \
                  "and updata_inputs.recipient='{1}'and updata_outputs.output_time IN (SELECT output_time FROM updata_outputs WHERE output_time BETWEEN '{2}' AND '{3}')" \
                  "AND updata_outputs.output_value IN ( SELECT output_value FROM updata_outputs WHERE output_value BETWEEN '{4}' AND '{5}' )".format(
            conditions["address"], conditions["address"], conditions["start_time"], conditions["end_time"],
            conditions["low_amount"], conditions["high_amount"])
        L = ('统计地址', 'TXID', '流出时间', '流出金额', '接收方地址', '接收金额')  # 将列名称定义
        total_info1 = mysqlutil.queryOperation(select2)
        # L=cursor.description
        print(type(L))
        print(L)
        fields = [field for field in L]

        print(fields)
        record_number = len(total_info1)
        print(len(total_info1))
        print(total_info1)
        # 写入excel
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')

        for col, field in enumerate(fields):
            sheet.write(0, col, field)
        row = 1
        for data in total_info1:
            for col, field in enumerate(data):
                if col == 2:
                    sheet.write(row, col, field, style_datetme)
                else:
                    sheet.write(row, col, field)
            row += 1
        datetime01 = datetime.datetime.now()
        file_index = datetime01.strftime("%Y-%m-%d%H%M%S")
        file_name = current_dir + "File_" + "%s.xls" % file_index
        book.save(current_dir + "File_" + "%s.xls" % file_index)
        print("Export to excel success!")
        time_range = str(start_time[0:10]) + '——' + str(end_time[0:10])
        print(time_range)
        # datetime01 = datetime.datetime.now()
        create_time = datetime01.strftime("%Y-%m-%d %H:%M:%S")
        print(create_time)
        create_people = '李四'
        if record_number > 0:
            low_amount = low_amount * pow(10, -8)
            high_amount = high_amount * pow(10, -8)
            amount_range = str(low_amount) + '~' + str(high_amount)
            # 如果文件导出成功，将相关信息插入数据表
            sql = "insert into transaction_flow(currency_type,address,time_range,trade_direction,amount_range,record_number,create_time,create_people) values('%s','%s','%s','%s','%s','%s','%s','%s')" \
                 % (currency_type,address,time_range,trade_direction,amount_range,record_number,create_time,create_people)
            mysqlutil.insertOperation(sql)
            print('信息插入成功！')
            return HttpResponse(json.dumps({'code': 0, 'msg': '查询到记录并插入成功', 'success': True}, ensure_ascii=False))
        else:
            print('未查询到符合条件的记录！')
            os.remove(file_name)
            return HttpResponse(json.dumps({'code': 1, 'msg': '未查询到符合条件的记录！', 'success': True}, ensure_ascii=False))


