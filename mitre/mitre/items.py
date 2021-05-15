# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from collections import OrderedDict

class MitreItem(Item):
    #item which has dynamic fields
    #creating dynamic pipeline
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = {}



