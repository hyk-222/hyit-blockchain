import json
import datetime
from django.shortcuts import render
from .utils import mysqldb
from .utils.mysqldb import MySQL_util
from django.http import HttpResponse, JsonResponse


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def pre_address(request):
    """
    查询流入交易地址
    """
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        address = request.GET.get('address')
        # address = '1DZTzaBHUDM7T3QvUKBz4qXMRpkg8jsfB5'
        sql1 = "SELECT updata_inputs.recipient 'input',updata_inputs.spending_time'time', updata_inputs.output_value * POWER(10,-8)  'value' " \
               "FROM updata_inputs WHERE updata_inputs.transaction_hash IN (SELECT updata_inputs.transaction_hash 'input'" \
               "FROM updata_inputs WHERE recipient = '{}')ORDER BY input".format(address)
        data = mysqlutil.queryOperation(sql1)
        start = 0
        end = 0
        c = len(data)
        detail = []
        for i in range(c):
            while i == 0:
                address = data[i][0]
                break
            if data[i][0] == address:
                end = end + 1
                if i == c - 1:
                    detail.append({'address': address,
                                   'data': data[start:end],
                                   'count': len(data[start:end])
                                   })
            else:
                detail.append({'address': address,
                               'data': data[start:end],
                               'count': len(data[start:end])
                               })
                address = data[i][0]
                start = end
                end = end + 1
                if i == c - 1:
                    detail.append({'address': address,
                                   'data': data[start:end],
                                   'count': len(data[start:end])
                                   })
        print(detail)

        return HttpResponse(json.dumps(detail, cls=DateEncoder))


def next_address(request):
    """
        查询流出交易地址
        """
    mysqlutil = MySQL_util(mysqldb.mysql_conf)
    if request.method == 'GET':
        address = request.GET.get('address')
        sql1 = "SELECT updata_inputs.recipient 'output',updata_inputs.spending_time'time', updata_inputs.output_value * POWER(10,-8)  'value' " \
               "FROM updata_inputs WHERE updata_inputs.transaction_hash IN (SELECT updata_inputs.spending_transaction_hash 'output'" \
               "FROM updata_inputs WHERE recipient = '{}')ORDER BY output".format(address)
        data = mysqlutil.queryOperation(sql1)
        start = 0
        end = 0
        c = len(data)
        detail = []
        for i in range(c):
            while i == 0:
                address = data[i][0]
                break
            if data[i][0] == address:
                end = end + 1
                if i == c - 1:
                    detail.append({'address': address,
                                   'data': data[start:end],
                                   'count': len(data[start:end])
                                   })
            else:
                detail.append({'address': address,
                               'data': data[start:end],
                               'count': len(data[start:end])
                               })
                address = data[i][0]
                start = end
                end = end + 1
                if i == c - 1:
                    detail.append({'address': address,
                                   'data': data[start:end],
                                   'count': len(data[start:end])
                                   })
        print(detail)
        return HttpResponse(json.dumps(detail, cls=DateEncoder))
