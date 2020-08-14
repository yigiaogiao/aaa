# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/2/19 12:27

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    # Column
    # 代表通过该插件将代码中的字段映射到数据库中完成初始化工作
    # autoincrement
    # 是否自动增值
    # Nullable = false
    # 不能为空，默认为True可以为空
    # Unique = true
    # 不能出现重复值
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    # 装帧版本
    binding = Column(String(20))
    # 出版社
    publisher = Column(String(50))
    # 价格
    price = Column(String(20))
    pages = Column(Integer)
    # 出版日期
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    # 简介
    summary = Column(String(1000))
    image = Column(String(50))
