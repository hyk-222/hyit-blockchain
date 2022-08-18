#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : linjie
import json
import datetime


class DateEncoder(json.JSONEncoder):
    '''
    解决 datetime json问题
    '''
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)