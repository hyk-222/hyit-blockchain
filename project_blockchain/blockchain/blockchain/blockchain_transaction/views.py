import json

from django.shortcuts import render

# Create your views here.
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse, JsonResponse


def transaction_analysis(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        get_hash = request.GET.get("info")
        print(get_hash)
        """
        先前哈希查询
        """
        prehash_list = []  # 来源hash
        n = 0
        for u in range(0):
            if prehash_list:
                for i in range(len(prehash_list)):
                    hash = prehash_list[n]
                    sql2 = "SELECT bitcoin_inputs.transaction_hash 'pre_transaction' " \
                           "FROM bitcoin_inputs,bitcoin_outputs,bitcoin_transactions " \
                           "WHERE  bitcoin_inputs.spending_transaction_hash = bitcoin_outputs.transaction_hash " \
                           "AND bitcoin_outputs.transaction_hash = bitcoin_transactions.`hash` " \
                           "and bitcoin_transactions.hash = '{0}'".format(hash)
                    pre_hash = mysqlutil.queryOperation(sql2)
                    if pre_hash:
                        n += len(pre_hash)
                        for y in range(len(pre_hash)):
                            prehash_list.append(pre_hash[y][0])
                        print('i=', i)
                        print('n=', n)
                    else:
                        print("未查询到！")
                        break
            else:
                sql1 = "SELECT bitcoin_inputs.transaction_hash 'pre_transaction' FROM bitcoin_inputs,bitcoin_outputs,bitcoin_transactions WHERE  bitcoin_inputs.spending_transaction_hash = bitcoin_outputs.transaction_hash " \
                       "AND bitcoin_outputs.transaction_hash = bitcoin_transactions.`hash` " \
                       "and bitcoin_transactions.hash = '{0}'".format(get_hash)
                pre_hash = mysqlutil.queryOperation(sql1)
                n = len(pre_hash) - 1
                print('11n=', n)
                for i in range(len(pre_hash)):
                    prehash_list.append(pre_hash[i][0])
        # print(prehash_list)
        """
        通过哈希向后查询交易信息
        """
        sql3 = "SELECT spending_transaction_hash as next_hash from bitcoin_inputs WHERE transaction_hash = '{0}'".format(
            get_hash)
        nexthash_list = []
        b = 0
        for u in range(2):
            if nexthash_list:
                for i in range(len(nexthash_list)):
                    hash = nexthash_list[b]
                    sql4 = "SELECT spending_transaction_hash from bitcoin_inputs WHERE recipient = '{0}'".format(hash)
                    next_hash = mysqlutil.queryOperation(sql4)
                    if next_hash:
                        for i in next_hash:
                            nexthash_list.append(i[0])
                        b += 1
                    else:
                        print("暂无下一级地址")
                        break
            else:
                next_hash = mysqlutil.queryOperation(sql3)
                for i in next_hash:
                    nexthash_list.append(i[0])
        # print(nexthash_list)
        """
        查询当前哈希的输出地址
        """
        b = 0
        data = []
        for i in nexthash_list:
            hash = i
            sql5 = " SELECT recipient from bitcoin_outputs where transaction_hash ='{0}'".format(hash)
            recipient = mysqlutil.queryOperation(sql5)
            if len(recipient) >= 1:
                for a in recipient:
                    data.append({
                        'index': b,
                        'hash_value': hash,
                        'recipient_address': a[0],
                    })
            else:
                print("无")
            b += 1
        # print(data)
        return HttpResponse(json.dumps({'data': data}))


def transaction_search(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        get_hash = request.GET.get("hash_query")
        print(get_hash)
        sql1 = "SELECT `hash`, input_total*POWER(10,-8), output_total*POWER(10,-8),fee*POWER(10,-8), time FROM bitcoin_transactions WHERE `hash` = '{0}'".format(
            get_hash)
        data = []
        total_info = mysqlutil.queryOperation(sql1)
        # 交易哈希号及总输入输出值、时间
        # 当前交易的输入输出地址及其金额
        sql2 = "SELECT bitcoin_inputs.recipient 'out_address',bitcoin_inputs.`value`*POWER(10,-8) 'out_value' from bitcoin_inputs where spending_transaction_hash='{0}'".format(
            get_hash)
        input_info = mysqlutil.queryOperation(sql2)
        input_list = []
        for i in input_info:
            sql4 = "SELECT transaction_hash from bitcoin_inputs WHERE recipient='{}' AND spending_transaction_hash='{}'".format(i[0], get_hash)
            pre_hash_info = mysqlutil.queryOperation(sql4)
            print(pre_hash_info[0][0])
            input_list.append({'address': i[0], 'value': i[1], 'pre_hash': pre_hash_info[0][0]})

        output_list = []
        sql3 = "select bitcoin_outputs.recipient 'out_address',bitcoin_outputs.value*POWER(10,-8) 'out_value' from bitcoin_outputs where transaction_hash='{0}'".format(
            get_hash)
        sql5 = "select bitcoin_outputs.recipient 'pro_outadd',bitcoin_outputs.value*POWER(10,-8) 'input_value',bitcoin_inputs.spending_transaction_hash 'next_hash'" \
               " from bitcoin_inputs,bitcoin_outputs where bitcoin_inputs.transaction_hash=bitcoin_outputs.transaction_hash and bitcoin_outputs.index =bitcoin_inputs.index and bitcoin_outputs.transaction_hash='{0}'".format(
            get_hash)
        next_info_address = mysqlutil.queryOperation(sql3)
        next_info_hash = mysqlutil.queryOperation(sql5)
        if next_info_hash:
            output_list = []
            for next_info in list(zip(next_info_address, next_info_hash))[0]:
                print(next_info)
                try:
                    next_hash = next_info[2]
                except:
                    next_hash = ''
                hash_dict = {
                    'output_address': next_info[0],
                    'value': next_info[1],
                    'next_hash': next_hash,
                    'hash': get_hash,
                }
                output_list.append(hash_dict)
        data.append({'hash': total_info[0][0], 'input_total': total_info[0][1], 'output_total': total_info[0][2],
                     'fee': total_info[0][3], 'time': total_info[0][4],
                     'input': input_list, 'output': output_list})
        return HttpResponse(json.dumps({'data': data}))
    else:
        print("未查询到")

    # mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # get_hash = '31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb'
    # sql1 = "SELECT `hash`, input_total*POWER(10,-8), output_total*POWER(10,-8),fee*POWER(10,-8), time FROM bitcoin_transactions WHERE `hash` = '{0}'".format(get_hash)
    # data = []
    # total_info = mysqlutil.queryOperation(sql1)

    # data.append({'hash': total_info[0][0], 'input_total':total_info[0][1], 'output_total': total_info[0][2], 'fee': total_info[0][3], 'time': total_info[0][4]})
    # # ({'input': input_list, 'output': output_list})
    # print(data)
    # return HttpResponse(json.dumps({'data': data}))

    # mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    #     get_hash = request.GET.get("hash_query")
    #     print(get_hash)
    #     sql1 = "SELECT `hash`, input_total*POWER(10,-8), output_total*POWER(10,-8),fee*POWER(10,-8), time FROM bitcoin_transactions WHERE `hash` = '{0}'".format(
    #         get_hash)
    #     data = []
    #     total_info = mysqlutil.queryOperation(sql1)
    #     # 交易哈希号及总输入输出值、时间
    #     # 当前交易的输入输出地址及其金额
    #     sql2 = "SELECT bitcoin_inputs.recipient 'out_address',bitcoin_inputs.`value`*POWER(10,-8) 'out_value' from bitcoin_inputs where spending_transaction_hash='{0}'".format(
    #         get_hash)
    #     sql3 = "SELECT bitcoin_outputs.recipient 'out_address',bitcoin_outputs.`value`*POWER(10,-8) 'out_value' from bitcoin_outputs where transaction_hash='{0}'".format(
    #         get_hash)
    #     input_info = mysqlutil.queryOperation(sql2)
    #     input_list = []
    #     for i in input_info:
    #         input_list.append({'address': i[0], 'value': i[1]})
    #     output_info = mysqlutil.queryOperation(sql3)
    #     output_list = []
    #     for i in output_info:
    #         output_list.append({'address': i[0], 'value': i[1]})
    #     data.append({'hash': total_info[0][0], 'input_total': total_info[0][1], 'output_total': total_info[0][2],
    #                  'fee': total_info[0][3], 'time': total_info[0][4],
    #                  'input': input_list, 'output': output_list})
    #     return HttpResponse(json.dumps({'data': data}))
    # else:
    #     print("未查询到")


def transaction_search_input(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    get_hash = '31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb'
    data = []
    # 当前交易的输入地址及其金额
    sql2 = "SELECT bitcoin_inputs.recipient 'out_address',bitcoin_inputs.`value`*POWER(10,-8) 'out_value' from bitcoin_inputs where spending_transaction_hash='{0}'".format(
        get_hash)
    input_info = mysqlutil.queryOperation(sql2)
    input_list = []
    for i in input_info:
        input_list.append({'address': i[0], 'value': i[1]})
    data.append(input_list)  # data.append({'input': input_list})
    print(data)
    return HttpResponse(json.dumps({'code': 0, 'data': data}))


def transaction_search_output(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'POST':
        get_phone = request.POST.get('username')
    get_hash = '31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb'
    data = []
    # 当前交易的输出地址及其金额
    sql3 = "SELECT bitcoin_outputs.recipient 'out_address',bitcoin_outputs.`value`*POWER(10,-8) 'out_value' from bitcoin_outputs where transaction_hash='{0}'".format(
        get_hash)
    output_info = mysqlutil.queryOperation(sql3)
    output_list = []
    for i in output_info:
        output_list.append({'address': i[0], 'value': i[1]})
    data.append(output_list)  # data.append({'output': output_list})
    print(data)
    return HttpResponse(json.dumps({'code': 0, 'msg': '', 'count': 2, 'data': data}))
# def address_search_input(request):


def transaction_pre_query(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        get_hash = request.GET.get('txid')
    # get_hash = "31999c6bd7024d7c2cf04fb0bc2fe536d07d8eb7a9828c5b52229209d3727cdb"
    """
    向前查询
    """
    sql = "SELECT bitcoin_inputs.transaction_hash 'pre_hash',bitcoin_inputs.value 'input_value',bitcoin_inputs.recipient 'input_address',bitcoin_inputs.spending_index " \
          "From bitcoin_inputs where bitcoin_inputs.spending_transaction_hash='{0}'".format(get_hash)
    pre_info_list = mysqlutil.queryOperation(sql)
    print(get_hash)
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
        sql1 = "select bitcoin_outputs.recipient 'out_address',bitcoin_outputs.value 'out_value' from bitcoin_outputs where transaction_hash='{0}'".format(
            get_hash)
        sql2 = "select bitcoin_inputs.spending_transaction_hash 'next_hash'" \
               " from bitcoin_inputs,bitcoin_outputs where bitcoin_inputs.transaction_hash=bitcoin_outputs.transaction_hash " \
               "and bitcoin_outputs.index =bitcoin_inputs.index and bitcoin_outputs.transaction_hash='{0}'".format(
            get_hash)
        next_info_address = mysqlutil.queryOperation(sql1)
        next_info_hash = mysqlutil.queryOperation(sql2)
        data = []
        if next_info_hash:
            for next_info in list(zip(next_info_address, next_info_hash)):
                try:
                    next_hash = next_info[1][0]
                except:
                    next_hash = ''
                hash_dict = {
                    'output_address': next_info[0][0],
                    'value': next_info[0][1],
                    'next_hash': next_hash,
                }
                data.append(hash_dict)

        return HttpResponse(json.dumps({'data': data}))