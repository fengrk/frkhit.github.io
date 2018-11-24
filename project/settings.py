# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging
import os
import sys

REPO_NAME = "frkhit.github.io"  # Used for FREEZER_BASE_URL
GIT_PATH = "https://github.com/frkhit/frkhit.github.io"  # Used for FREEZER_BASE_URL
DEBUG = True

# Assumes the app is located in the same directory
# where this file resides
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def parent_dir(path):
    """Return the parent of a directory."""
    return os.path.abspath(os.path.join(path, os.pardir))


def init_logger(log_file=None, logger_lever=logging.INFO):
    _default_formatter = logging.Formatter("%(asctime)s %(filename)s - %(name)s - %(levelname)s - %(message)s", None)

    root_logger = logging.getLogger()
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(_default_formatter)
    root_logger.addHandler(_console_handler)

    # file handler
    if log_file is not None:
        _file_handler = logging.FileHandler(log_file)
        _file_handler.setFormatter(_default_formatter)
        root_logger.addHandler(_file_handler)

    root_logger.setLevel(logger_lever)


PROJECT_ROOT = parent_dir(APP_DIR)
if not os.path.exists(PROJECT_ROOT):
    os.makedirs(PROJECT_ROOT)

FREEZER_DESTINATION = PROJECT_ROOT
# Since this is a repo page (not a Github user page),
# we need to set the BASE_URL to the correct url as per GH Pages' standards
FREEZER_BASE_URL = "http://localhost"
FREEZER_REMOVE_EXTRA_FILES = False  # IMPORTANT: If this is True, all app files
# will be deleted when you run the freezer
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FLATPAGES_ROOT = os.path.join(FREEZER_DESTINATION, 'blog')
FLATPAGES_EXTENSION = '.md'
init_logger()
