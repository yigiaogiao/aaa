# -*-coding:utf-8-*- 
# author: xdz
# @Time :2020/6/15 16:14
from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, ForeignKey


class Drift(Base):
    """
    一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)
    # 邮寄信息
    # 收件人姓名
    recipient_name = Column(String(20), nullable=False)
    # 收件人地址
    address = Column(String(100), nullable=False)
    # 留言
    message = Column(String(200))
    # 手机号
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者id
    gifter_id = Column(Integer)
    # 礼物的id号
    gift_id = Column(Integer)
    # 赠送者昵称
    gifter_nickname = Column(String(20))
    # 赠送状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
