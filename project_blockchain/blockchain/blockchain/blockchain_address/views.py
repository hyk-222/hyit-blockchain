import json

from django.shortcuts import render

# Create your views here.
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse, JsonResponse


def address(request):
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    # if request.method == 'GET':
    address = 'bc1qsnyclsxswgfq9t6yluelhmz6ynvmcgj7qsg82k'
    sql1 = "SELECT DISTINCT bitcoin_inputs.recipient 'input'FROM `bitcoin_inputs`,bitcoin_outputs,bitcoin_transactions WHERE  " \
           "bitcoin_inputs.spending_transaction_hash = bitcoin_outputs.transaction_hash AND " \
           "bitcoin_outputs.transaction_hash = bitcoin_transactions.`hash` and bitcoin_outputs.recipient = '{" \
           "0}'".format(address)
    input_list = []
    input = mysqlutil.queryOperation(sql1)
    for i in input:
        input_list.append(i[0])
    total_input = 0
    data = []
    for i in input_list:
        print(i)
        rec_address = i
        sql2 = "SELECT sum(value)*POWER(10,-8) from bitcoin_outputs where recipient='{0}'".format(rec_address)
        sql3 = "SELECT time from bitcoin_outputs where recipient='{0}'".format(rec_address)
        input_value = mysqlutil.queryOperation(sql2)
        input_value = mysqlutil.queryOperation(sql3)
        total_input += input_value[0][0]
        data.append({
            'input_address': i,
            'input_total': input_value[0][0],
            'time':i,
        })

    return HttpResponse(json.dumps({'address': data}))


def address_search(request):

    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    sql1 = "SELECT bitcoin_inputs.recipient 'input',bitcoin_inputs.transaction_hash 'pro_transaction', " \
           "bitcoin_inputs.spending_transaction_hash 'loc_transaction'FROM `bitcoin_inputs`,bitcoin_outputs," \
           "bitcoin_transactions WHERE  bitcoin_inputs.spending_transaction_hash = bitcoin_outputs.transaction_hash " \
           "AND bitcoin_outputs.transaction_hash = bitcoin_transactions.`hash` and bitcoin_outputs.recipient = " \
           "'1MhNkiqBqjjszBWduZ5ZiZkyHuQPRrGhnJ' "
    sql2 = "SELECT spending_transaction_hash from bitcoin_inputs WHERE transaction_hash = '{0}'".format(loc_hash)
    data = []
    data = mysqlutil.queryOperation(sql1)
    print(data)
    return HttpResponse(json.dumps({'address': 1}))