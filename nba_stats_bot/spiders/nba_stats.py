# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
from nba_stats_bot.items import NBAStatsItem, PlayerItem
from dateutil.parser import parse as parse_date 
from pandas import DataFrame
import json

def int_or_None(n):
    try:
        return int(n)
    except (ValueError, TypeError):
        return None 

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
            callback = self.request_player_info_1
        )

    def request_player_info_1(self, response):
        r_json = json.loads(response.body_as_unicode())
        result_set = r_json[u'resultSets'][0]
        df = DataFrame(data=result_set[u'rowSet'], columns=result_set[u'headers']).set_index('PERSON_ID')
        for id_, data in df.iterrows():
            p = PlayerItem()
            p['nba_player_id'] = id_
            p['nba_player_code'] = data['PLAYERCODE']
            p['is_active'] = bool(data['ROSTERSTATUS'])
            yield FormRequest(
                url = 'http://stats.nba.com/stats/commonplayerinfo/',
                method = 'GET',
                formdata = {'PlayerID': str(id_)},
                meta = dict(player=p),
                callback = self.request_player_info_2
            )

    def request_player_info_2(self, response):
        p = PlayerItem(response.meta.get('player'))
        r_json = json.loads(response.body_as_unicode())
        result_set = r_json[u'resultSets'][0]
        df = DataFrame(data=result_set[u'rowSet'], columns=result_set[u'headers']).set_index('PERSON_ID')
        id_, data = next(df.iterrows())
        p['first_name'] = data['FIRST_NAME']
        p['last_name'] = data['LAST_NAME']
        p['birthdate'] = parse_date(data['BIRTHDATE']).date()
        p['school'] = data['SCHOOL']
        p['country'] = data['COUNTRY']
        p['position'] = data['POSITION']
        p['jersey'] = int_or_None(data['JERSEY'])
        yield Request(
            url = 'http://stats.nba.com/feeds/players/profile/{player_id}_Profile.js' \
                .format(player_id=str(id_)),
            meta = dict(player=p),
            callback = self.parse_player_info
        )

    def parse_player_info(self, response):
        p = PlayerItem(response.meta.get('player'))
        r_json = json.loads(response.body_as_unicode())
        data = r_json[u'PlayerProfile'][0][u'PlayerBio'][0]
        p['height'] = data[u'Height']
        p['weight'] = int_or_None(data[u'Weight'])
        p['pick'] = int_or_None(data[u'DraftPick'])
        yield p

    def parse(self, response):
        pass