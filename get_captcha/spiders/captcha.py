import scrapy
from scrapy.http import HtmlResponse
from get_captcha.items import ImageItem

class CaptchaSpider(scrapy.Spider):
    name = 'captcha'
    allowed_domains = ['pb.nalog.ru']
    start_urls = ['https://pb.nalog.ru/captcha-dialog.html?aver=2.8.7&sver=4.39.5&pageStyle=GM2']

    def start_requests(self):
        for i in range(1):
            request = scrapy.Request("https://pb.nalog.ru/captcha-dialog.html?aver=2.8.7&sver=4.39.5&pageStyle=GM2",
                           callback=self.parse, meta={'number': str(i)})
            yield request

    def parse(self, response: HtmlResponse):
        a = f"https://pb.nalog.ru{response.xpath('//img//@src')[0].root}"
        a = a.replace('version=2', 'version=3')

        item = ImageItem(image_urls=[a], file_name=f"{response.meta['number']}_1.jpg")
        yield item
        item = ImageItem(image_urls=[a], file_name=f"{response.meta['number']}_2.jpg")
        yield item
        item = ImageItem(image_urls=[a], file_name=f"{response.meta['number']}_3.jpg")
        yield item
