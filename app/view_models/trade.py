# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/4/10 19:55


class TradeInfo:
    def __init__(self, goods):
        # 两张表返回的数据是一组，需要来记录有多少的赠送或心愿
        self.total = 0
        # 实际数据
        self.trades = []
        self.__parse(goods)

    # 一组数据处理
    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    # 单数据处理
    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )

