# Спайдер для магазина maksavit на фреймворке Scrapy

### **Usage**

Я сделал так чтобы Вы могли запустить проект просто запуском модуля. Находясь внутри фолдера spiders используйте

```
python maksavit_pages.py
```

В categories поместите ссылки из путей до категорий которые хотите спарсить ( минимум 3 )

Укажите количество товаров для каждой категории в параметре items_amount ( минимум 50 )

Укажите желаемый регион в параметре region

![1711579103800](image/Readme/1711579103800.png)

### Важно

Версия Scrapy 2.11.1

Для доступа к сайту нужны cookies, иначе 401. Cookies живут 15 минут

Я не реализовывал автоматическое добавление cookies, так как проект уже занял не мало времени

У меня есть 3 варианта решения данной проблемы, могу рассказать при встрече. Также интересно узнать Ваш подход.

В фолдере spiders Вы найдете пример аутпута.

Если Вы всё таки хотите запустить проект, то перейдите на сайт и через панель разработчика скопируйте с запроса cookies

![1711579483623](image/Readme/1711579483623.png)

Далее перейдите в модуль cookies.py и просто поместите данные из буффера в переменную cookie_string. Теперь у Вас 15 минут на проверку

### **Дополнительно**

В middlewares я всё же сделал набросок для будущего решения проблемы с доступом.

Также пришлось сделать свой ItemPipeline потому что дефолтное поведение не декодировало unicode символы в нормальный текст

Также имеет смысл сказать что я не проверял работу спайдера на всём сайте, нужна дополнительная работа по оценке качества данных. С данными в примере всё впорядке, но проверял я только 3, или 4 

Ещё добавлю что я принял решение обернуть проход по категории и страницам товаров в один спайдер. Это не самый лучший способ, но я решил сэкономить время и сопроводил код комментариями, надеюсь не устанете разбираться!

Очень надеюсь на Ваш фидбек!

Контакты:

почта - epguitars@yahoo.com

телеграм - @epguitars

Спасибо за возможность пройти тестовое задание! Всего наилучшего
