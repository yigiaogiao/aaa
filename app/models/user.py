# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/3/25 18:31
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from math import floor
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    # 虚拟货币
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 对传入的值与加密的password进行加密在比较
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 对交易模型中的isbn进行验证
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushubook = YuShuBook()
        yushubook.search_by_isbn(isbn)
        if not yushubook.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不能同时成为赠送者和索要者

        # 既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn
                                       , launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn
                                       , launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def can_send_drift(self):
        """判断鱼豆大于等于1和索取两本书且自己送一本书"""
        if self.beans < 1:
            return False
        # 赠送了多少书籍
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        # 获取了多少书籍
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if \
            floor(success_receive_count / 2) <= floor(success_gifts_count) \
            else False

    # 生成token令牌
    def generate_token(self, expiration=600):
        #expiration参数是token失效时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    # 更改密码的方法
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    # def get_id(self):
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
