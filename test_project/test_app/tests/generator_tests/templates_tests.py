import os

from nose.tools import eq_

from generate_scaffold.generators import TemplatesGenerator
from test_app.models import PreExistingModel, PreExistingDatedModel


TEST_APP_NAME = 'test_app'
TEST_APP_DIR = __import__(TEST_APP_NAME).__path__[0]
TEST_APP_TPL_DIR = os.path.join(TEST_APP_DIR, 'templates', TEST_APP_NAME)
TEMPLATES_GENERATOR = TemplatesGenerator(TEST_APP_NAME)
TEST_MODEL = PreExistingModel()
TEST_MODEL_TPL_DIR = os.path.join(TEST_APP_TPL_DIR, 'preexistingmodel')
TEST_TIMESTAMPED_MODEL = PreExistingDatedModel()
TEST_TIMESTAMPED_MODEL_TPL_DIR = os.path.join(
    TEST_APP_TPL_DIR, 'preexistingdatedmodel')


def test_get_model_fields():
    fields = TEMPLATES_GENERATOR.get_model_fields(TEST_MODEL)
    target_fields = ['description']
    eq_(fields, target_fields)

    fields = TEMPLATES_GENERATOR.get_model_fields(TEST_TIMESTAMPED_MODEL)
    target_fields = ['created_at']
    eq_(fields, target_fields)


def test_render_templates_no_timestamp():
    template_tuples = list(TEMPLATES_GENERATOR.render_templates(
        TEST_MODEL, TEST_MODEL_TPL_DIR))

    filenames = sorted([os.path.basename(path)
        for path, tpl in template_tuples])
    target_filenames = sorted([
        'base.html',
        'preexistingmodel_confirm_delete.html',
        'preexistingmodel_detail.html',
        'preexistingmodel_form.html',
        'preexistingmodel_list.html',
        'object_table_detail.html',
        'object_table_list.html',
        'pagination.html'
    ])
    eq_(filenames, target_filenames)


def test_render_templates_with_timestamp():
    template_tuples = list(TEMPLATES_GENERATOR.render_templates(
        TEST_TIMESTAMPED_MODEL, TEST_TIMESTAMPED_MODEL_TPL_DIR))

    filenames = sorted([os.path.basename(path)
        for path, tpl in template_tuples])
    target_filenames = sorted([
        'base.html',
        'preexistingdatedmodel_archive.html',
        'preexistingdatedmodel_archive_day.html',
        'preexistingdatedmodel_archive_month.html',
        'preexistingdatedmodel_archive_week.html',
        'preexistingdatedmodel_archive_year.html',
        'preexistingdatedmodel_confirm_delete.html',
        'preexistingdatedmodel_detail.html',
        'preexistingdatedmodel_form.html',
        'preexistingdatedmodel_list.html',
        'object_table_detail.html',
        'object_table_list.html',
        'pagination.html'
    ])
    eq_(filenames, target_filenames)
