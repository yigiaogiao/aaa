"""
 Created by 七月 on 2018-2-1.
"""
from flask import jsonify, request, current_app, url_for, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
import json
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web

__author__ = '七月'


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 默认gift与wish两张表都查询不到为False
    has_in_gifts = False
    has_in_wishes = False
    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    # 判断用户是否登录
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,
                                isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,
                                isbn=isbn, launched=False).first():
            has_in_wishes = True
    # 数据库查询到的原始数据
    teade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    teade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    # 经过view——model修饰以后的数据
    trade_wish_model = TradeInfo(teade_wishes)
    trade_gift_model = TradeInfo(teade_gifts)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wish_model, gifts=trade_gift_model,
                           has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts)


@web.route('/test')
def test():
    r = {
        'name': None,
        'age': 18
    }
    # data['age']
    r1 = {

    }
    flash('hello,qiyue', category='error')
    flash('hello, jiuyue', category='warning')
    # 模板 html
    return render_template('test.html', data=r, data1=r1)


@web.route('/test1')
def test1():
    print(id(current_app))
    from flask import request
    from app.libs.none_local import n
    print(n.v)
    n.v = 2
    print('-----------------')
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    print('-----------------')
    return ''