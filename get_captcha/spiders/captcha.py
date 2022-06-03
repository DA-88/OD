import scrapy
from scrapy.http import HtmlResponse
from get_captcha.items import ImageItem
import os
from preprocess_img import PreprocessImage

class CaptchaSpider(scrapy.Spider):
    name = 'captcha'
    allowed_domains = ['pb.nalog.ru']
    start_urls = ['https://pb.nalog.ru/captcha-dialog.html?aver=2.8.7&sver=4.39.5&pageStyle=GM2']

    def start_requests(self):
        for i in range(1):
            dir = f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\{i}"
            if not os.path.exists(dir): os.mkdir(dir)
            request = scrapy.Request("https://pb.nalog.ru/captcha-dialog.html?aver=2.8.7&sver=4.39.5&pageStyle=GM2",
                           callback=self.parse, meta={'number': i})
            yield request

    def parse(self, response: HtmlResponse):
        a = f"https://pb.nalog.ru{response.xpath('//img//@src')[0].root}"
        a = a.replace('version=2', 'version=3')
        i = 0
        while i <= 1000:
            req = scrapy.Request(a, meta={"number": response.meta['number'],
                                          'sub_number': i}, callback=self.download_img)
            yield req
            i += 1

    def download_img(self, response):

        with open(f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\{response.meta['number']}\\{response.meta['sub_number']}.bmp", 'wb') as img_file:
            img_file.write(response.body)
        # im = PreprocessImage()
        # im.ImgLoad(f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\{response.meta['number']}\\{response.meta['sub_number']}.bmp")
        # i = 0
        # while i <= 5:
        #     dir = f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\{response.meta['number']}\\{i}"
        #     if not os.path.exists(dir): os.mkdir(dir)
        #     im.save_digit(number=i, path=f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\{response.meta['number']}\\{i}\\")
        #     i += 1

