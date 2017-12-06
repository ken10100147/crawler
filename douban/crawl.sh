#!/bin/sh

#scrapy crawl music
scrapy crawl review
scrapy crawl follower
scrapy crawl user -s DOWNLOAD_DELAY=4 -s CONCURRENT_REQUESTS_PER_DOMAIN=1
#run multi time to get more info
scrapy crawl user -s DOWNLOAD_DELAY=4 -s CONCURRENT_REQUESTS_PER_DOMAIN=1
#run multi time to get more info
scrapy crawl user -s DOWNLOAD_DELAY=4 -s CONCURRENT_REQUESTS_PER_DOMAIN=1
