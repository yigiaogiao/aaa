# -*-coding:utf-8-*- 
# author: xdz
# @Time :2020/6/28 9:15
from app.libs.enums import PendingStatus
from flask_login import current_user


class DriftColltion:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self.__parse(drift, current_user_id)
    # 判断是赠送者还是索取者
    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {'drift_id': drift.id,
             'you_are': you_are,
             'book_title': drift.book_title,
             'book_author': drift.book_author,
             'book_img': drift.book_img,
             # 实际显示赠送者或者索要者
             'operator': drift.requester_nickname if you_are != 'requester'
                 else drift.gifter_nickname,
             'date': drift.create_datetime.strftime('%Y-%m-%d'),
             'message': drift.message,
             'address': drift.address,
             'recipient_name':drift.recipient_name,
             'mobile': drift.mobile,
             # 枚举用法显示状态
             'status_str': pending_status,
             'status': drift.pending}
        return r
