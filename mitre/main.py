import os



if __name__ == '__main__':
    os.system('scrapy crawl metrics')
    os.system('python3 create_index.py')
    os.system('python3 json_to_es.py')
    os.remove('MitreData.json')
