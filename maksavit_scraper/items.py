# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


def check_discount(old_price: float, current_price: float):
    """ calculate discount """
    return round((1 - current_price / old_price) * 100)


@dataclass
class PriceData:
    original: float = None
    current: float = None
    sale_tag: str = None

    def __post_init__(self):
        if self.current is None:
            self.current = self.original
        
        if self.sale_tag is None and self.original:
            self.sale_tag = f"Скидка {check_discount(self.original, self.current)}%"
        
        else:
            self.sale_tag = None


@dataclass
class StockData:
    in_stock: bool
    count: int = 0


@dataclass
class MediaAssets:
    main_image: str = None
    set_images: list[str] = None
    view360: list[str] = None
    video: list[str] = None

    def __post_init__(self):
        if not self.set_images:
            self.set_images = [self.main_image]


@dataclass
class MaksavitScraperItem:
    """ Модель данных для товара с maksavit.ru """
    
    # Дата и время сбора товара в формате timestamp.
    timestamp: int 
    
    # Уникальный код товара.
    RPC: str 
    
    # Ссылка на страницу товара.
    url: str 
    
    # Заголовок/название товара 
    # *Если в карточке товара указан цвет или объем, но их нет в названии, 
    # необходимо добавить их в title в формате: "{Название}, {Цвет или Объем}").
    title: str 
    
    # Список маркетинговых тэгов, например: ['Популярный', 'Акция', 'Подарок']. 
    # Если тэг представлен в виде изображения собирать его не нужно.
    marketing_tags: list 
    
    # Информация о цене товара
    # "price_data": {
    #         "current": float,  # Цена со скидкой, если скидки нет то = original.
    #         "original": float,  # Оригинальная цена.
    #         "sale_tag": "str"  # Если есть скидка на товар то необходимо вычислить процент скидки и записать формате: "Скидка {discount_percentage}%".
    #           },
    price_data: PriceData

    # Словарь с информацией о наличии товара
    #   stock: {
    #    "in_stock": bool,  # Есть товар в наличии в магазине или нет.
    #    "count": int  # Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0.
    #     }     
    stock: dict

    # Бренд товара.
    brand: str = None

    # Иерархия разделов
    # Например: [
    #            'Игрушки', 
    #            'Развивающие и интерактивные игрушки', 
    #            'Интерактивные игрушки'
    #           ]
    section: list[str] = None
    
    # Данные о медиа
    #    "assets": {
    #         "main_image": "str",  # Ссылка на основное изображение товара.
    #         "set_images": ["str"],  # Список ссылок на все изображения товара.
    #         "view360": ["str"],  # Список ссылок на изображения в формате 360.
    #         "video": ["str"]  # Список ссылок на видео/видеообложки товара.
    #          }
    assets: MediaAssets = None

    # Дополнительная информация о товаре
    #     "metadata": {
    #    "__description": "str",  # Описание товара
    #    "KEY": "str",
    #    "KEY": "str",
    #    "KEY": "str"
    #    }
    # Также в metadata необходимо добавить все характеристики товара которые могут быть на странице.
    # Например: Артикул, Код товара, Цвет, Объем, Страна производитель и т.д.
    # Где KEY - наименование характеристики.
    metadata: dict = None

    # Кол-во вариантов у товара в карточке 
    # (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).
    variants: int = 0
