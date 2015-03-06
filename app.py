import os
from flask import Flask
from models import *
import config
from flask.ext import restful
import flask.ext.restless
import json


app = Flask(__name__)
#api = restful.Api(app)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

manager = flask.ext.restless.APIManager(app, session=session)
last10 = manager.create_api(Summary, methods=['GET', 'POST'])
"""
class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

class Last10(restful.Resource):
    def get(self):
        results = {}
        last10 = session.query(Summary).order_by(Summary.timestamp.desc()).limit(10)
        for entry in last10:
            results[entry.id] = {}
            results[entry.id]['timestamp'] = entry.timestamp.isoformat()
            results[entry.id]['model'] = entry.model
            results[entry.id]['avg_io_size'] = entry.avg_io_size
            results[entry.id]['iops_95th'] = entry.iops_95th
            results[entry.id]['iops_avg'] = entry.iops_avg
            results[entry.id]['iops_max'] = entry.iops_max
            results[entry.id]['percent_read'] = entry.percent_read

        return json.dumps(results)


api.add_resource(HelloWorld, '/')
api.add_resource(Last10, '/last10')
"""


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
