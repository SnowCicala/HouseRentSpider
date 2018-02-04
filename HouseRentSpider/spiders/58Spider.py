# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector 
from bs4 import BeautifulSoup
from ..items import BriefHouseRentItem, DetailHouseRentItem
import re

class X58Spider(scrapy.Spider):
    name = 'X58'
    allowed_domains = ['58.com']
    #start_urls = ['http://bj.58.com/zufang/0/']
    #start_urls = ['https://www.baidu.com/']
    def start_requests(self):
         
        yield scrapy.Request('http://bj.58.com/zufang/0/', callback = self.parse_personal_house_brief)
        
    def parse_personal_house_brief(self, response):   
        print(response.headers.getlist('Set-Cookie'))
        #print(response.body)
        breifHouseData = []
        houseList = response.xpath('//ul[@class="listUl"]/li')
        for houseItem in houseList:    
            item = BriefHouseRentItem()
            # 房源信息
            houseInfos = houseItem.xpath('./div[@class="des"]')
            for element in houseInfos:
                detailLink = element.xpath('./h2/a/@href').extract_first()
                yield scrapy.Request(detailLink, callback = self.parse_personal_house_detail)
                
                item['title'] = element.xpath('./h2/a/text()').extract_first()
                item['room'] = element.xpath('./p[@class="room"]/text()').extract_first()
                locations = element.xpath('./p[@class="add"]/a/text()').extract()
                if locations:
                    item['region'] = locations[0]
                    item['community'] = " " if len(locations) < 2 else locations[1]
                
                item['location']  = element.xpath('./p[@class="add"]/text()').extract()[-1]
                #address =  ';'.join((region, community, location))
                item['sender'] = element.xpath('./p[@class="geren"]/text()').extract()[-1]
                
            # 价格信息
            item['money'] = houseItem.xpath('./div[@class="listliright"]/div[@class="money"]/b/text()').extract_first()
            #print(item['money'])
            
            breifHouseData.append(item)
        #print(breifHouseData)    
        
    def parse_count(self, response):
        print(response.headers.getlist('Set-Cookie'))
        print(response.body)
        item = response.meta["item"]
        item["pageHits"] = response.text.split(';')[-1]
        
    def parse_personal_house_detail(self, response):
        print(response.headers.getlist('Set-Cookie'))
        #print(response.text)
        counterUrl = 'http://jst1.58.com/counter?infoid={infoid}&uname=&userid=&totalControl=&listControl=&sid=0&lid=0&px=0&cfpath=&_=1517290042748'
        referer = 'http://bj.58.com/zufang/{infoid}x.shtml?end=end&from=1-list-0&iuType=z_0&PGTID=0d300008-0000-1f03-d8cb-2556b6ad4ead&ClickID=4'    
        header = {
            'Host': 'jst1.58.com',
            'Accept-Encoding' : 'gzip, deflate',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',                  
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }  
        tagClear = re.compile(r"<.*?>|\s+")
        detailHouseData = []
        houseInfos = response.xpath('//div[@class="main-wrap"]')
        for houseItem in houseInfos:    
            item = DetailHouseRentItem()
            # 标题信息
            titleInfos = houseItem.xpath('./div[@class="house-title"]')
            for element in titleInfos:
                item['title'] = element.xpath('./h1/text()').extract_first()      
                item['updateDate'] = element.xpath('./p/text()').extract_first()
                item['pageHits'] = element.xpath('./p/em/text()').extract_first()
             
                # 房屋基本信息
                basicHouseInfos = element.xpath('./div[@class="house-desc-item fl c_333"]')
                for ele in basicHouseInfos:

                    item['money'] = ele.xpath('./div[@class="house-pay-way f16"]/span[@class="c_ff552e"]/b/text()').extract_first()
                    item['payWay'] = ele.xpath('./div[@class="house-pay-way f16"]/span[@class="c_333"]/text()').extract_first()
                    item['feeDetail'] = tagClear.sub(" ", ';'.join(ele.xpath('./div[@class="house-pay-way f16"]/a[@class="c_0091d7 freeEntry"]/div/ul/li').extract()))
                    item['location'] = tagClear.sub(" ", ';'.join(ele.xpath('./ul[@class="f14"]/li/span').extract()[:-1]))
                    #print(item['location'] )
                    
            # 房屋描述
            detailDescs = houseItem.xpath('./div[@class="house-detail-desc"]/div[@class="main-detail-info fl"]')
            for element in detailDescs:      
                # 房屋配置
                item['disposal'] = ';'.join(element.xpath('./ul[@class="house-disposal"]/li/text()').extract())
                #print(item['disposal'])
                
            # 房屋描述
            item['introduce'] = ""
            wordIntroduces = element.xpath('./div[@class="house-word-introduce f16 c_555"]/ul[@class="introduce-item"]/li')
            #print(wordIntroduces)
            for ele in wordIntroduces:
                key = tagClear.sub(" ", ele.xpath('./span').extract_first())
                value = tagClear.sub(" ", ele.xpath('./span[2]').extract()[0])
                item['introduce'] += '{0} : {1};'.format(key, value) 
                #print('%s : %s ' % (key, value))
                # 基本信息
                basicInfos = houseItem.xpath('./div[@class="house-basic-info"]/div[@class="house-basic-right fr"]/div[@class="house-basic-desc"]')
                for element in basicInfos:
                    # 房屋agent信息
                    agentInfos = element.xpath('./div[@class="house-agent-info fr"]').extract()
                    if agentInfos:
                        groups = re.findall(r"infoId=(\d*)", agentInfos[0])
                        url = counterUrl.format(infoid = groups[0])
                        header['Referer'] = referer.format(infoid = groups[0])
                        
                        yield scrapy.Request(url, callback = self.parse_count, headers= header, meta={"item":item})
                        
                    
            detailHouseData.append(item)
            print(detailHouseData)
        #sel = Selector(response)
        #print(sel.data)
        #yield scrapy.Request(response.url, callback= self.parse)
        #soup = BeautifulSoup(response.body, "lxml")
        #print(soup)
        #for sel in response.xpath('//ul/li'):
            # title = sel.xpath('a/text()').extract()
            # link = sel.xpath('a/@href').extract()
            # desc = sel.xpath('text()').extract()
            # print (title, link, desc)

            #item = TutorialItem()
            #item['title'] = sel.xpath('a/text()').extract()
            #item['link'] = sel.xpath('a/@href').extract()
            #item['desc'] = sel.xpath('text()').extract()
            #yield item

            
            
from scrapy import cmdline
if __name__ == "__main__":       
    name = 'X58'
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())