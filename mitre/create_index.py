import requests
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

#deleting existing index
requests.delete('http://localhost:9200/mitre')

es.indices.create(index='mitre', ignore=400)

url = 'http://localhost:9200/mitre/_settings'
body = {"index.mapping.total_fields.limit": 100000}
headers = {'content-type': 'application/json'}

r = requests.put(url, data=json.dumps(body), headers=headers)
print(r)