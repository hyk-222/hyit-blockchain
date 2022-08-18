#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : linjie
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    '''
    解决decimal json问题
    '''
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)