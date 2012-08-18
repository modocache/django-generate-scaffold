from types import ModuleType

from nose.tools import eq_, raises

from generate_scaffold.generators import GeneratorError
from generate_scaffold.generators.base import BaseGenerator
from test_app.models import PreExistingModel, PreExistingDatedModel


TEST_APP_NAME = 'test_app'
BASE_GENERATOR = BaseGenerator(TEST_APP_NAME)
DATED_MODEL = PreExistingDatedModel()
NON_DATED_MODEL = PreExistingModel()


def test_init():
    eq_(BASE_GENERATOR.app_name, TEST_APP_NAME)


def test_get_app_module():
    module = BASE_GENERATOR.get_app_module('models')
    eq_(module.__name__, '{}.models'.format(TEST_APP_NAME))
    eq_(type(module), ModuleType)


@raises(GeneratorError)
def test_get_app_module_raises_error():
    BASE_GENERATOR.get_app_module('spaceships')


def test_get_timestamp_field_no_field_not_named():
    eq_(BASE_GENERATOR.get_timestamp_field(NON_DATED_MODEL), None)


@raises(GeneratorError)
def test_get_timestamp_field_no_field_named():
    BASE_GENERATOR.get_timestamp_field(NON_DATED_MODEL, 'doesnt-exist')


@raises(GeneratorError)
def test_get_timestamp_field_field_named_not_timestamp():
    BASE_GENERATOR.get_timestamp_field(NON_DATED_MODEL, 'description')


def test_get_timestamp_field_not_named():
    dated_field = DATED_MODEL._meta.get_field('created_at')
    timestamp_field = BASE_GENERATOR.get_timestamp_field(DATED_MODEL)

    eq_(dated_field, timestamp_field)
    eq_(timestamp_field.__class__.__name__, 'DateTimeField')


def test_get_timestamp_field_named():
    dated_field = DATED_MODEL._meta.get_field('created_at')
    timestamp_field = \
        BASE_GENERATOR.get_timestamp_field(DATED_MODEL, 'created_at')

    eq_(dated_field, timestamp_field)
    eq_(timestamp_field.__class__.__name__, 'DateTimeField')
