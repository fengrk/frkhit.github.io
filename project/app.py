# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
import operator
import os
import re
from itertools import takewhile

from flask import Flask
from flask_flatpages import FlatPages
from flask_flatpages.page import Page as OldPage, cached_property, yaml
from flask_frozen import Freezer
from werkzeug.utils import import_string


class Page(OldPage):
    def __init__(self, path, meta, body, html_renderer):
        """

        :type body: str
        :type meta: str
        :type path: str
        """
        super(Page, self).__init__(path, meta, body, html_renderer)
        
        # date re
        self.date_re = re.compile(r"[\d]{4}/[\d]{2}/[\d]{2}(?=/)")
        
        # 执行meta方法
        if self.meta:
            pass
    
    @cached_property
    def html(self):
        """The content of the page, rendered as HTML by the configured
        renderer.
        """
        return self.html_renderer(self)
    
    @cached_property
    def meta(self):
        """A dict of metadata parsed as YAML from the header of the file.
        """
        meta = yaml.safe_load(self._meta)
        # YAML documents can be any type but we want a dict
        # eg. yaml.safe_load('') -> None
        #     yaml.safe_load('- 1\n- a') -> [1, 'a']
        if not meta:
            if self._meta:
                # 还原body
                self.body = "\n".join((self._meta, self.body))
            
            meta = {}
        
        if not isinstance(meta, dict):
            raise ValueError("Excpected a dict in metadata for '{0}', got {1}".
                             format(self.path, type(meta).__name__))
        
        # title
        if "title" not in meta:
            _title = None
            if self._meta:
                _title = self._meta.replace("#", "").strip()
            
            if _title is None:
                _title = os.path.basename(self.path)
            
            meta["title"] = _title or "日志"
        
        # date
        if "date" not in meta:
            meta["date"] = self._get_date_from_path(self.path) or datetime.date.today()
        
        return meta
    
    def _get_date_from_path(self, path):
        """
            文件命名: /2018/01/31/xxx.md
        :rtype: datetime.date
        """
        result = self.date_re.findall(path)
        if result:
            return datetime.datetime.strptime(result[0], "%Y/%m/%d").date()
        return None


def _parse(self, content, path):
    """Parse a flatpage file, i.e. read and parse its meta data and body.

    :return: initialized :class:`Page` instance.
    """
    lines = iter(content.split('\n'))
    
    # Read lines until an empty line is encountered.
    meta = '\n'.join(takewhile(operator.methodcaller('strip'), lines))
    # The rest is the content. `lines` is an iterator so it continues
    # where `itertools.takewhile` left it.
    content = '\n'.join(lines)
    
    # Now we ready to get HTML renderer function
    html_renderer = self.config('html_renderer')
    
    # If function is not callable yet, import it
    if not callable(html_renderer):
        html_renderer = import_string(html_renderer)
    
    # Make able to pass custom arguments to renderer function
    html_renderer = self._smart_html_renderer(html_renderer)
    
    # Initialize and return Page instance
    return Page(path, meta, content, html_renderer)


FlatPages._parse = _parse

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)
