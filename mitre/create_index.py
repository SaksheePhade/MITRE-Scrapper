import os

from elasticsearch import Elasticsearch


def get_els_client():
    #establishing connection with elastic search on port 9200 using Elasticsearch module
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
        #deleting the previous index to avoid duplication of data
        es.indices.delete(index='mitre', ignore=400) 
    except Exception as e:
        print("Index does not exists. Continue.")

    #this mapping is for the datasources field 
    mapping = {  
            "mappings":{  
                "properties":{  
                    "datasources":{  
                        "type":"nested",
                        "properties":{
                            "name":{"type":"text"},
                            "type":{"type":"text"},
                            "description":{"type":"text"},
                            "relatinships":{
                                "type":"nested",
                                "properties":{
                                    "source_data_element":{"type":"text"},
                                    "target_data_element":{"type":"text"},
                                    "relationship":{"type":"text"}
                                }
                            }    
                        }
                    }
                }
            }
        }    
    
    #creating the index with the specified mapping
    es.indices.create(index='mitre', ignore=400, body = mapping)

    #changing the field limits to avoid errors
    output = es.indices.put_settings(index='mitre',
                                     body={"index": {
                                         "mapping.total_fields.limit": 100000,
                                         "mapping.nested_fields.limit" : 100000,
                                         "mapping.nested_objects.limit" : 100000
                                     }})
    print("Index got created!")