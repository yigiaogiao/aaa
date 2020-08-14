# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/3/25 18:31
from flask import current_app

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from collections import namedtuple

from app.spider.yushu_book import YuShuBook

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 是否送出
    launched = Column(Boolean, default=False)
    isbn = Column(String(15), nullable=False)

    def is_yourself_gift(self, uid):
        """判断自己不能像自己请求书籍"""
        return True if self.uid == uid else False

    # 赠送清单显示我最近赠送的书籍
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    # 通过isbn列表计算出某个礼物的具体数量
    @classmethod
    def get_wish_counts(cls, lisbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn，到wish表中计算出某个礼物的wish心愿数量
        # filter只会接收一些条件表达式
        # mysql in查询
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(lisbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        # 用字典来增加代码可读性
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
    # 通过isbn调用api查询图书的具体信息，然后通过viewmodel层进行数据筛选
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 对象代表一个礼物，具体
    # 类代表礼物这个事物，他是抽象，不是具体的一个
    # 主页显示最近上传的前三十本书籍
    @classmethod
    def recent(cls):
        # 链式调用
        # 主体 query
        # 子函数
        # 触发语句 first（） all（）
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
