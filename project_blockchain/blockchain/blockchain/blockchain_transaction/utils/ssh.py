# import pymysql
# from sshtunnel import SSHTunnelForwarder
#
# with SSHTunnelForwarder(
#         ('222.184.15.228', 22),  # B机器的配置--跳板机
#         ssh_password="5532",  # B机器的配置--跳板机账号
#         ssh_username="1472444218@qq.com",  # B机器的配置--跳板机账户密码
#         remote_bind_address=('mysql_192.168.0.79', 3306)
#     ) as server:  # A机器的配置-MySQL服务器
#         conn = pymysql.connect(
#                 host='127.0.0.1',  # 此处必须是必须是127.0.0.1，代表C机器
#                 port=3306,
#                 user='test',  # A机器的配置-MySQL服务器账户
#                 passwd='123456',  # A机器的配置-MySQL服务器密码c
#                 db='bit_db',  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
#                 charset='utf8'  # 和数据库字符编码集合，保持一致，这样能够解决读出数据的中文乱码问题
#                    )
#         cursor = conn.cursor()
#         query = "select version();"
#         cursor.execute(query)
#         data = cursor.fetchall()
#         print(data)
# 建立一个sshclient对象
import paramiko

ssh = paramiko.SSHClient()
# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 调用connect方法连接服务器
ssh.connect(hostname='222.184.15.228', port=22, username='root', password='5532')
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df -hl')
# 结果放到stdout中，如果有错误将放到stderr中
print(stdout.read().decode())
# 关闭连接
ssh.close()