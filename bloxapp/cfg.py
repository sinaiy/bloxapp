import pymysql
server_port = 5000
baseurl = 'http://127.0.0.1:5000'
db_cfg = dict(host='localhost',
              user='bloxappuser',
              password='passwd',
              db='bloxapp',
              charset='utf8mb4',
              autocommit=True,
              cursorclass=pymysql.cursors.DictCursor
              )