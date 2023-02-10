Шаги для запуска на вашей системе:

1. git clone https://github.com/ananos548/django_stripe
2. docker-compose build
3. docker-compose up
4. Перейти на http://127.0.0.1:8000/

основные ссылки:
http://127.0.0.1:8000/item/{id} - информация о выбранном Item и кнопка для оплаты
http://127.0.0.1:8000/buy/{id} - информация об Stripe Session Id
