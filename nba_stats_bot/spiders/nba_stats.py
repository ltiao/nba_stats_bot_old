# -*- coding: utf-8 -*-
import scrapy


class NbaStatsSpider(scrapy.Spider):
    name = "nba-stats"
    allowed_domains = ["stats.nba.com"]
    start_urls = (
        'http://www.stats.nba.com/',
    )

    def parse(self, response):
        pass
