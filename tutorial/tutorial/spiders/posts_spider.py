import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PostsSpider(CrawlSpider):

    name = "posts"

    def __init__(self, start_urls, allowed_domains, follow_pages,  *args, **kwargs):
        self.start_urls = [start_urls]
        self.allowed_domains = [allowed_domains]
        self.rules = (
            Rule(
                LinkExtractor(allow=(follow_pages)), 
                callback='parse_page', 
                follow=True,
            ),
        )
        super(PostsSpider, self).__init__(*args, **kwargs)


    def parse_page(self, response):
        self.logger.info('Start parse page %s', response.url)
        tm = 'thumbnail'
        for post in response.css('article'):
            item = {
                tm: post.css('img::attr(src)').get(),
                'category': post.css('dd.category-name a::text').get(),
                'title': post.css('h2 a::text').get(),
                'url': post.css('h2 a::attr(href)').get(),
                'desc': post.css('p::text').get(),
            }
            yield response.follow(item['url'], self.parse_content, cb_kwargs=dict(item=item))

    def parse_content(self, response, item):
        self.logger.info('Start parse content %s', response.url)
        item['html'] = response.css('article div[itemprop="articleBody"]').get()
        yield item