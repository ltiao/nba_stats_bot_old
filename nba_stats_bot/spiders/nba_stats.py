# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
from nba_stats_bot.items import NBAStatsItem
import json

class NBAStatsSpider(Spider):
    name = "nba-stats"
    allowed_domains = ["stats.nba.com"]

    def start_requests(self):
    	params = {
            'LeagueID': '00', 
            'Season': '2013-14', 
            'IsOnlyCurrentSeason': '0'
        }
        yield FormRequest(
            url = 'http://stats.nba.com/stats/commonallplayers',
			method = 'GET', 
            formdata = params,
            callback = self.request_player_info
        )

    def request_player_info(self, response):
        item = NBAStatsItem(data=json.loads(response.body_as_unicode()))
        for id_ in item.as_dataframe(keys='PERSON_ID').index:
            yield FormRequest(
                url = 'http://stats.nba.com/stats/commonplayerinfo/',
                method = 'GET',
                formdata = {'PlayerID': str(id_)},
                callback = self.parse_player_info
            )

    def parse_player_info(self, response):
        item = NBAStatsItem(data=json.loads(response.body_as_unicode()))
        yield item        

    def parse(self, response):
        pass