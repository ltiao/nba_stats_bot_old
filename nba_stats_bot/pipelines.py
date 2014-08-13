# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dateutil.parser import parse as parse_date 
from nba.models import Player

class BotPipeline(object):
    def process_item(self, item, spider):
    	record = item.as_dataframe(keys='PERSON_ID').to_dict('records')[0]
    	p = Player(
    		first_name = record[u'FIRST_NAME'],
    		last_name = record[u'LAST_NAME'],
    		birthdate = parse_date(record[u'BIRTHDATE']),
    		school = record[u'SCHOOL'],
    		country = record[u'COUNTRY'],
    		# active = ,
    		jersey = record[u'JERSEY'],
    		# position = ,
    		# height = ,
    		# weight = ,
    		# pick = ,
    	)
    	# p.save(commit=False)
        return item
