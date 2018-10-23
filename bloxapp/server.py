#!flask/bin/python
from __future__ import print_function
from flask import Flask
from flask import request
from datetime import datetime
import json
import logging
import cfg

app = Flask(__name__)

@app.route('/postjson', methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    #print(content)
    print(content['id'])
    print(content['name'])
    return 'JSON posted'

@app.route('/uptime', methods=['GET'])
def get_uptime():
    app.__requests += 1
    uptime = (datetime.now() - app.__startup).total_seconds()
    app.logger.info([app.__requests,uptime])
    return json.dumps(dict(uptime = uptime))
    
@app.route('/messages', methods=['GET'])
def get_messages():
    app.__requests += 1
    app.logger.info([app.__requests])
    return json.dumps(dict(messages = app.__requests))

    
if __name__ == '__main__':    
    app.__startup = datetime.now()
    app.__requests = 0
    handler = logging.FileHandler('server.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.run(debug=False, host='0.0.0.0', port=cfg.server_port)