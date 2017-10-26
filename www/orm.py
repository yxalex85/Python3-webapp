#!/user/bin/env python3
# _*_ coding: utf-8 _*_

import asyncio, logging
import aiomysql

async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306)

    )
