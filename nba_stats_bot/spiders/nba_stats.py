# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
import json

class NBAStatsSpider(Spider):
    name = "nba-stats"
    allowed_domains = ["stats.nba.com"]

    def start_requests(self):
    	yield FormRequest('http://stats.nba.com/stats/commonallplayers',
			method='GET', formdata={'LeagueID': '00', 'Season': '2013-14', 'IsOnlyCurrentSeason': '0'})

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for row in data[u'resultSets'][0][u'rowSet']:
        	player_id = str(row[0])
        	yield FormRequest('http://stats.nba.com/stats/commonplayerinfo/',
        		method='GET', formdata={'PlayerID': player_id})