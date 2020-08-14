# -*-coding:utf-8-*- 
# author: xdz
# @Time :2020/6/1 13:35
from collections import namedtuple

from app.view_models.book import BookViewModel

# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gift_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()
        pass

    def __parse(self):
        temp_gifts = []
        for gift in self.__gift_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
