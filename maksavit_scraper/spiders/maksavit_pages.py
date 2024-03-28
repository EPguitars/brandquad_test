from datetime import datetime
from urllib.parse import (urljoin, 
                          urlparse, 
                          parse_qsl, 
                          urlencode, 
                          urlunparse)

import scrapy
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from rich import print # удалить в конце

import __init__
from headers import headers
from cookies import Cooker, cookie_string
from items import (MaksavitScraperItem,
                   PriceData,
                   StockData,
                   MediaAssets)


class MaksavitPagesSpider(scrapy.Spider):
    name = "maksavit_pages"
    allowed_domains = ["maksavit.ru"]
    # этот аттрибут нужен для конструирования ссылок
    base_url = "https://maksavit.ru"
    cookies = Cooker(cookie_string).cookie_dict
    items_counter = dict()

    def __init__(self, 
                 region: str=None, 
                 categories: list[str]=None, 
                 items_amount: str=None,
                *args, 
                **kwargs):   
        """
        Метод переназначен для передачи аргументов
        """
        super(MaksavitPagesSpider, self).__init__(*args, **kwargs)
        self.items_counter = int(items_amount)

        if len(categories) < 3:
            raise CloseSpider("You should pass at least 3 categories")

        else:
            for category_path in categories:
                url = f"https://maksavit.ru/{region}/catalog/{category_path}"
                
                if category_path[-1] == "/":
                    self.start_urls.append(f"{url}")               
                else:
                    self.start_urls.append(f"{url}/")
        
        if items_amount:
            self.items_counter = int(items_amount)
        
        else:
            raise CloseSpider("You should pass at least 50 items to scrape")


    def start_requests(self):
        """
        Метод переназначен для передачи заголовков и куков
        """
        for url in self.start_urls:
            request = scrapy.Request(
                url,
                callback=self.parse,
                headers=headers,
                cookies=self.cookies,
                dont_filter=True,
                meta={"counter" : self.items_counter}
            )
            yield request


    def extract_cards(self, response) -> list[Selector]:
        """
        Генерирует селекторы для каждой карточки товара
        """
        cards = response.css("div.product-card-block")
        
        if cards:
            return cards 
        
        else:
            self.logger.warning("No cards found on the page, requires recheck")
            return None
        

    def parse_rpc(self, card: Selector) -> str:
        """
        Извлекает id товара
        """
        url = card.css("a.product-card-block__title::attr(href)")
        
        if url:
            code = url.get().split("/")[-2]
            return code
        
        else:
            self.logger.warning("No RPC found on the card")
            return None
        

    def parse_url(self, card: Selector) -> str:
        """ 
        Извлекает ссылку на страницу товара 
        """
        path = card.css("a.product-card-block__title::attr(href)")
        
        if path:
            url = urljoin(self.base_url, path.get())
            return url
        
        else:
            self.logger.warning("No URL found on the card")
            return None


    def parse_title(self, card: Selector) -> str:
        """
        Извлекает название товара
        """
        title = card.css("a.product-card-block__title span::text")
        
        if title:
            return title.get()
        
        else:
            self.logger.warning("No title found on the card")
            return None


    def parse_marketing_tags(self, card: Selector) -> list[str]:
        """ 
        Извлекает маркетинговые тэги 
        """
        tags = card.css("div.badges div::text")
        
        if tags:
            marketing_tags = [tag.strip() for tag in tags.getall() if len(tag.strip()) > 0]
            return marketing_tags
        
        else:
            self.logger.warning("No marketing tags found on the card")
            return None


    def parse_price_data(self, card: Selector) -> PriceData:
        """
        Извлекает информацию о цене товара
        """
        old_price = card.css("div.product-price__old-price::text")
        current_price = card.css("div.product-price__current-price > span::text")
        # Другой сценарий расположения цены
        if not current_price:
            current_price = card.css("span.isg-offer__tab-price::text")

        if not current_price:
            self.logger.warning("No current price found on the card, requires recheck")
            return None

        if not old_price:
            current = int("".join(current_price[0].re(r"\d+")).strip())
            return PriceData(
                current=current,
                original=current
            )

        else:
            current=int("".join(current_price[0].re(r"\d+")).strip())
            original=int("".join(old_price.re(r"\d+")).strip())

            return PriceData(
                current=current,
                original=original,
            )


        
    def parse_stock_data(self, card: Selector) -> StockData:
        """
        Извлекает информацию о наличии товара
        Наличие товара определяет по состоянию кнопки для заказа
        """
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
        """
        Извлекает бренд товара
        Информацию получает из блока "Изготовитель"
        """
        brand_selector = response.css("a.product-info__brand-value::text")

        if brand_selector:
            return brand_selector.get().strip()

        else:
            self.logger.warning("No brand found on the page, requires recheck")
            return None

    
    def parse_section(self, response) -> list[str]:
        """
        Извлекает хлебные крошки
        """
        breadcrumbs = response.css("ul.breadcrumbs > li")
        
        if breadcrumbs:
            section = [crumb.css("span::text").get().strip() for crumb in breadcrumbs[2:-1]]
            return section

        else:
            self.logger.warning("No section found on the page, requires recheck")
            return None


    def parse_media_assets(self, response) -> MediaAssets:
        """
        Извлекает данные о медиа
        На этом сайте у товаров из медиа только одно фото
        """
        main_image_path = response.css("div.product-picture > img::attr(src)")

        if main_image_path:
            main_image_url = urljoin(self.base_url, main_image_path.get())
            return MediaAssets(
                main_image=main_image_url,
            )

        else:
            self.logger.warning("No media assets found on the page, requires recheck")
            return None

    def parse_additional_info(self, response) -> dict:
        """
        Извлекает метаданные о товаре
        Все что в блоке "Описание" отправляет в __description
        для остального генерирует ключи по заголовкам
        """
        info_block = response.css("div.product-instruction__guide > div")
        additional_info = dict()

        if info_block:
            for article in info_block:
                
                header = article.css("h3::text").extract_first()
                content = article.css("::text").getall()
                
                if "Описание" == header:
                    additional_info["__description"] = content[1].strip()

                else:
                    additional_info[header] = content[1].strip()
            
            return additional_info
        
        else:
            self.logger.warning("No additional info found on the page, requires recheck")
            return None


    def add_query_to_url(self, existing_url, new_query_params):
        """ 
        Реконструирует url с новыми параметрами 
        """
        parsed_url = list(urlparse(existing_url))
        parsed_url[4] = urlencode(
            {**dict(parse_qsl(parsed_url[4])), **new_query_params})
        return urlunparse(parsed_url)


    def generate_next_page_url(self, response) -> str:
        """
        Генерирует ссылку на следующую страницу
        """
        pagination_bar = response.css("ul.ui-pagination > li")
        
        if pagination_bar:
            last_page = int(pagination_bar[-2].css("::text").get())
            current_page = int(pagination_bar.css("a.ui-pagination__item_checked::text").get())
            current_url = response.request.url
            next_page = current_page + 1

            if next_page <= last_page:
                return self.add_query_to_url(current_url, {"page": next_page})
            else:
                return None

        else:
            self.logger.warning("No pagination bar found on the page, requires recheck")
            return None


    
    def parse(self, response):
        """
        Я использовал дефолтный метод для парсинга страницы с карточками
        товаров. В нем я извлекаю некоторые данные которые можно оттуда достать
        остальные данные я получаю переходя на страницу товара
        и в качестве колбэка использую уже метод parse_item
        """
        # Для начала генерируем селекторы для каждой карточки товара
        cards = self.extract_cards(response)
        # Переносим счётчик в переменную
        items_counter = response.meta["counter"]

        if cards:
            # Проходимся по каждой карточке и извлекаем то что можно извлечь
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
                
                
                # Генерируем новый Request с собранными данными
                yield scrapy.Request(
                    item.url,
                    callback=self.parse_item_page,
                    headers=headers,
                    cookies=self.cookies,
                    dont_filter=True,
                    meta={
                        "item": item},
                )

                # Останавливаемся когда соберём указанное количество товаров
                items_counter -= 1

                if items_counter <= 0:
                    break
            
            else:
                # Отдаём новый Request со следующей страницей
                next_page = self.generate_next_page_url(response)

                if next_page:
                    yield scrapy.Request(
                        next_page,
                        callback=self.parse,
                        headers=headers,
                        cookies=self.cookies,
                        dont_filter=True,
                        meta={"counter": items_counter}
                    )
                else:
                    self.logger.info("No more pages, scraping category is done!")
                    return None

        else:
            self.logger.warning("No cards found on the page, requires recheck")
            return None


    def parse_item_page(self, response):
        """
        Собирает оставшуюся информацию и отправляет в пайплайн
        """
        item = response.meta["item"]

        item.brand = self.parse_brand(response)
        item.section = self.parse_section(response)
        item.assets = self.parse_media_assets(response)
        item.metadata = self.parse_additional_info(response)

        yield item


if __name__ == "__main__":
    # Для теста
    categories = ["kosmetologiya/ukhod_za_volosami/",
                    "materinstvo_i_detstvo/detskaya_gigiena",
                  "ukhod_za_bolnym/vzroslye_podguzniki"
                  ]
    
    process = CrawlerProcess(
        settings={
            'ITEM_PIPELINES': {
            "pipelines.MaksavitScraperPipeline": 300,
            }}
    )
    # parameter to write into json file
    process.crawl(MaksavitPagesSpider, 
                  region="novosibirsk", 
                  categories=categories,
                  items_amount=50,
                  )
    
    process.start()
    
    