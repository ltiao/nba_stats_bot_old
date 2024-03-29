# -*- coding: utf-8 -*-

# Scrapy settings for nba_stats_bot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nba_stats_bot'

SPIDER_MODULES = ['nba_stats_bot.spiders']
NEWSPIDER_MODULE = 'nba_stats_bot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nba_stats_bot (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
	'nba_stats_bot.pipelines.BotPipeline': 1,
}

import os

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = os.path.join('/Users/tiao/Desktop', 'httpcache')