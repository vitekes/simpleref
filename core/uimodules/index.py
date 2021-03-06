#-*- coding: utf-8 -*-
from tornado import web
import consts


class Index(web.UIModule):
    def render(self, widargs):
        return self.render_string("{0}/index.html".format(consts.WEB_PAGE_TEMPLATE_PATH), **widargs)
