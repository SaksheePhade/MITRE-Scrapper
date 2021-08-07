# Scrapy settings for mitre project

BOT_NAME = 'mitre'
LOG_LEVEL = 'ERROR'
SPIDER_MODULES = ['mitre.spiders']
NEWSPIDER_MODULE = 'mitre.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'mitre.pipelines.JsonWriterPipeline': 300,
}

