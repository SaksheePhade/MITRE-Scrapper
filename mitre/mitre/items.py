from scrapy import Item, Field
from collections import OrderedDict

class MitreItem(Item):
    #item which has dynamic fields
    #this was created because each technique had a card in which the fields were varying for each technique
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = {}



