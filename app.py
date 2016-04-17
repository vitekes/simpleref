#-*- coding: utf-8 -*-
import os
import sys
import signal
import argparse
from tornado import ioloop, web, gen, escape
from daemon import Daemon
import consts
from core.db import db_funcs
from core.uimodules import template
from core.uimodules import category
from core.uimodules import post
from core.uimodules import index


#############################################################################
is_closing = False
work_dir = os.getcwd()
templates = {'errors': {}}


def sigHandler(signum, frame):
    global is_closing
    print '\nexiting...'
    is_closing = True
# signal_handler

#############################################################################


def try_exit():
    """
    try_exit should close all unfinished ...
    """
    global is_closing
    if is_closing:
        ioloop.IOLoop.instance().stop()
        print 'exit success'
# try_exit
#############################################################################


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


#############################################################################
class IndexHandler(BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        webargs = {
            'user_module': 'Index',
            'title': 'Рефераты это просто! Все рефераты здесь',
            'page_args': {
            }
        }
        self.render(template_name="./web/template.html", **webargs)
#############################################################################


class CategoryHandler(BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self, category_inner_id, page=0):
        category_url = '{0}{1}'.format(consts.CATEGORY_PARTIAL_URL, category_inner_id)
        category_id, category_name, total_count = db_funcs.get_category_by_url(category_url)
        entries = db_funcs.get_articles_from_db(category_id, page)
        last_page = total_count // 20
        if last_page == 0:
            last_page = 1

        webargs = {
            'user_module': 'Category',
            'title': 'Категория {0} страница {1}. Рефераты это просто!'.format(
                       'category_name',
                       page
                   ),
            'page_args': {
                'entries': entries,
                'page':page,
                'last': last_page
            }
        }
        self.render(template_name="./web/template.html", **webargs)
#############################################################################


class PostHandler(BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self, referat_id):
        ref_list = db_funcs.get_referat_by(referat_id)
        webargs = {'title': 'TWR', 'posts': ref_list}
        self.render(template_name="./web/index.html", **webargs)
#############################################################################


settings = {
    "cookie_secret": "61oETzKXQOGaYdkL5gEmGeJJFuYh7EQnp2CdTP1o/Vo=",
    "ui_modules": [template, category, post, index],
    "login_url": "./web/templates/base.html",
    "debug": True,
}


application = web.Application([
    (r"/category/([0-9]+)", CategoryHandler),
    (r"/referat/([0-9]+)", PostHandler),
    (r"/", IndexHandler),
    (r"/img/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/img".format(wdir=work_dir)}),
    (r"/js/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/js".format(wdir=work_dir)}),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/css".format(wdir=work_dir)}),
    (r"/fonts/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/fonts".format(wdir=work_dir)}),
    (r"/category/img/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/img".format(wdir=work_dir)}),
    (r"/category/js/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/js".format(wdir=work_dir)}),
    (r"/category/css/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/css".format(wdir=work_dir)}),
    (r"/category/fonts/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/fonts".format(wdir=work_dir)}),
    (r"/referat/img/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/img".format(wdir=work_dir)}),
    (r"/referat/js/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/js".format(wdir=work_dir)}),
    (r"/referat/css/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/css".format(wdir=work_dir)}),
    (r"/referat/fonts/(.*)", web.StaticFileHandler, {"path": "{wdir}/web/fontss".format(wdir=work_dir)}),
    (r"/(.*\.ico)",  web.StaticFileHandler, {"path": "{wdir}/web/app".format(wdir=work_dir)}),
], **settings)


def run_app(arguments):
    def set_exit_handler(func):
        signal.signal(signal.SIGTERM, func)

    def daemon_exit(sig, func):
        set_exit_handler(signal.SIG_DFL)
        exit(0)

    set_exit_handler(daemon_exit)

    port = 8888
    address = "127.0.0.1"
    pid_file = arguments.pid_file
    daemonizator = Daemonizator(port, address, pid_file)
    if not arguments.debug:
        daemonizator.start()
    else:
        daemonizator.run()


def daemon_main(port, address):
    application.listen(port, address)

    ioloop.PeriodicCallback(try_exit, 100).start()
    ioloop.IOLoop.instance().start()


class Daemonizator(Daemon):
    def __init__(self, port, address, pid_file):
        self.port = port
        self.address = address
        self.pid_file = os.path.realpath(pid_file)
        Daemon.__init__(self, pidfile=self.pid_file)

    def run(self):
        daemon_main(self.port, self.address)


if __name__ == "__main__":

    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pid-file", type=str, help="pid-file of daemonized app", default="/tmp/game.pid")
    parser.add_argument("-d", "--debug", help="do not daemonize, run in console", action='store_true', default=False)
    parser.add_argument("--stop", help="stop daemon")
    parser.add_argument("--restart", help="restart daemon")
    arguments = parser.parse_args()

    # load templates
    with open('{wdir}/web/404.html'.format(wdir=work_dir), 'rb') as _f:
        templates['errors']["404"] = _f.read()

    run_app(arguments)