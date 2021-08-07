import os

from elasticsearch import Elasticsearch


def get_els_client():
    default_els_host = "localhost:9200"

    els_host = os.environ.get('ELS_HOST')
    els_username = os.environ.get('ELS_USERNAME')
    els_password = os.environ.get("ELS_PASSWORD")

    if els_host is None:
        els_host = default_els_host

    if els_username is None:
        els_username = "elastic"

    if els_password is None:
        els_password = "9KACp49956n73ok2aqbcoI4I"

    es = Elasticsearch("localhost:9200",
                       http_auth=(els_username, els_password),
                       scheme="https",
                       timeout=500,
                       verify_certs=False)
    return es


if __name__ == '__main__':
    es = get_els_client()
    try:
        es.indices.delete(index='mitre', ignore=400)
    except Exception as e:
        print("Index does not exists. Continue.")
    es.indices.create(index='mitre', ignore=400)

    output = es.indices.put_settings(index='mitre',
                                     body={"index": {
                                         "mapping.total_fields.limit": 100000
                                     }})
    print("Index got created!")