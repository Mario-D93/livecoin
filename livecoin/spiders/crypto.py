# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from datetime import date

class CryptoSpider(scrapy.Spider):
    name = 'crypto'
    allowed_domains = ['www.livecoin.net/en']
    
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = False

            assert(splash:go(args.url))
            splash:wait(1)
            
            btn = splash:select_all(".filterPanelItem___2z5Gb")
            btn[3]:mouse_click()
            
            splash:wait(1)

            btn_more = splash:select("div.showMoreContainer___2HlS0 button")
            btn_more:mouse_click()
            assert(splash:wait(2))
            
            splash:set_viewport_full()
            splash:wait(1)
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute",args={
            'lua_source':self.script
        })

    def parse(self, response):
        dt = date.today()
        yield{
            'Date: ':dt
        }
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield{
                'coin_pair':currency.xpath(".//div[1]/div/text()").get(),
                'volume_24h':currency.xpath(".//div[2]/span/text()").get(),
                'last_price':currency.xpath(".//div[3]/span/text()").get(),
                'change_24h':currency.xpath(".//div[4]/span/span/text()").get(),
            }