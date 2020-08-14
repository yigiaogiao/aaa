# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/2/13 15:18
'''
获取api数据
'''
from flask import current_app

from app.libs.httpd import HTTP


class YuShuBook:
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = 'http://t.talelin.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            # 该方法将空列表books实现追加获取到的数据data中的数据
            self.books.append(data)

    def __fill_collenction(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = YuShuBook.keyword_url.format(keyword, current_app.config
        ['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collenction(result)

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
