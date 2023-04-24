# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from nsreg.items import NsregItem

#работает

REGEX_PATTERN = r".*([0-9]+\.).*"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}


class Nsreg_aabSpider(scrapy.Spider):
    name = 'nsreg_aab'
    allowed_domains = ['aab.ru']
    start_urls = ['https://aab.ru/tarifi_na_uslugi.html']

    def parse(self, response):
        pricereg = response.xpath('//*[@id="full_story"]/table/tbody/tr[3]/td[2]/text()').get()
        pricereg = str(pricereg).strip()
        if m := re.match(REGEX_PATTERN, pricereg):
            pricereg = f'{float(pricereg)}'
            logging.info('pricereg = %s', pricereg)
        
        priceprolong = response.xpath('//*[@id="full_story"]/table/tbody/tr[6]/td[2]/text()').get()
        priceprolong = str(priceprolong).strip()
        if m := re.match(REGEX_PATTERN, priceprolong):
            priceprolong = f'{float(priceprolong)}'
            logging.info('priceprolong = %s', priceprolong)

        pricechange = response.xpath('//*[@id="full_story"]/table/tbody/tr[9]/td[2]/text()').get()
        pricechange = str(pricechange).strip()
        pricechange = f'{float(pricechange)}'
        logging.info('pricechange = %s', pricechange)

        item = NsregItem()
        item['name'] = "ООО «ААБ Медиа»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        price['pricechange'] = pricechange 
        item['price'] = price

        yield item
