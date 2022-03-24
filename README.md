# API_YAMDB
## API для проекта api_yamdb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

- Добавление постов
- Возможность добовлять комментарии к постам
- Возможность подписываться на авторов постов
- Принадлежность постов к группам
- ✨Аутентификация с помощью JWT✨

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/jamsi-max/api_yamdb.git
```
```sh
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```sh
python3 -m venv env
```
> для Linux:
```sh
source env/bin/activate
```
> для Windows:
```sh
venv\Scripts\acrivate
```
Обновить pip:
```sh
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python3 manage.py migrate
```
Запустить проект:
> для Windows:
```sh
python manage.py runserver
```
> для Linux:
```sh
python3 manage.py runserver
```
## Автор

```sh
Команда № 8 ©
```

## Лицензия

MIT



