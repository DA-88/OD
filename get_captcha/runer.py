from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from get_captcha import settings
from get_captcha.spiders.captcha import CaptchaSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(CaptchaSpider)

    process.start()