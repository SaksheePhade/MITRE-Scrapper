import os

os.system('scrapy crawl metrics')
os.system('python create_index.py')
os.system('python json_to_es.py')
os.remove('MitreData.json')
