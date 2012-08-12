#!/usr/bin/env python


import os
import sys
import subprocess


def runtests():
    """Use generatescaffold to generate a model, then run the test
    suite, before finally cleaning up after generatescaffold. Exits
    with the status code of ./manage.py test."""

    app_abspath = os.path.dirname(os.path.dirname(__file__))
    models_abspath = os.path.join(app_abspath, 'models.py')
    models_exists = os.path.isfile(models_abspath)
    urls_abspath = os.path.join(app_abspath, 'urls.py')
    urls_exists = os.path.isfile(urls_abspath)
    views_abspath = os.path.join(app_abspath, 'views')
    views_exists = os.path.isdir(views_abspath)
    tpls_abspath = os.path.join(app_abspath, 'templates')
    tpls_exists = os.path.isdir(tpls_abspath)

    for f in [models_abspath, urls_abspath]:
        if os.path.isfile(f):
            subprocess.call('cp {} {}.orig'.format(f, f), shell=True)

    if views_exists:
        subprocess.call('cp -r {} {}.orig'.format(views_abspath, views_abspath), shell=True)

    if tpls_exists:
        subprocess.call('cp -r {} {}.orig'.format(tpls_abspath, tpls_abspath), shell=True)

    subprocess.call('python manage.py generatescaffold test_app GeneratedModel title:string description:text', shell=True)
    test_status = subprocess.call('python manage.py test --with-selenium --with-cherrypyliveserver --noinput', shell=True)

    if models_exists:
        subprocess.call('mv {}.orig {}'.format(models_abspath, models_abspath), shell=True)
    else:
        subprocess.call('rm {}'.format(models_abspath), shell=True)

    if urls_exists:
        subprocess.call('mv {}.orig {}'.format(urls_abspath, urls_abspath), shell=True)
    else:
        subprocess.call('rm {}'.format(urls_abspath), shell=True)

    if views_exists:
        subprocess.call('rm -rf {}'.format(views_abspath), shell=True)
        subprocess.call('mv {}.orig {}'.format(views_abspath, views_abspath), shell=True)
    else:
        subprocess.call('rm -rf {}'.format(views_abspath), shell=True)

    if tpls_exists:
        subprocess.call('rm -rf {}'.format(tpls_abspath), shell=True)
        subprocess.call('mv {}.orig {}'.format(tpls_abspath, tpls_abspath), shell=True)
    else:
        subprocess.call('rm -rf {}'.format(tpls_abspath), shell=True)

    subprocess.call('rm {}/*.pyc'.format(app_abspath), shell=True)

    sys.exit(test_status)


if __name__ == '__main__':
    runtests()