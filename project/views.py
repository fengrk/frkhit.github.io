# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template

from app import app, pages
from settings import GIT_PATH


@app.route('/')
def home():
    posts = [_page for _page in pages if 'date' in _page.meta]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True, key=lambda _page: _page.meta['date'])
    return render_template('index.html', pages=sorted_posts, git_path=GIT_PATH)


@app.route('/<path:path>/')
def page(path):
    # Path is the filename of a page, without the file extension
    # e.g. "first-post"
    _page = pages.get_or_404(path)
    return render_template('page.html', page=_page, git_path=GIT_PATH)
