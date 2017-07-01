import falcon
from train import predict_single
import json


class Task(object):
    def on_get(self, req, resp):
        string = req.query_string.replace("%20", " ")
        string = string.replace("introduction=", "")

        category = predict_single(string)

        dictA = {}
        dictA["category"] = category

        resp.body = json.dumps(dictA, sort_keys=True, indent=4, separators=(',', ': '))

        # resp.set_header('Access-Control-Allow-Origin', "http://67.205.189.184")
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header('Access-Control-Allow-Origin', "http://localhost")
        resp.status = falcon.HTTP_200
