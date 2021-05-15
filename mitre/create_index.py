import requests
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()
es.indices.create(index='mitretest', ignore=400)

url = 'http://localhost:9200/mitretest/_settings'
body = {"index.mapping.total_fields.limit": 100000}
headers = {'content-type': 'application/json'}

r = requests.put(url, data=json.dumps(body), headers=headers)
print(r)