# Проект YaMDb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 10. Итоговый проект. API для YaMDb.

## Описание

Проект YaMDb собирает отзывы `Review` пользователей на произведения `Title`. Произведения делятся на категории: `Книги`, `Фильмы`, `Музыка`. Список категорий `Category` может быть расширен. Сами произведения в YaMDb не хранятся. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы `Review` и выставляют произведению рейтинг.
# Проект YaMDb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 10. Итоговый проект. API для YaMDb.

## Описание

Проект YaMDb собирает отзывы `Review` пользователей на произведения `Title`. Произведения делятся на категории: `Книги`, `Фильмы`, `Музыка`. Список категорий `Category` может быть расширен. Сами произведения в YaMDb не хранятся. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы `Review` и выставляют произведению рейтинг.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ValleLari/api_yamdb.git
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Импорт данных 

Импорт данных из static/data:
```
python3 manage.py import_data
```

Внимание, если при импорте возникают конфликты с ранее загруженными данными, то можно запустить скрипт с аругментов для предварительной очистки всех моделей:
```
python3 manage.py import_data --clear
```

Правда, в этом случае и суперюзер будет удален, так что скорее всего придется сделать 
```
python manage.py createsuperuser
```
Суперюзером можно войти в админку и посмотреть заполненность данных.

## Разработчики

- Валентина Ларина(TeamLead) - Review/Comments

- Иван Мамичев - Auth/Users

- Виктория Галиуллина - Categories/Genres/Titles
