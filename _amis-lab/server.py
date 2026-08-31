#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
amis 本地渲染实验室：静态服务 + 带延迟的 mock API

用法:
    python server.py            # 默认 8080 端口
    python server.py 9000       # 指定端口

提供两类能力:
    1. 静态文件: index.html / schema.json / vendor/*
    2. mock 接口: /api/**  -> 返回 amis 标准响应结构，支持 ?waitSeconds=N 延迟

终端会打印带毫秒时间戳的请求日志，用于观察接口时序（判断 loading 是否等待完成）。
"""

import json
import os
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# Windows 控制台默认可能是 GBK，打印中文会报错，强制切 UTF-8
try:
    if (sys.stdout.encoding or '').lower().replace('-', '') != 'utf8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 8080

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
}

# 模拟数据，结构与官方 mock /api/mock2/sample 保持一致
ROWS = [
    {
        'id': i,
        'engine': 'Trident - %03d' % i,
        'browser': 'Internet Explorer',
        'platform': 'Win 95+',
        'version': '4',
        'grade': 'X',
    }
    for i in range(1, 11)
]


def log(msg):
    now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print('[%s] %s' % (now, msg), flush=True)


class Handler(BaseHTTPRequestHandler):
    # 配合 Content-Length 启用长连接，避免浏览器反复重连
    protocol_version = 'HTTP/1.1'

    def log_message(self, fmt, *args):
        pass  # 使用自己的 log()，带毫秒时间戳

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_GET(self):
        self._route(b'')

    def do_POST(self):
        self._route(self._read_body())

    do_PUT = do_POST
    do_DELETE = do_POST

    def _read_body(self):
        length = int(self.headers.get('Content-Length') or 0)
        return self.rfile.read(length) if length else b''

    def _route(self, body):
        u = urlparse(self.path)
        if u.path.startswith('/api/'):
            self._mock(u, body)
        else:
            self._static(u)

    def _mock(self, u, body):
        q = parse_qs(u.query)
        raw_wait = q.get('waitSeconds', ['0'])[0]
        # fail=1 时返回 status=1，用于触发 amis 的 submitFail 分支
        fail = q.get('fail', ['0'])[0] == '1'
        try:
            wait = max(0.0, float(raw_wait))
        except ValueError:
            wait = 0.0

        log('%s %s  waitSeconds=%s fail=%d  请求到达' % (self.command, u.path, raw_wait, fail))
        if body:
            log('        body=%s' % body.decode('utf-8', 'replace')[:300])

        if wait > 0:
            time.sleep(wait)

        payload = {
            'status': 1 if fail else 0,
            'msg': 'mock failure' if fail else 'ok',
            'data': {
                'count': 171,
                'total': 171,
                'rows': ROWS,
                'items': ROWS,
            },
        }
        out = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        log('%s %s  响应 %dB (status=%d)  <<< 此刻前端 loading 应结束'
            % (self.command, u.path, len(out), payload['status']))
        self._send(200, out, 'application/json; charset=utf-8')

    def _static(self, u):
        rel = u.path.lstrip('/') or 'index.html'
        # 防目录穿越
        path = os.path.normpath(os.path.join(ROOT, rel))
        if not path.startswith(ROOT) or not os.path.isfile(path):
            self._send(404, b'404 not found', 'text/plain; charset=utf-8')
            return
        ctype = MIME.get(os.path.splitext(path)[1].lower(), 'application/octet-stream')
        with open(path, 'rb') as f:
            self._send(200, f.read(), ctype)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    log('=' * 60)
    log('amis lab 已启动 -> http://localhost:%d' % port)
    log('根目录: %s' % ROOT)
    log('改 schema.json 后刷新浏览器即可生效；Ctrl+C 停止')
    log('=' * 60)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        log('已停止')


if __name__ == '__main__':
    main()
