import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, CrawlSpider, Rule
from slugify import slugify


def clean(lst_or_str):
    clean_r = re.compile(r'\s+')
    _clean = lambda s: clean_r.sub(' ', s)

    if isinstance(lst_or_str, list):
        lst_or_str = [_clean(str).strip() for str in lst_or_str if str and _clean(str or '').strip()]
    else:
        lst_or_str = _clean(lst_or_str or '').strip()

    return lst_or_str


class WhatIsMyBrowserParseSpider(Spider):
    name = 'whatismybrowser-parse'
    seen_user_agents = set()

    def parse(self, response, *args, **kwargs):
        user_agent = self.extract_user_agent(response)

        if self.is_seen_user_agent(user_agent):
            return

        user_agent = {
            'source_url': response.url,
            'user_agent': user_agent,
            'operating_system': self.extract_os_name(response),
            'software_name': self.extract_software_name(response),
            'software_engine': self.extract_software_engine(response),
            'software_type': self.extract_software_type(response),
            'software_version': self.extract_software_version(response),
            'hardware_type': self.extract_hardware_type(response),
            'popularity': response.meta.get('popularity')
        }

        return user_agent

    def is_seen_user_agent(self, user_agent):
        _user_agent = slugify(user_agent)

        if user_agent in self.seen_user_agents:
            return True

        self.seen_user_agents.add(_user_agent)

    def extract_user_agent(self, response):
        return response.css('h2.useragent ::text').extract_first()

    def extract_os_name(self, response):
        css = '.key:contains("Operating System Name Code") + .value ::text'
        return clean(response.css(css).extract())[0]

    def extract_software_name(self, response):
        css = '.key:contains("Software Name Code") + .value ::text'
        return clean(response.css(css).extract())[0]

    def extract_software_engine(self, response):
        css = '.key:contains("Layout Engine Name") + .value ::text'
        return clean(response.css(css).extract())[0]

    def extract_software_type(self, response):
        css = '.key:contains("Software Type") + .value ::text'
        return clean(response.css(css).extract())[0]

    def extract_software_version(self, response):
        css = '.key:contains("Software Version") + .value ::text'
        return clean(response.css(css).extract())[0]

    def extract_hardware_type(self, response):
        css = '.key:contains("Hardware Type") + .value ::text'
        return clean(response.css(css).extract())[0]


class WhatIsMyBrowserCrawlSpider(CrawlSpider):
    name = 'whatismybrowser-crawl'
    parse_spider = WhatIsMyBrowserParseSpider()

    allowed_domains = ['developers.whatismybrowser.com']
    start_urls = ['https://developers.whatismybrowser.com/useragents/explore/']

    listings_css = [
        '.browse-all',
        'table .maybe-long',
        '#pagination',
    ]

    user_agent_css = '.useragent'

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
    ]

    def parse(self, response, *args, **kwargs):
        for row in response.css('.table-useragents tbody tr'):
            popularity = clean(row.css('td ::text').extract())[-1].lower()
            url = clean(row.css('td a::attr(href)').extract())[0]
            yield response.follow(url, meta={'popularity': popularity}, callback=self.parse_item)

        yield from self._requests_to_follow(response)

    def parse_item(self, response):
        return self.parse_spider.parse(response)
