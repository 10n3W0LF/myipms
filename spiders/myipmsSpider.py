from email import header
from time import sleep
import scrapy
from random import randint
import logging
from scrapy.utils.log import configure_logging


class myipmsSpider(scrapy.Spider):
    name='shopifyDomains'
    allowed_domains = ['myip.ms']
    custom_settings={
        'DOWNLOAD_DELAY':randint(20,120),
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    } 
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    def start_requests(self):
        urls = ['https://myip.ms/ajax_table/sites/%s/own/376714' % page for page in list(range(100)) if page >= 3]
        for link in urls:
            yield scrapy.Request(url=link, method = 'POST', callback= self.parse) 

    def parse(self, response):
        main=response.css('#sites_tbl')
        web_name=main.css('td:nth-child(2)')
        ip=main.css('td:nth-child(3)')
        rank=[]
        for x in response.css('span.bold.arial.grey::text').getall():
            if '#' in x:
                rank.append(x)
            else:
                pass
        for i in range(len(web_name)):
            yield{
                'website':web_name.css('a::text').getall()[i],
                'web_ip_addr':ip.css('a::text').getall()[i],
                'World_Site_Popular_Rating':rank[i]
            }
    
    
        