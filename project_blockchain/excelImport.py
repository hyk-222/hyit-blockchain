import traceback

import pymysql
import xlrd

'''
    连接数据库
    args：db_name（数据库名称）
    returns:db

'''


def mysql_link(de_name):
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='bitcoin_database')
        return db
    except:
        print("could not connect to mysql server")


'''
    读取excel函数
    args：excel_file（excel文件，目录在py文件同目录）
    returns：book
'''


def open_excel(excel_file):
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        return book
    except:
        print(traceback.print_exc())
        print("open excel file failed!")


'''
    执行插入操作
    args:db_name（数据库名称）
         table_name(表名称）
         excel_file（excel文件名，把文件与py文件放在同一目录下）

'''


def store_to(db_name, table_name, excel_file):
    db = mysql_link(db_name)  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
    except:
        print(traceback.print_exc())
        print("open excel file failed!")
    #book = open_excel(excel_file)  # 打开excel文件
    sheets = book.sheet_names()  # 获取所有sheet表名
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print("11111",row_num)
        list = []  # 定义列表用来存放数据
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = (row_data[0], row_data[1], row_data[2], row_data[3],
                     row_data[4], row_data[5], row_data[6], row_data[7],
                     row_data[8], row_data[9], row_data[10], row_data[11],
                     row_data[12], row_data[13], row_data[14], row_data[15],
                     )  # 选择获取第几列
            print("22222",value)
            list.append(value)  # 将数据暂存在列表
            # print(i)
        print("list",list)
        # sql = "insert into" + table_name + "(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable) \
        #       values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        sql = "insert into huaian(phone,IMEI1,IMEI2,IMSI,MAC,live_pro,live_city,live_region,live_poi,job_pro,job_city,job_region,job_poi,use_language,time_zones,lable)" \
            " values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 插入的sql语句
        cursor.executemany(sql, list)  # 执行sql语句
        db.commit()  # 提交
        list.clear()  # 清空list
        print("worksheets: " + sheet + " has been inserted " + str(row_num) + " datas!")
    cursor.close()  # 关闭连接
    db.close()




def Query(db_name,table_name):
    db = mysql_link(db_name)  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    data = {
        "userId": "1",
        "username": "",
        "IMEI1":  "",
        "IMEI2": "",
        "IMSI":  "",
        "MAC":  "",
        "ju_pro": "",
        "ju_city": "淮安",
        "ju_region": "",
        "ju_poi":  "",
        "gz_pro": "",
        "gz_city": "",
        "gz_region":  "",
        "gz_poi": "",
        "language": "",
        "time_zone":  "",
        "lable": "",
    }
    #select='select * from huaian where (phone="{0}" or "{0}"="") and (IMEI1="{1}" or "{1}"="") and (IMEI2 ="{2}" or "{2}"="") and (IMSI ="{3}" or "{3}"="") and (MAC ="{4}" or "{4}"="") and (live_pro ="{5}" or "{5}"="")'.format(data["username"], data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],data["ju_pro"])
    select = 'select * from huaian where (phone="{0}" or "{0}"="") and (IMEI1="{1}" or "{1}"="") and (IMEI2 ="{2}" or "{2}"="") and (IMSI ="{3}" or "{3}"="")' \
             ' and (MAC ="{4}" or "{4}"="") and (live_pro ="{5}" or "{5}"="") and (live_city ="{6}" or "{6}"="") and (live_region ="{7}" or "{7}"="")' \
             ' and (live_poi ="{8}" or "{8}"="") and (job_pro ="{9}" or "{9}"="") and (job_city ="{10}" or "{10}"="")'\
             'and (job_region ="{11}" or "{11}"="") and (job_poi ="{12}" or "{12}"="") and (use_language ="{13}" or "{13}"="") and (time_zones ="{14}" or "{14}"="")' \
             'and (lable ="{15}" or "{15}"="")'.format(data["username"], data["IMEI1"], data["IMEI2"], data["IMSI"], data["MAC"],data["ju_pro"],data["ju_city"],
                                                        data["ju_region"], data["ju_poi"], data["gz_pro"], data["gz_city"], data["gz_region"],data["gz_poi"],data["language"],data["time_zone"],data["lable"])

   # select1='select * from huaian where IMEI2="{0}"'.format(359548045606162)
    cursor.execute(select)
   # cursor.execute(select1)
   # result1=cursor.fetchall()

    result = cursor.fetchall()
    print(type(result))
    print(result)
    if result==():
        print("没有符合条件的记录")



  #  print(result1)





if __name__ == '__main__':
    # store_to(数据库名，表名，excel文件名)
    store_to('bitcoin_database', 'huaian', 'huaian.xls')
    #Query('mysql_test','huaian')

