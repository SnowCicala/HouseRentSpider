# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BriefHouseRentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field() # 标题
    room = scrapy.Field() # 房间大小
    region = scrapy.Field() # 区域
    community = scrapy.Field() # 社区
    location = scrapy.Field() # 交通信息
    sender = scrapy.Field() # 发布者
    money = scrapy.Field() # 价格
    #pass
    
    
class DetailHouseRentItem(BriefHouseRentItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    orientation = scrapy.Field() # 房间朝向
    floor = scrapy.Field() # 楼层
    
    disposal = scrapy.Field() # 房源配置
    introduce = scrapy.Field() # 房间描述
    
    rentWay = scrapy.Field() # 租赁方式
    feeDetail = scrapy.Field() # 费用明细
    payWay = scrapy.Field() # 支付方式
    
    picLinks = scrapy.Field() # 房屋图片
    updateDate = scrapy.Field() # 发布时间
    pageHits = scrapy.Field() # 浏览次数

