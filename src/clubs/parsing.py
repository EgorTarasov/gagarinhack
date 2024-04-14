import datetime
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

from news.models import NewsDao


def parse_ithub_news():
    res = []
    base_url = "https://ithub.ru"
    num_pages = 30
    current_year = 2024
    last_month = 12
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}/all-news/page_{page_number}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при запросе страницы {url}")
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        news_on_page = soup.find_all("a", class_="news-article", href=True)
        for news in news_on_page:
            try:
                page_url = f"{base_url}{news['href']}"
                response = requests.get(page_url)
                if response.status_code != 200:
                    print(f"Ошибка при запросе страницы {page_url}")
                    continue
                soup = BeautifulSoup(response.content, "html.parser")
                title = markdownify(soup.find("title").text)
                date = soup.find("p", class_="date")
                date = parse_date(date.string, current_year)
                if date.month > last_month:
                    current_year -= 1
                last_month = date.month
                image_link = soup.find_all("img")[2]["src"]
                if not image_link.startswith("http"):
                    image_link = base_url + image_link
                text = soup.find("article", id="body_news")
                text = markdownify(text.text).replace("\n", "")
                news_index = int(news['href'].split('/')[-1])
                # print(news_index, date, title, image_link)
                data = NewsDao(
                    id=news_index,
                    title=str(title),
                    created_at=date,
                    description=str(text),
                    image_link=image_link
                )
                res.append(data)
            except BaseException as e:
                continue
    return res


russian_months = ["янв", "фев", "мар", "апр", "ма", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]


def parse_date(date: str, year: int) -> datetime:
    day, month = date.split(" ")
    date = datetime.date(day=int(day), month=1, year=1)
    for ind, russian_month in enumerate(russian_months, start=1):
        if month.lower().startswith(russian_month):
            date = date.replace(month=ind, year=year)
            break
    else:
        print(day, month)
    return date


if __name__ == "__main__":
    print(parse_ithub_news())
