import os
import requests
from pyquery import PyQuery as pq


class Model():
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """

    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def get(url, filename):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached_mtime'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def movie_from_li(li):
    """
    从一个 li 里面获取到一个电影信息
    """
    e = pq(li)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('h2').text()
    # m.other = e('.other').text()
    m.score = e('.total').text() + e('.total2').text()
    m.quote = e('.mt3').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.number').find('em').text()
    return m


def save_cover(movies):
    for m in movies:
        filename = '{}.jpg'.format(m.ranking)
        get(m.cover_url, filename)


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    # http: // www.mtime.com / top / movie / top100 / index - 5.html
    if url.endswith('html'):
        filename = url.split('-', 1)[-1]
    else:
        filename = '1.html'
    page = get(url, filename)
    e = pq(page)
    items = e('.top_list').find('li')
    # 调用 movie_from_li
    movies = [movie_from_li(i) for i in items]
    save_cover(movies)
    return movies


def main():
    for i in range(1, 11):
        if i == 1:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
        movies = movies_from_url(url)
        print('top100 movies', movies)


if __name__ == '__main__':
    main()
