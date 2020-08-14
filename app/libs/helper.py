# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/2/13 14:43

'''

判断搜索关键字是文字还是isbn，再判断isbn是10位还是13位

'''


def is_isbn_or_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_q = word.replace('-', '')
    if '-' in word and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key