from __future__ import print_function
import re
import pymysql
import requests
import cfg
import logging
import time
import sys
import json

if sys.version_info >= (3,0):
    pass
else:
    input = raw_input
    
    
logging.basicConfig(filename='app.log',level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler())

cursor = pymysql.connect(**cfg.db_cfg).cursor()

class ExitRequest(Exception):
    pass
    
def get(measure):
    res = requests.get(url= cfg.baseurl + '/' + measure)
    json = res.json()
    logging.getLogger('app').debug([json])
    for row in json.items():
        cursor.execute('''INSERT INTO bloxapp.metrics(measure,val) VALUES(%s,%s)''' , row )
    return(json)    

def auto(measure,sleep = 60):
    while True:
        get(measure)
        time.sleep(sleep)
    
def exit():
    logging.getLogger('app').debug(['exit requested'])
    raise ExitRequest()
    
def last(measure):
    cursor.execute('''SELECT val as last FROM bloxapp.metrics WHERE measure = %s ORDER BY id DESC LIMIT 1''' , measure )
    row = cursor.fetchone()
    logging.getLogger('app').debug([row])
    return row
    
def avg(measure,samples = 1):
    cursor.execute('''SELECT AVG(val) as avg FROM (SELECT measure,val FROM bloxapp.metrics WHERE measure = %s ORDER BY id DESC LIMIT %s) temp''' ,
        (measure,int(samples) )
        )
    row = cursor.fetchone()
    logging.getLogger('app').debug([row])
    return row
    
if __name__ == '__main__':
    def iter():
        while True:
            raw = input('>')
            params = re.search('(?P<action>get|last|avg|exit|auto)\s*(?P<measure>uptime|messages)?\s*(?P<samples>[0-9]+)?',raw)
            if params:
                yield {k:v for k,v in params.groupdict().items() if v}
            else:
                logging.getLogger('app').debug(['invalid input use get|last|avg|exit|auto '])
                
    for params in iter():
        logging.getLogger('app').debug([params])
        try:
            res = locals().get(params.pop('action'))(**params)
            if res:
                print('>>>',json.dumps(res))
                
        except ExitRequest as e:
            break