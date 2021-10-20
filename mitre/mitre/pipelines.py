from itemadapter import ItemAdapter   

import json
import os

#pipeline to store the records into json file(MitreData.json)
class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('MitreData.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

