# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/2/13 13:54

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
