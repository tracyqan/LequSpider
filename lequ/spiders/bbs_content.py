
import scrapy
from scrapy.spiders import Spider
from lequ.items import ContentItem
import re


class BbsLequComSpider(Spider):
    name = 'content'
    allowed_domains = ['bbs.lequ.com']
    # 改为网站第一页的url
    start_urls = ['http://bbs.lequ.com/forum-173-1.html']
    # pipeline配置项,用来区分不同爬虫使用的pipeline的类
    custom_settings = {
        'ITEM_PIPELINES': {'lequ.pipelines.ContentPipeline': 300,}
    }

    def parse(self, response):
        # 提取当前页的所有帖子url存放在urls列表中, 注意当爬虫启动的时候首先会调用这个方法对start_url列表中的url进行爬取
        # 所以如果爬取的网站需要登录, 需要在这个方法中实现
        urls = response.xpath('//th[@class="common"]/a[1]/@href|//th[@class="new"]/a[1]/@href').getall()
        # 抓取下一页的url
        next_page = response.xpath('//a[@class="nxt"]/@href').get()

        for url in urls:
            # 遍历urls,对每一个帖子链接传递给parse_detail函数解析
            yield scrapy.Request(url, callback=self.parse_detail)

        # 判断是否存在下一页url,一般情况下最后一页是没有下一页链接的
        if next_page:
            # 将下一页的url返回给parse函数进行解析,可以当作是递归的思想
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):

        name = response.xpath('//div[@class="authi"]/a/text()').get()
        content = response.xpath('//div[@id="postlist"]/div[@id][1]//td[@class="t_f"]/text()').getall()
        content = re.sub(r'\s', '', ''.join(content))
        public_time = response.xpath('//em[@id][1]/text()').get().replace('发表于 ', '')
        read_count = int(response.xpath('//div[@class="hm ptn"]/span[2]/text()').get())
        reply_count = int(response.xpath('//div[@class="hm ptn"]/span[5]/text()').get())

        # 创建Item对象进行存放数据,
        item = ContentItem(name=name, content=content, public_time=public_time,
                           read_count=read_count, reply_count=reply_count)

        yield item
        print('{}的帖子内容已爬取'.format(name))