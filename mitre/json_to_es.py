import json
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch("localhost:9200", timeout=500)
def get_data_from_text_file(self):
# the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

# call the function to get the string data containing docs
docs = get_data_from_text_file("MitreData.json")

# print the length of the documents in the string
print ("String docs length:", len(docs))

# define an empty list for the Elasticsearch docs
doc_list = []

# use Python's enumerate() function to iterate over list of doc strings
for num, doc in enumerate(docs):

# catch any JSON loads() errors
    try:
        doc = doc.replace("True", "true")
        doc = doc.replace("False", "false")
        dict_doc = json.loads(doc)
        # append the dict object to the list []
        doc_list += [dict_doc]

    except json.decoder.JSONDecodeError as err:
        # print the errors
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

    print ("Dict docs length:", len(doc_list))
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    resp = helpers.bulk(
    client,
    docs,
    index = "mitre",
    stats_only=True,
    )
    print ("helpers.bulk() RESPONSE:", resp)
    print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:

    # print any errors returned while making the helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()