# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
import urllib.parse
from user_agents import settings


class AutoProxyMiddleware(object):
    """Automatically set a proxy for the request based on the spider's market.
    This will only be used for spiders that have explicitely enabled it.
    (They need to have auto_proxy = True.)
    For each request, a random proxy is selected.
    """

    def process_request(self, request, spider):
        proxies = settings.proxies
        if not proxies:
            return

        proxy = random.choice(proxies)
        if not proxy:
            return

        # For proxies using this spider this will be an extra line per
        # request! When zipping up the file it shouldn't make much difference
        # but we might want to keep an eye out for log file sizes.
        spider.log("Using proxy: {0}".format(proxy))
        url, auth = self.parse_proxy_url(proxy)
        request.meta["proxy"] = url

        if auth is not None:
            # We have to specify auth as a request header.
            # http://stackoverflow.com/a/29716179
            b_encoded_user_pass = base64.b64encode(auth.encode("utf-8"))
            encoded_user_pass = b_encoded_user_pass.decode("utf-8")
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    def parse_proxy_url(self, proxy_url):
        parsed = urllib.parse.urlparse(proxy_url)

        if parsed.username is not None:
            # netloc has the username & password, so we use hostname to rebuild.
            new_netloc = f"{parsed.hostname}:{parsed.port}"
            parsed_as_tuple = (parsed.scheme, new_netloc, parsed.path, parsed.query, parsed.fragment)
            rebuilt_url = urllib.parse.urlunsplit(parsed_as_tuple)
            username_password = f"{parsed.username}:{parsed.password}"

            return (rebuilt_url, username_password)
        else:
            return (proxy_url, None)


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(settings.USER_AGENT_LIST)

