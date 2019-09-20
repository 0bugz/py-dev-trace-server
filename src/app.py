import os
import re
import json
from flask import Flask
from flask import request
from zb_common import Util

app = Flask(__name__)
util = Util("../config/test.cfg", "Dev Trace Server")

# Slack channel config
eng_ops_alerts = util.get_env_value("eng-ops-alerts", "slack-channels")
# Slack channel config

@app.route("/echo", methods=['POST'])
def echo():
    print("Echoing message")
    resp = {
        "status": "success",
        "message": ""
    }
    http_status_code = 200
    try:
        request.get_data()
        contentType = request.headers.get('Content-Type')
        msg_body = request.data.decode('utf-8', 'strict')
        print(request.headers)
        print(contentType)
        print(msg_body)        
        resp["message"] = msg_body
    except Exception as e:
        message = "Exception processing message: {}".format(e)
        resp["message"] = message
        resp["status"] = "failure"
        http_status_code = 500
        util.slack_log(eng_ops_alerts, message)
    finally:
        return json.dumps(resp), http_status_code

if __name__ == '__main__':
    port = os.getenv("PORT")
    file_encoding = os.getenv("PYTHONIOENCODING")
    print("starting server on port: {}, python-io-encoding: {}".format(port, file_encoding))
    app.run(host= '0.0.0.0', debug=True, port=port)
