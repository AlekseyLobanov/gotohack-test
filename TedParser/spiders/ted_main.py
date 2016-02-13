# -*- coding: utf-8 -*-
import re
import json

import scrapy


class TedMainSpider(scrapy.Spider):
    name = "ted_main"
    allowed_domains = ["ted.com"]
    START_URL       = "http://www.ted.com/talks/"
    start_urls      = [START_URL + str(i) for i in range(1,4000)]
    views_re        = re.compile(r"talk-sharing__value'>([^<]+)<")
    PATTERN_START   = '<script>q("talkPage.init",'
    PATTERN_END     =  ')</script></div>'

    def parse(self, response):
        data = response.body
        st   = data.find(self.PATTERN_START)
        if st < 0:
            return None
        st  += len(self.PATTERN_START)
        end = data.find(self.PATTERN_END, st)
        js  = json.loads(data[st:end])
        res = {}
        views_list = self.views_re.findall(data)
        if len(views_list) == 0:
            return None
        res[u'views'] = int(views_list[0].strip().replace(",",""))
        res[u'tags']  = js[u'talks'][0][u'targeting'][u'tag']
        res[u'id']    = js[u'talks'][0][u'targeting'][u'id']
        res[u'title'] = js[u'talks'][0][u'title']
        for item in js[u'ratings']:
            res[item[u'name'].lower()] = item[u'count']
        return res
