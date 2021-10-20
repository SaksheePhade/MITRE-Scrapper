#this is the main file to be executed
import os

if __name__ == '__main__':
    os.system('scrapy crawl metrics') #calling the scrapper after which data will be stored in json file
    os.system('python3 create_index.py')# creating an index in elasticsearch
    os.system('python3 json_to_es.py') # storing data from json file into es index
    os.remove('MitreData.json') #deleting json file created by scrapper 
