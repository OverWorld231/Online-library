# Парсинг библиотеки

## Описание
Проект создан для парсинга онлайн-библиотеки. Загружает содержание книг и обложек в разные папки.

## Установка
Скачайте необходимые файлы затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей и установить зависимости. Зависимости можно установить командой представленной ниже.

Установите зависимости командой:
```
pip install -r requirements.txt
```
## Пример запуска скрипта
Для запуска скрипта у вас должен быть установлен Python3.

Для запуска программы укажите страницу католога с научной фантастикой, с которой нужно начать скачивать, после аргумента --start_page и страницу каталога с научной фантастикой, до которой нужно скачивать, после агрумента --end_page. Укажите аргумент --skip_txt, если не хотите скачивать текст книг, и аргумент --skip_images, если не хотите скачивать обложки к книгам. Укажите путь для скачивания книг и обложек после:
```
python main.py --start_id <страница> --end_page <страница> --skip_txt --skip_imgs*
```
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/)


