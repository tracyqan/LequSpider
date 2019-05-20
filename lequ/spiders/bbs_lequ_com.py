# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lequ.items import LequItem
import re


class BbsLequComSpider(CrawlSpider):
    name = 'lequ'
    allowed_domains = ['bbs.lequ.com']
    # 改为网站第一页的url
    start_urls = ['http://bbs.lequ.com/forum-173-1.html']
    # pipeline配置项,用来区分不同爬虫使用的pipeline的类
    custom_settings = {
        'ITEM_PIPELINES': {'lequ.pipelines.LequPipeline': 300, }
    }
    # 将正则表达式的字符串形式编译为Pattern实例, 提高效率
    pattern = re.compile(r'[\(\)（）;；“”\s]')
    # url匹配规则
    rules = (
        # 在start_url中爬取满足.*forum-173-\d+.html的url, follow=True为跟进匹配,即当爬取的url中还存在满足表达式的url时继续爬取
        # 在这个规则中没有回调函数,是因为我们不需要解析页面内容,只需要获取到网页源码从中找出满足匹配规则的url即可
        Rule(LinkExtractor(allow=r'.*forum-173-\d+.html'), follow=True),
        # 在上面的每一个url中爬取满足.*space-uid-\d+.html的url,并传递给parse_html解析
        Rule(LinkExtractor(allow=r'.*space-uid-\d+.html'), callback='parse_html', follow=True),
    )
    # 注意,在写上一个爬虫中讲过,爬虫开始的时候默认调用parse方法爬取start_url,CrawlSpider爬虫模板已经实现了该方法,并对rules规则匹配
    def parse_html(self, response):

        name = response.xpath('//h2[@class="mt"]/text()').get() # 获取用户名
        name = self.pattern.sub('', name)
        active_time = int(response.xpath('//ul[@id="pbbs"]/li[1]/text()').get().split()[0]) # 获取在线时长
        create_time = response.xpath('//ul[@id="pbbs"]/li[2]/text()').get() # 获取创建时间
        last_login = response.xpath('//ul[@id="pbbs"]/li[3]/text()').get() # 获取最后登录时间
        last_activity = response.xpath('//ul[@id="pbbs"]/li[4]/text()').get() # 获取最后活跃时间
        area = response.xpath('//ul[@id="pbbs"]/li[6]/text()').get() # 获取地址信息
        area = self.pattern.sub('', area)
        identity = response.xpath('//span[contains(@style, "color")]//text()').getall()[-1] # 获取论坛等级
        uid_str = response.xpath('//span[@class="xw0"]/text()').get() # 获取uid
        uid = int(re.search(r'UID: (\d+)', uid_str).group(1))
        signature_info = response.xpath('//div[@class="pbm mbm bbda cl"]/ul[2]//td//text()').getall() # 获取个性签名
        signature = ''.join(signature_info) if signature_info else ''
        signature = self.pattern.sub('', signature)
        infos = response.xpath('//ul[@class="cl bbda pbm mbm"]//a/text()').getall()
        friend_nums = int(infos[0].split()[-1]) # 获取好友数
        reply_times = int(infos[1].split()[-1]) # 获取回复数
        theme_nums = int(infos[2].split()[-1])  # 获取发帖数
        forum_money = int(response.xpath('//div[@id="psts"]/ul[@class="pf_l"]/li[last()]/text()').get().strip()) # 获取论坛币数量
        # 构造Item对象,存储数据
        item = LequItem(name=name, active_time=active_time, create_time=create_time, last_login=last_login,
                        last_activity=last_activity, area=area, identity=identity, uid=uid, signature=signature,
                        friend_nums=friend_nums, reply_times=reply_times, theme_nums=theme_nums, forum_money=forum_money)
        yield item
        print('{}的用户信息已爬取'.format(name))



if __name__ == '__main__':
    from scrapy.cmdline import execute
    # 创建执行爬虫命令, execute需要传入一个列表,即['scrapy', 'crawl', BbsLequComSpider.name]
    # 直接执行这个文件,就等于在命令行启动这个爬虫
    execute('scrapy crawl {}'.format(BbsLequComSpider.name).split())