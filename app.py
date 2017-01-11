# things.py

# Let's get this party started!
import falcon
import json
import zlib
import base64
from pymongo import MongoClient


quote = '\nTwo things awe me most, the starry sky '\
         'above me and the moral law within me.\n'\
         '\n'\
         '    ~ Immanuel Kant\n\n'


class ThingsResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = (quote)
    def on_head(self, req, resp):
        resp.status = falcon.HTTP_200
        #resp.body


class ZipFile(object):
    def on_post(self, req, resp):
        json_blob = json.load(req.stream)
        print "postdata: {}".format(json_blob)

        test = {k:base64.b64encode(zlib.compress('|'.join(([v]*10000000)))) for k,v in json_blob.iteritems()}


        db = MongoClient("mongodb://localhost:27017").db
        r = db['falcon'].insert_one(test)
        resp.body = str(r.inserted_id)


# falcon.API instances are callable WSGI apps
api = application = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()
zip_files = ZipFile()

# things will handle all requests to the '/things' URL path
api.add_route('/things', things)
api.add_route('/zip-files', zip_files)