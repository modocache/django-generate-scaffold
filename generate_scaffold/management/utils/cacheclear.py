import os

from django.db.models.loading import AppCache
from django.utils.datastructures import SortedDict


def reload_django_appcache():
    cache = AppCache()

    cache.app_store = SortedDict()
    cache.app_models = SortedDict()
    cache.app_errors = {}
    cache.handled = {}
    cache.loaded = False

    for app in cache.get_apps():
        __import__(app.__name__)
        reload(app)


def clean_pyc_in_dir(dirpath):
    for root, _, files in os.walk(dirpath):
        for f in [f for f in files if os.path.splitext(f)[-1] == '.pyc']:
            os.remove(os.path.join(root, f))

