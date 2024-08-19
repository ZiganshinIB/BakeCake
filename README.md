# Сервис BakeCake
**В разарботки!**
<br>
Сайт магазина тортов на заказ 
![img.png](git_media/index.png)
![img_1.png](git_media/lk.png)
## Цели
#### Интернет магазин для заказа тортов это для клиентов этого магазина
 - Способ удивить гостей на празднике (свадьба, день рождения, корпоратив)
 - Возможность заказать себе вкусный десерт 
 - Простой способ проявить внимание человеку, у которого праздник

#### Используя это приложение вы:
 - Получить новый источник заказов
 - Автоматизировать приём заказов (не по телефону через удалённого менеджера по продажам, а автоматически)

## Требования к системе
* OS: Windows 10 или выше, Linux, Mac OS
* ПО(Soft): Python 3.9, 3.10
* Пакеты: смотреть в [requirements.txt](./requirements.txt)

# Быстрый старт 
1. Склонировать проект
```shell
git clone https://github.com/ZiganshinIB/BakeCake.git
```
2. Создание виртуальной среды
```shell
python -m venv .venv
```
_Python должен быть версии 3.9 или 3.10!_
3. Активируйте виртуальную среду
```shell
source ./.venv/bin/activate
```
3. Часть данных проекта берётся из переменных окружения. Чтобы их определить, создайте файл .env и присвойте значения переменным окружения в формате: ПЕРЕМЕННАЯ=значение.
```shell
touch .env
```
Основые переменные:
```text
DJANGO_SECRET_KEY='django_secret_key'              # секретный ключ django проекта
```
Опцианальные:
```shell
DJANGO_DEBUG=true                                 # отладочный режим
DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'        # белый список хостов
DB_URL="postgres://user:pass@host:port/db"        # Адресс базыданных в виде DSN
EMAIL_HOST_USER=test@local.dj                     # Адресс электронный почты сайта
EMAIL_HOST_PASSWORD=password                      # Пароль от почты
NGINX_DOMAINS=http://mysite.ru                    # Nginx веб сервер, для работы через Nginx
```
4. Установите зависимости
```shell
pip install -r requirements.txt
```
5. Мигруруйте схемы БД
```shell
pytho manage.py migrate
```
6. Соберите коллекцию статичных файлов 
```shell
python manage.py collectstatic
```
7. Запустите сайт 
```shell
python manage.py runserver
```


