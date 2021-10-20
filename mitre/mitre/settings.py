# Scrapy settings for mitre project

BOT_NAME = 'mitre'

SPIDER_MODULES = ['mitre.spiders']
NEWSPIDER_MODULE = 'mitre.spiders'

ROBOTSTXT_OBEY = False #this is false because if made true the scrapper cannot crawl the github pages

CONCURRENT_REQUESTS = 32 #this is enabled to avoid 429 error

HTTPERROR_ALLOWED_CODES  = [404,429]

ITEM_PIPELINES = {
   'mitre.pipelines.JsonWriterPipeline': 300,
}

