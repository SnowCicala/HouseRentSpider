
# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
# @Author : woodenrobot

from scrapy import cmdline
if __name__ == "__main__":
    
    name = 'X58'
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())