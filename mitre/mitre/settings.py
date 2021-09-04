# Scrapy settings for mitre project

BOT_NAME = 'mitre'

SPIDER_MODULES = ['mitre.spiders']
NEWSPIDER_MODULE = 'mitre.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32

HTTPERROR_ALLOWED_CODES  =[404,429]

ITEM_PIPELINES = {
   'mitre.pipelines.JsonWriterPipeline': 300,
}

