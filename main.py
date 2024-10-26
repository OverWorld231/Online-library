import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


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
    title_book = soup.find("h1").text
    title, author = title_book.split(" :: ")
    book_image_url = soup.find("div", class_="bookimage").find("img")["src"]
    full_image_url = urljoin(book_url, book_image_url)
    book_comments = soup.find_all("div", class_="texts")
    comments = [book_comment.find("span", class_="black").text for book_comment in book_comments]
    book_genres = soup.find("span", class_="d_book").find_all("a")
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
    parser.add_argument("--start_id", type=int, default=1, help="Номер начальной книги")
    parser.add_argument("--end_id", type=int, default=10, help="Номер последней книги")
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id):
        try:
            url = f"https://tululu.org/txt.php"
            book_url = f"https://tululu.org/b{book_id}/"
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            about_book = parse_book_page(response, book_url)
            filename = about_book["title"].strip()
            download_image(about_book["full_image_url"])
            download_txt(url, filename, book_id)
        except:
            print("Книга не найдена")


if __name__ == "__main__":
    main()
