# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from pandas import DataFrame

class NBAStatsItem(Item):
	data = Field()

	def as_dataframe(self, result_set_ind=0, keys=None):
		result_set = self[u'data'][u'resultSets'][result_set_ind]
		df = DataFrame(result_set[u'rowSet'], columns=result_set[u'headers'])
		if keys is not None:
			df.set_index(keys, inplace=True)
		return df