import os
import requests
from pyquery import PyQuery as pq
import config
from bs4 import BeautifulSoup


def get(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64)'
                      'AppleWebKit / 537.36(KHTML, likeGecko)'
                      'Chrome / 63.0.3239.84'
                      'Safari / 537.36',
        'Cookie': config.cookie,
    }
    r = requests.get(url, headers=headers)
    page = r.content
    return page


def main():
    url = 'https://www.zhihu.com'
    page = get(url)
    soup = BeautifulSoup(page.decode())
    print(soup.prettify())


if __name__ == '__main__':
    main()
