import os
from collections import OrderedDict

from django.core.cache import cache
from importlib import reload


def reload_django_appcache():
    cache.app_store = OrderedDict()
    cache.app_models = OrderedDict()
    cache.app_errors = {}
    cache.handled = {}
    cache.loaded = False

    for app in cache.get_apps():
        __import__(app.__name__)
        reload(app)


def clean_pyc_in_dir(dirpath):
    for root, _, files in os.walk(dirpath):
        for f in [f for f in files if os.path.splitext(f)[-1] == ".pyc"]:
            os.remove(os.path.join(root, f))
