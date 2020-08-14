# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/3/13 12:20


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        # '、'.join(data['author'])把列表之间的作者通过顿号分隔
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        # 使用book变量去便利api返回的列表类型数据中的books的值中的内容，
        # 然后形成新的列表数据
        self.books = [BookViewModel(book) for book in yushu_book.books]