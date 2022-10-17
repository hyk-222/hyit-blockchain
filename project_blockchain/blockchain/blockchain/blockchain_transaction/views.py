import json
import datetime

from django.shortcuts import render

# Create your views here.
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse, JsonResponse


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def transaction_pre_query(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        get_hash = request.GET.get('txid')
    # get_hash = "31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb"
    """
    向前查询
    """
    sql = "SELECT updata_inputs.transaction_hash 'pre_hash',updata_inputs.output_value * POWER(10,-8) 'input_value',updata_inputs.recipient 'input_address',updata_inputs.spending_index " \
          "From updata_inputs where updata_inputs.spending_transaction_hash='{0}'".format(get_hash)
    pre_info_list = mysqlutil.queryOperation(sql)
    data = []
    if pre_info_list:
        for pre_info in pre_info_list:
            hash_dict = {
                'pre_hash': pre_info[0],
                'value': pre_info[1],
                'input_address': pre_info[2],
            }
            data.append(hash_dict)

    return HttpResponse(json.dumps({'data': data}))


def transaction_next_query(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        get_hash = request.GET.get('txid')
        """
        向后查询
        """
        sql1 = "select updata_outputs.recipient 'out_address',updata_outputs.output_value * POWER(10,-8) 'out_value' from updata_outputs where transaction_hash='{0}'".format(
            get_hash)
        sql2 = "select  updata_inputs.recipient 'out_address', updata_inputs.spending_transaction_hash 'next_hash', updata_inputs.output_value * POWER(10,-8) 'out_value' " \
               " from updata_inputs,updata_outputs where updata_inputs.transaction_hash=updata_outputs.transaction_hash " \
               "and updata_outputs.output_index =updata_inputs.output_index and updata_outputs.transaction_hash='{0}'".format(
            get_hash)
        next_info_address = mysqlutil.queryOperation(sql1)
        next_info_hash = mysqlutil.queryOperation(sql2)
        data = []
        if next_info_hash:
            for next_info in next_info_hash:
                try:
                    next_hash = next_info[2]
                except:
                    next_hash = ''
                hash_dict = {
                    'output_address': next_info[0],
                    'next_hash': next_info[1],
                    'value': next_info[2],
                }
                data.append(hash_dict)
                print(next_info)

        return HttpResponse(json.dumps({'data': data}))


# 查询目标txid详细信息
def transaction_txid_detail(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        txid = request.GET.get('txid')
    # 输入地址信息
    sql1 = "SELECT updata_inputs.output_time 'input_time',updata_inputs.recipient 'input_address',updata_inputs.output_value * POWER(10,-8) 'output_value'" \
           "From updata_inputs where updata_inputs.spending_transaction_hash= '{0}'".format(txid)
    # 输出地址信息
    sql2 = "SELECT updata_inputs.spending_time 'output_time',updata_inputs.recipient 'output_address',updata_inputs.output_value * POWER(10,-8) 'output_value'" \
           "From updata_inputs where updata_inputs.transaction_hash= '{0}'".format(txid)
    sql3 = "SELECT updata_transactions.fee, updata_transactions.time from updata_transactions WHERE updata_transactions.transaction_hash= '{0}'".format(
        txid)
    inputs = []
    i = 0
    input_value = 0
    for input in mysqlutil.queryOperation(sql1):
        i = {
            'input_time': input[0],
            'input_address': input[1],
            'input_value': input[2],
        }
        input_value += input[2]
        inputs.append(i)
    outputs = []
    output_value = 0
    for output in mysqlutil.queryOperation(sql2):
        i = {
            'output_time': output[0],
            'output_address': output[1],
            'output_value': output[2],
        }
        output_value += output[2]
        outputs.append(i)
    fee_time = mysqlutil.queryOperation(sql3)
    return HttpResponse(json.dumps({
        'input': inputs, 'output': outputs, 'output_total': output_value, 'input_total': input_value, 'fee': fee_time[0],
        'time': fee_time},
        cls=DateEncoder))


# 查询目标地址详细信息
def transaction_address_detail(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        address = request.GET.get('address')
    sql1 = "SELECT updata_inputs.output_value * POWER(10,-8) , updata_inputs.output_time, updata_inputs.spending_time from updata_inputs where updata_inputs.recipient='{}'".format(
        address)
    sql2 = "SELECT updata_outputs.output_value * POWER(10,-8) from updata_outputs where updata_outputs.recipient='{}'".format(
        address)
    input_value = mysqlutil.queryOperation(sql1)
    output_value = mysqlutil.queryOperation(sql2)
    address_data = {
        'input_value': input_value[0][0],
        'output_value': output_value[0][0],
        'balance': input_value[0][0] - output_value[0][0],
        'output_time': input_value[0][1],
        'spending_time': input_value[0][2],
    }
    return HttpResponse(json.dumps(address_data, cls=DateEncoder))


# 输入和输出地址全部信息
def address_all(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    sql1 = "SELECT DISTINCT recipient  'in_address' FROM updata_inputs limit 500"
    sql2 = "SELECT DISTINCT recipient 'out_address' FROM updata_outputs  limit 500"
    in_addr = mysqlutil.queryOperation(sql1)
    out_addr = mysqlutil.queryOperation(sql2)
    addrss_all = {
        'in_addr': in_addr,
        'out_addr': out_addr,
    }
    return HttpResponse(json.dumps(addrss_all, cls=DateEncoder))
