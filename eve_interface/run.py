#coding: utf-8
from eve import Eve

application = Eve()

if __name__ == '__main__':
    application.run(host="0.0.0.0",port=5002)
