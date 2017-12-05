# -*- coding: utf-8 -*-
import scrapy
import json
import random

from banner.items import Album


class QqpcSpider(scrapy.Spider):
    name = 'qqpc'
    allowed_domains = ['y.qq.com', 'u.y.qq.com']
    # 592588565118626
    jsonp_callback = 'recom' + str(random.random())[2:]
    start_urls = [
        'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=%s&g_tk=5381&jsonpCallback=%s&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"comm":{"ct":24},"category":{"method":"get_hot_category","param":{"qq":""},"module":"music.web_category_svr"},"recomPlaylist":{"method":"get_hot_recommend","param":{"async":1,"cmd":2},"module":"playlist.HotRecommendServer"},"playlist":{"method":"get_playlist_by_category","param":{"id":8,"curPage":1,"size":40,"order":5,"titleid":8},"module":"playlist.PlayListPlazaServer"},"new_song":{"module":"QQMusic.MusichallServer","method":"GetNewSong","param":{"type":0}},"new_album":{"module":"QQMusic.MusichallServer","method":"GetNewAlbum","param":{"type":0,"category":"-1","genre":0,"year":1,"company":-1,"sort":1,"start":0,"end":39}},"toplist":{"module":"music.web_toplist_svr","method":"get_toplist_index","param":{}},"focus":{"module":"QQMusic.MusichallServer","method":"GetFocus","param":{}}}' % (
            jsonp_callback, jsonp_callback)]

    def parse(self, response):
        musics_json_text = response.text.replace('%s(' % self.jsonp_callback, '')
        banners = json.loads(musics_json_text[0:musics_json_text.rfind(')')])['focus']['data']['content']
        for banner in banners:
            # digitalbum
            if banner['type'] == 10002:
                yield scrapy.Request('https://y.qq.com/n/yqq/album/%s.html#stat=y_new.index.focus.click' %
                                     banner['jump_info']['url'], self.parse_album)
            elif banner['type'] == 10012:
                self.log('mv')
            elif banner['type'] == 10014:
                self.log('playlist')
            else:
                # 3002 msa pass
                self.log('type:' + str(banner['type']))

    def parse_album(self, response):
        return Album(name=response.xpath('//h1[@class="data__name_txt"]/text()').extract_first(default=''),
                     artists=response.xpath('//div[@class="data__singer"]/a/text()').extract_first(default=''),
                     href=response.url)
