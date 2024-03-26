import scrapy


class MaksavitPagesSpider(scrapy.Spider):
    name = "maksavit_pages"
    allowed_domains = ["maksavit.ru"]
    start_urls = ["https://maksavit.ru/"]
    
    def __init__(self, region=None, category=None, 
                 subcategory=None, *args, **kwargs):
        
        super(MaksavitPagesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://maksavit.ru/{region}/catalog/{category}/{subcategory}"]

    def parse(self, response):
        print(response.status)
        print("================")



# scrapy crawl maksavit_pages -a region=novosibirsk -a category=materinstvo_i_detstvo -a subcategory=detskaya_gigiena
