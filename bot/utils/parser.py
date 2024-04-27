from bs4.element import Tag
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_parser_object(url: str) -> BeautifulSoup:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) \
            Chrome/121.0.0.0 Safari/537.36',
    }
    html_content = requests.get(url=url, headers=headers).text.encode('utf-8')
    parser = BeautifulSoup(markup=html_content, features='html.parser')
    return parser


def get_text(html_element: Tag | str) -> str | None:
    if html_element is None:
        return None
    if isinstance(html_element, Tag):
        text = html_element.text
    else:
        text = html_element
    text = text.strip().replace('\n', ' ')
    while text.count('  ') > 0:
        text = text.replace('  ', ' ')
    return text


def get_date(html_element: Tag | None | str) -> datetime | None:
    if html_element is None:
        return None
    if isinstance(html_element, Tag):
        date = get_text(html_element).split(' ')[0]
    else:
        date = html_element
    year, month, day = map(int, date.split('.'))
    return datetime(year=year, month=month, day=day)


def get_time(time: str, date: datetime | None = None) -> datetime:
    if date is None:
        date = datetime.now()
    hour, minute = map(int, time.split(':'))
    return date.replace(minute=minute, hour=hour, second=0, microsecond=0)


def get_hltv_link(path: str):
    return f"https://hltv.org{path}"
