# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/4/3 12:18

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship


from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)
    isbn = Column(String(15), nullable=False)

    # 通过isbn调用api查询图书的具体信息，然后通过viewmodel层进行数据筛选
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 赠送清单显示我最近赠送的书籍
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    # 通过isbn列表计算出某个礼物的具体数量
    @classmethod
    def get_gift_counts(cls, lisbn_list):
        from app.models.gift import Gift
        # 根据传入的一组isbn，到wish表中计算出某个礼物的wish心愿数量
        # filter只会接收一些条件表达式
        # mysql in查询
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(lisbn_list),
            Gift.status == 1).group_by(Gift.isbn).all()
        # 用字典来增加代码可读性
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list