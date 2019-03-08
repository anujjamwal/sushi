import json

import psutil
from aiohttp import web


async def stats(_):
    resp = web.Response()
    stats = dict(mem=psutil.virtual_memory()._asdict(),
                 swap=psutil.swap_memory()._asdict(),
                 cpu=psutil.cpu_times_percent()._asdict())
    resp.body = json.dumps(stats)
    return resp


async def health(_):
    resp = web.Response()
    resp.body = 'OK'
    return resp
