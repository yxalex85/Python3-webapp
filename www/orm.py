#!/user/bin/env python3
# _*_ coding: utf-8 _*_

import asyncio, logging
import aiomysql

# SQL语句反馈
def log(sql, args=()):
    logging.info('SQL: %s, %s' % (sql, args))

async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
    )

#单独封装select
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    #以上下文方式打开conn连接，无需再调用conn.close()
    #或-->with await __pool as conn:
    async with __pool.get() as conn: #从连接池获取一个connection
         # 创建一个DictCursor类指针，返回dict形式结果集
         # 以上下文方式创建cur指针，无需在调用cur.close()
         async with conn.cursor(aiomysql.DictCursor) as cur: #获取游标cursor
             await cur.execute(sql.replace('?', "%s"), args or ())
             if size:
                 rs = await cur.fetchmany(size)
             else:
                 rs = await cur.fetchall()
    logging.info('rows returned: %s' % len(rs))
    return rs

#封装insert, update, delete
async def execute(sql, args, autocommit=True):
    log(sql,args)
    with await __pool as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback() #如果没有自动commit则回滚
            raise e
        return affected

#  创建占位符，用于insert, update, delete语句
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

from orm import Model, StringField, IntegerField
class User(Model): #这里的Model是orm框架提供的父类，下面的IntergerField等也是orm框架提供的
    __table__ = 'users' # table name
    # the following properties represent the column's name of table 'user'
    # id, name is the name of the column
    id = IntegerField(primary_key=True)
    name = StringField()

class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(255)'):
        super(StringField, self).__init__(name, ddl, primary_key, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntegerField, self).__init__(name, 'bigint', primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=None):
        super(BooleanField, self).__init__(name, 'boolean', False, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super(TextField, self).__init__(name, 'Text', False, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=None):
        super(FloatField, self).__init__(name, 'real', primary_key, default)

class Model()