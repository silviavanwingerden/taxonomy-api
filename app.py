import falcon
import categorize

api = application = falcon.API()

api.add_route('/task', categorize.Task())
