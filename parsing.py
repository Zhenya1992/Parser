import sqlite3
import requests
from bs4 import BeautifulSoup


def get_hacker_news_title():
    url = "https://habr.com/ru/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = [title.text for title in soup.select("h2.tm-title a")]
    return titles


def save_to_sqlite(titles, db_name="habr.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habr(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE )
    """)

    for title in titles:
        try:
            cursor.execute("INSERT INTO habr (title) VALUES (?) ON CONFLICT(title) DO NOTHING", (title,))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    cursor.close()
    conn.close()


def save_to_file(titles, filename="habr.txt"):
    with open(filename, "w", encoding="UTF-8") as file:
        for title in titles:
            file.write(f"{title}\n")
        print(f"Заголоки статей сохранены в {filename}")


if __name__ == "__main__":
    news_titles = get_hacker_news_title()
    # save_to_sqlite(news_titles)
    # for id, title in enumerate(news_titles, 1):
    #     print(f"{id}: {title}")
    save_to_file(news_titles)
    for id, title in enumerate(news_titles, 1):
        print(f"{id}: {title}")
