import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tutorial.items import SpieceIndexItem, SpieceItem


CRAWL_CATEGORY = {
  'freshwater':{
    'start_urls':['https://www.daff.qld.gov.au/fisheries/species-identification/freshwater-fish'],
    'rules':(
            Rule(LinkExtractor(allow=('species-identification/freshwater-fish/.*', 
                                      'species-identification/inshore-estuarine-species/barramundi',
                                      'species-identification/shark-identification-guide/photo-guide-to-sharks/sharks,-part-3/freshwater-sawfish',
                                      'species-identification/inshore-estuarine-species/tropical-snappers/mangrove-jack',
                                      'species-identification/inshore-estuarine-species/mullet/sea-mullet',
                                      'species-identification/inshore-estuarine-species/garfish/snubnose-garfish'
                                      )), callback='parse_item', follow= True),
            )
  },
  'inshore':{
    
  },
  'all':{
    
  }
}

selected_item = CRAWL_CATEGORY['freshwater']
class FishSpider(CrawlSpider):
    name = "fish"
    allowed_domains = ["daff.qld.gov.au"]
    start_urls = selected_item['start_urls']
    
    rules = selected_item['rules']
      
    # def parse_start_url(self, response):
    #   for sel in response.xpath('//*[@id="new_div_80245"]/ul/li'):
    #     item = SpieceIndexItem()
    #     item['name'] = sel.xpath('a/text()').extract()
    #     item['link'] = sel.xpath('a/@href').extract()
    #     yield item
    
    def parse_item(self, response):
      for sel in response.xpath('//*[@id="main"]/div[3]/div[1]/div[1]'):
        item = SpieceItem()
        item['name'] = sel.xpath('//h1/text()').extract()[0]
        item['image_url'] = sel.xpath('//*[@class="fancybox"]/@href').extract() or \
                            sel.xpath('//dl/dt/img/@src').extract()
        item['source_url'] = response.url
 
        # parse description items
        description_all = sel.xpath('//tr')
        description_items = {}
        for i in description_all:
          key = i.xpath('th/text()').extract()[0]
          value = i.xpath('td//text()').extract()
          description_items[key.strip()] =  [v for v in value if v.strip() != '']

        item['descriptions'] = description_items
        if item['image_url'] == [] or item['descriptions'] == []:
          break
        yield item
    
    