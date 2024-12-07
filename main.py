import requests
import os
from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import argparse
import json

def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError

def get_category_book_urls(start_page, end_page):
    all_books_urls = []
    all_number_books = []
    for number in range(start_page,end_page):
        tululu_url =  f"https://tululu.org/l55/{number}"
        response = requests.get(tululu_url)
        response.raise_for_status()
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, "html.parser")
        book_selector = "table.d_book"
        book_urls = soup.select(book_selector)
        for book_url in book_urls:
            url = book_url.find("a")["href"]
            full_url = urljoin(tululu_url,url)
            split_url = urlsplit(url).path.split("/")[1]
            all_books_urls.append(full_url)
            all_number_books.append(split_url)
    return all_books_urls, all_number_books

def download_txt(url, filename, book_id, folder="books/"):
    params = {"id":book_id} 
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    file_path = os.path.join(f"{folder}{sanitize_filename(filename)}.txt")
    with open(file_path, "wb") as file:
        file.write(response.content)


def download_image(url, folder="images/"):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    image_name = urlsplit(url).path.split("/")[-1]
    file_path = os.path.join(folder, image_name)
    with open(file_path, "wb") as file:
        file.write(response.content)


def parse_book_page(response, book_url): 
    soup = BeautifulSoup(response.text, "lxml")
    title_book = soup.select_one("h1").text
    title, author = title_book.split(" :: ")
    book_image_selector = "div.bookimage img"
    book_image_url = soup.select_one(book_image_selector)["src"]
    full_image_url = urljoin(book_url, book_image_url)
    book_comments_selector = "div.texts span.black"
    book_comments = soup.select(book_comments_selector)
    comments = [book_comment.text for book_comment in book_comments]
    book_genres_selector = "span.d_book a"
    book_genres = soup.select(book_genres_selector)
    genres = [genre.text for genre in book_genres]
    about_book = {
        "genres": genres,
        "author": author,
        "title": title,
        "full_image_url": full_image_url,
        "comments": comments,
    }
    return about_book

def main():
    parser = argparse.ArgumentParser(
        description="Программа скачивает готовые книги с сайта с оболжками."
    )
    parser.add_argument("--start_page", type=int, default=1, help="Номер начальной книги")
    parser.add_argument("--end_page", type=int, default=702, help="Номер последней книги")
    parser.add_argument("--dest_folder", type=str, default="media", help="Путь к каталогу с результатами парсинга: картинкам, книгам, JSON.")
    parser.add_argument("--skip_imgs", action="store_true", help="Пропускает скачивание изображение")
    parser.add_argument("--skip_txt", action="store_true",  help="Пропускает скачивание текста")
    args = parser.parse_args()
    all_book_parameters = []
    book_urls, book_numbers = get_category_book_urls(args.start_page, args.end_page)
    for book_url, book_number in zip(book_urls, book_numbers):
        try:
            url = f"https://tululu.org/txt.php"
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            about_book = parse_book_page(response, book_url)
            all_book_parameters.append(about_book)
            filename = about_book["title"].strip()
            if not args.skip_imgs:
                download_image(about_book["full_image_url"])
            if not args.skip_txt:
                download_txt(url, filename, book_number[1:])
        except requests.exceptions.HTTPError:
            print("Книга не найдена")
        except requests.exceptions.ConnectionError:
            print("Повторное подключение к серверу")
            sleep(20)
    with open ("information_about_book.json","w", encoding='utf8') as json_file:
        json.dump(all_book_parameters,json_file,ensure_ascii=False)


if __name__ == "__main__":
    main()

