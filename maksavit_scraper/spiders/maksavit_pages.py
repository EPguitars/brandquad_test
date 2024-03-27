from datetime import datetime
from urllib.parse import urljoin

import scrapy
from scrapy.selector import Selector
from rich import print # удалить в конце

from headers import headers
from cookies import Cooker, cookie_string
from items import (MaksavitScraperItem,
                   PriceData,
                   StockData,
                   MediaAssets,
                   AdditionalInfo)


class MaksavitPagesSpider(scrapy.Spider):
    name = "maksavit_pages"
    allowed_domains = ["maksavit.ru"]
    base_url = "https://maksavit.ru"
    cookies = Cooker(cookie_string).cookie_dict

    def __init__(self, region=None, category=None, 
                 subcategory=None, *args, **kwargs):
        
        super(MaksavitPagesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://maksavit.ru/{region}/catalog/{category}/{subcategory}/"]


    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(
                url,
                callback=self.parse,
                headers=headers,
                cookies=self.cookies,
                dont_filter=True,
            )
            yield request


    def extract_cards(self, response) -> list[Selector]:
        cards = response.css("div.product-card-block")
        
        if cards:
            return cards 
        
        else:
            self.logger.warning("No cards found on the page, requires recheck")
            return None
        

    def parse_rpc(self, card: Selector) -> str:
        url = card.css("a.product-card-block__title::attr(href)")
        
        if url:
            code = url.get().split("/")[-2]
            return code
        
        else:
            self.logger.warning("No RPC found on the card")
            return None
        

    def parse_url(self, card: Selector) -> str:
        path = card.css("a.product-card-block__title::attr(href)")
        
        if path:
            url = urljoin(self.base_url, path.get())
            return url
        
        else:
            self.logger.warning("No URL found on the card")
            return None


    # title надо дополнить 
    # *Если в карточке товара указан цвет или объем, но их нет в названии, 
    # необходимо добавить их в title в формате: "{Название}, {Цвет или Объем}").
    def parse_title(self, card: Selector) -> str:
        title = card.css("a.product-card-block__title span::text")
        
        if title:
            return title.get()
        
        else:
            self.logger.warning("No title found on the card")
            return None


    def parse_marketing_tags(self, card: Selector) -> list[str]:
        tags = card.css("div.badges div::text")
        
        if tags:
            marketing_tags = [tag.strip() for tag in tags.getall() if len(tag.strip()) > 0]
            return marketing_tags
        
        else:
            self.logger.warning("No marketing tags found on the card")
            return None


    def parse_price_data(self, card: Selector) -> PriceData:
        old_price = card.css("div.product-price__old-price::text")
        current_price = card.css("div.product-price__current-price > span::text")

        if not old_price:
            return PriceData(
                current=int(current_price.re_first(r"\d+").strip()),
            )
        
        else:
            return PriceData(
                current=int(current_price.re_first(r"\d+").strip()),
                original=int(old_price.re_first(r"\d+").strip()),
            )


    def parse_stock_data(self, card: Selector) -> StockData:
        purchase_button = card.css("button.btn-buy-main::text")
        detect_word = "корзину"

        if purchase_button:
            if detect_word in purchase_button.get().lower():
                return StockData(
                    in_stock=True
                )
            
            else:
                return StockData(
                    in_stock=False
                )
        
        else:
            self.logger.warning("No stock data found on the card, requires recheck")
            return None


    def parse_brand(self, response) -> str:
        brand_selector = response.css("a.product-info__brand-value::text")

        if brand_selector:
            return brand_selector.get().strip()

        else:
            self.logger.warning("No brand found on the page, requires recheck")
            return None

    
    def parse_section(self, response) -> list[str]:
        breadcrumbs = response.css("ul.breadcrumbs > li")
        
        if breadcrumbs:
            section = [crumb.css("span::text").get().strip() for crumb in breadcrumbs[2:-1]]
            return section

        else:
            self.logger.warning("No section found on the page, requires recheck")
            return None


    def parse_media_assets(self, response) -> MediaAssets:
        main_image_path = response.css("div.product-picture > img::attr(src)")

        if main_image_path:
            main_image_url = urljoin(self.base_url, main_image_path.get())
            return MediaAssets(
                main_image=main_image_url,
            )

        else:
            self.logger.warning("No media assets found on the page, requires recheck")
            return None

    def parse_additional_info(self, response) -> AdditionalInfo:
        pass

    
    def parse(self, response):
        """
        Я использовал дефолтный метод для парсинга страницы с карточками
        товаров. В нем я извлекаю некоторые данные которые можно оттуда достать
        остальные данные я получаю переходя на страницу товара
        и в качестве колбэка использую уже метод parse_item
        """
        cards = self.extract_cards(response)


        if cards:
            for card in cards:
                item = MaksavitScraperItem(
                    timestamp=int(datetime.now().timestamp()),
                    RPC=self.parse_rpc(card),
                    url=self.parse_url(card),
                    title=self.parse_title(card),
                    marketing_tags=self.parse_marketing_tags(card),
                    price_data=self.parse_price_data(card),
                    stock=self.parse_stock_data(card)
                )
                
                yield scrapy.Request(
                    item.url,
                    callback=self.parse_item,
                    headers=headers,
                    cookies=self.cookies,
                    dont_filter=True,
                    meta={"item": item},
                )

                break
        
            
            else:
                pass
        
        else:
            self.logger.warning("No cards found on the page, requires recheck")
            return None


    def parse_item(self, response):
        
        item = response.meta["item"]

        item.brand = self.parse_brand(response)
        item.section = self.parse_section(response)
        item.assets = self.parse_media_assets(response)
        item.metadata = self.parse_additional_info(response)

        print(item)
        pass

# для теста
# scrapy crawl maksavit_pages -a region=novosibirsk -a category=materinstvo_i_detstvo -a subcategory=detskaya_gigiena
# 