# coding: utf-8

from datetime import datetime

from flask import Flask
from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import request

app = Flask(__name__)

HouseInfo = Query(Object.extend('HouseInfo'))


@app.route('/')
def index():
    return u"测试成功"


'''http://192.168.13.57:3000/check_agent?phone=13691400786'''


@app.route('/check')
def _indexc():
    phone = request.args.get("phone").strip()

    phone = Query(HouseInfo).equal_to('phone', phone).find()

    a = {x.get('xiaoqu').strip() for x in phone}

    if not phone:
        return json.dumps({'agent': 'no', 'data': []})

    print phone[-1].get('owner'), '\n\n'

    if len(a) >= 2 or u'经纪人' in phone[-1].get('owner'):
        return json.dumps({'agent': 'yes',
                           'data': [{'img': x.get('img'),
                                     'xiaoqu': x.get('xiaoqu'),
                                     'weizhi': x.get('weizhi'),
                                     'phone': x.get('phone'),
                                     'objectId': x.get('objectId'),
                                     'price': x.get('price')
                                     } for x in phone]})

    return json.dumps({'agent': 'no',
                       'data': [{'img': x.get('img'),
                                 'xiaoqu': x.get('xiaoqu'),
                                 'weizhi': x.get('weizhi'),
                                 'phone': x.get('phone'),
                                 'objectId': x.get('objectId'),
                                 'price': x.get('price')
                                 } for x in phone]})


@app.route('/check_agent')
def _index1():
    phone = request.args.get("phone").strip()
    b = Query(HouseInfo).equal_to('phone', phone).find()

    a = {x.get('xiaoqu').strip() for x in b}
    if len(a) >= 2:
        return json.dumps({'agent': 'yes',
                           'data': [{'img': x.get('img'),
                                     'xiaoqu': x.get('xiaoqu'),
                                     'weizhi': x.get('weizhi'),
                                     'phone': x.get('phone'),
                                     'price': x.get('price'),
                                     'objectId': x.dump().get('objectId')
                                     } for x in b]})

    return json.dumps({'agent': 'no',
                       'data': [{'img': x.get('img'),
                                 'xiaoqu': x.get('xiaoqu'),
                                 'weizhi': x.get('weizhi'),
                                 'phone': x.get('phone'),
                                 'price': x.get('price'),
                                 'objectId': x.dump().get('objectId')
                                 } for x in b]})


'''http://192.168.13.57:3000/house_info?id=56a6048ac4c9710053e7d6c6'''


@app.route('/house_info')
def _index2():
    data = request.args.get("id")
    return json.dumps(Query(HouseInfo).equal_to('objectId', data).first().dump())


@app.route('/house_info1')
def ind():
    data = request.args.get("id")

    # if not data:
    #     return
    house_info = Query(HouseInfo)
    house_info.equal_to('objectId', data)
    house_info = house_info.find()
    house_info.pop('_id')

    return json.dumps(house_info)


# @app.route('/all_phone')
# def _index4():
#     from collections import Counter
#
#     # from leancloud import Query
#     #
#     # result = Query.do_cloud_query('select phone from HouseInfo').results
#     # return Counter([x.get('phone') for x in db.test.find()])
#     # a = [x.get('phone').strip() for x in Query(HouseInfo).limit(1000).find()]
#     # return json.dumps(Counter(a))
#     # return 'ok'

# return json.dumps(Counter([x.get('phone') for x in db.test.find()]))


@app.route('/time')
def time():
    return str(datetime.now())


import json


class HouseInfo(Object): pass


@app.route('/test')
def _index3():
    a = [x.dump() for x in Query(HouseInfo).equal_to('phone', '1830118****').find()]
    return json.dumps(a)


# json.dumps(Query(HouseInfo).limit(1).first().dump())
# json.dumps(Query(HouseInfo).equal_to('phone', '1830118****').first().dump())


@app.route('/img', methods=['POST'])
def _oo():
    a = request.files.get('img')
    a.save('./static/{}'.format(a.filename))

    return 'http://192.168.13.57:3000/static/{}'.format(a.filename)


# @app.route('/app')
# def show():
#     try:
#         todos = Query(Todo).descending('createdAt').find()
#     except LeanCloudError, e:
#         if e.code == 101:  # 服务端对应的 Class 还没创建
#             todos = []
#         else:
#             raise e
#     return json.dumps([x.get('content') for x in todos])


@app.route('/app/add')
def add():
    '''
    for x in Query(Todo).not_equal_to('hello', 'hello').find():
        x.set('hello','world')
        x.save()
    '''

    from collections import Counter

    a = {x.get('xiaoqu').strip() for x in Query(HouseInfo).equal_to('phone', '13810072091').find()}

    if len(a) >= 2:
        return



        # for x in Query(HouseInfo).find():
        #
        #     print x.get('phone')

        # if not x.get('source'):
        #     x.destroy()

    print "ooook"
    # x.save()

    # todo = Todo().set("hello", 'hello').set('sex', 'man').set('age', 123).save()
    return "ok"

# @app.route('/t')
# def _tt():
#     db = pymongo.MongoClient("mongodb://localhost:27017/spyder").spyder
#
#     b = [x for x in db.test.find()]
#
#     bbb = []
#
#     import random

# for x in b:
#     if x.get('phone')[-4:] == '****':
#         db.test.update({'_id': x.get("_id")},{'$set':{'phone':x.get('phone')[0:-4]+''.join([str(i) for i in random.sample([1,2,3,4,5,6,7,8,9,0],4)])}})

# for x in b:
#     if not x.get('objectId'):
#         db.test.remove({'_id': x.get("_id")})

# for x in b:
# print {'key':x.get('phone')+x.get('owner')+x.get('huxing')+x.get('louceng')}
# if x.get('phone') :
# db.test.update({'_id': x.get("_id")},{'$set':{'key':x.get('phone')+x.get('owner')+x.get('huxing')+x.get('louceng')}})


# for x in b:
#     if x.get('key') in bbb:
#         db.test.remove({'_id': x.get("_id")})
#     else:
#         bbb.append(x.get('key'))

# for i in xrange(5):
#     a = Query(HouseInfo).limit(1000).skip(i * 1000).find()
#     if not a:
#         break
#     [db.test.insert(x.dump()) for x in a if x.dump().get('objectId') not in b]  # {'objectId':x.get('objectId')},

# return 'ok'
