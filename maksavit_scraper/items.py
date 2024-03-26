# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class MaksavitScraperItem:
    """ Target item model for maksavit.ru """
    
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
    
    # Бренд товара.
    brand: str 

    # Иерархия разделов
    # Например: [
    #            'Игрушки', 
    #            'Развивающие и интерактивные игрушки', 
    #            'Интерактивные игрушки'
    #           ]
    section: list[str] 
    
    # Информация о цене товара
    # "price_data": {
    #         "current": float,  # Цена со скидкой, если скидки нет то = original.
    #         "original": float,  # Оригинальная цена.
    #         "sale_tag": "str"  # Если есть скидка на товар то необходимо вычислить процент скидки и записать формате: "Скидка {discount_percentage}%".
    #           },

    price_data: dict

    # Словарь с информацией о наличии товара
    #    {
    #    "in_stock": bool,  # Есть товар в наличии в магазине или нет.
    #    "count": int  # Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0.
    #     }     
    stock: dict

    # Данные о медиа
    #    "assets": {
    #         "main_image": "str",  # Ссылка на основное изображение товара.
    #         "set_images": ["str"],  # Список ссылок на все изображения товара.
    #         "view360": ["str"],  # Список ссылок на изображения в формате 360.
    #         "video": ["str"]  # Список ссылок на видео/видеообложки товара.
    #          }
    assets: dict

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
    metadata: dict

    # Кол-во вариантов у товара в карточке 
    # (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).
    variants: int


