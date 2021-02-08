# Сборщик активной аудитории из социальных сетей

Данная программа предназначена для формирования списков активных пользователей. Доступные сети: VK, Facebook, Instagram.

## Примеры вывода
#### для VK
 ```
 ----Целевая активная аудитория:----
{452468496, 587506745, 209512419, 618076709}
```
#### для Facebook
 ```
----Комментаторы за последний месяц:----
{'2853121058297981'}
----------------------------
----Реакции пользователей:----
{'2853121058297981': {'ANGRY': 0, 'HAHA': 0, 'LIKE': 2, 'LOVE': 1, 'SAD': 0, 'THANKFUL': 0, 'WOW': 0}}
```
#### для Instagram
 ```
----Комментаторы за последние 3 месяца с кол-вом комментариев----:
{192999764: 7,  1683400985: 3, ... }
----Комментаторы за последние 3 месяца с кол-вом постов, которые комментировали----:
{192999764: 3, 45230642069: 1, ... }
```


## Как установить

Для запуска программы у вас уже должен быть установлен Python 3. 

Установите зависимости командой в терминале:

```
$ pip install -r requirements.txt
```

Далее, создайте файл `.env` в корневой папке приложения и заполните по шаблону ниже, исходя из нужных вам соц.сетей:
```
INSTAGRAM_USERNAME=имя пользователя в инстаграм
INSTAGRAM_PASSWORD=пароль в инстаграм

VK_SERVICE_KEY=создайте приложение в VK и скопируйте сюда сервисный ключ
VK_GROUP_NAME=введите имя группы, его можно взять из ссылки на сообщество

FACEBOOK_GROUP_ID=введите id группы, его можно взять из ссылки на сообщество
FACEBOOK_ACCESS_TOKEN=создайте приложение в Facebook и скопируйте сюда ключ доступ (получите абсолютно все разрешения для него... на всякий случай)
```

## Аргументы

Скрипт принимает на вход один обязательный аргумент:
1. `vk` - для Вконтакте
2. `facebook` - для Facebook
3. `instagram` - для Instagram


## Пример запуска
```
$ python main.py instagram
<выдача для Instagram>
$ python main.py vk
<выдача для VK>
$ python main.py facebook
<выдача для Facebook>
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
