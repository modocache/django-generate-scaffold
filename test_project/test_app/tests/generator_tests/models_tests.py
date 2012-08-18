from nose.tools import eq_, raises

from generate_scaffold.generators import ModelsGenerator, GeneratorError
from generate_scaffold.generators.base import FIELD_ALIASES


TEST_APP_NAME = 'test_app'
MODELS_GENERATOR = ModelsGenerator(TEST_APP_NAME)


def test_get_field_key():
    for field_key, aliases in FIELD_ALIASES.items():
        [eq_(field_key, MODELS_GENERATOR.get_field_key(a))
            for a in aliases]


def test_get_field_key_found():
    eq_(MODELS_GENERATOR.get_field_key('bool'), 'booleanfield')


def test_get_field_key_not_found():
    eq_(MODELS_GENERATOR.get_field_key('doesnt-exist'), None)


@raises(GeneratorError)
def test_render_field_bad_variable_name():
    MODELS_GENERATOR.render_field('class', 'text')


@raises(GeneratorError)
def test_render_field_no_such_field():
    MODELS_GENERATOR.render_field('foo', 'doesnt-exist')


def test_render_autofield():
    target_field = u'auto = models.AutoField()\n'
    test_field = MODELS_GENERATOR.render_field('auto', 'auto')
    eq_(target_field, test_field)


def test_render_bigintegerfield():
    target_field = u'bigi = models.BigIntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('bigi', 'bigint')
    eq_(target_field, test_field)


def test_render_booleanfield():
    target_field = u'boo = models.BooleanField()\n'
    test_field = MODELS_GENERATOR.render_field('boo', 'bool')
    eq_(target_field, test_field)


def test_render_charfield():
    target_field = u'char = models.CharField(max_length=200)\n'
    test_field = MODELS_GENERATOR.render_field('char', 'string')
    eq_(target_field, test_field)


def test_render_commaseparatedintegerfield():
    target_field = u'c = models.CommaSeparatedIntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('c', 'comma')
    eq_(target_field, test_field)


def test_render_datefield():
    target_field = u'da = models.DateField()\n'
    test_field = MODELS_GENERATOR.render_field('da', 'date')
    eq_(target_field, test_field)


def test_render_datetimefield():
    target_field = u'dt = models.DateTimeField()\n'
    test_field = MODELS_GENERATOR.render_field('dt', 'datetime')
    eq_(target_field, test_field)


def test_render_decimalfield():
    target_field = \
        u'd = models.DecimalField(max_digits=10, decimal_places=5)\n'
    test_field = MODELS_GENERATOR.render_field('d', 'decimal')
    eq_(target_field, test_field)


def test_render_emailfield():
    target_field = u'emailfield = models.EmailField(max_length=254)\n'
    test_field = MODELS_GENERATOR.render_field('emailfield', 'email')
    eq_(target_field, test_field)


def test_render_filefield():
    target_field = u"__f__ = models.FileField(upload_to='uploaded_files')\n"
    test_field = MODELS_GENERATOR.render_field('__F__', 'file')
    eq_(target_field, test_field)


def test_render_filepathfield():
    target_field = u"foo = models.FilePathField(path='uploaded_files')\n"
    test_field = MODELS_GENERATOR.render_field('%&fo$o**', 'path')
    eq_(target_field, test_field)


def test_render_floatfield():
    target_field = u"this_is_a_really_long_variable_name_this_is_crazy_what_is_going_on = models.FloatField()\n"
    test_field = MODELS_GENERATOR.render_field('this_is_a_really_long_variable_name_this_is_crazy_what_is_going_on', 'float')
    eq_(target_field, test_field)


@raises(GeneratorError)
def test_render_foreignkey_without_other_model():
    MODELS_GENERATOR.render_field('owner', 'foreignkey')


def test_render_foreignkey_with_other_model():
    target_field = u"owner = models.ForeignKey('django.contrib.auth.models.User')\n"
    test_field = MODELS_GENERATOR.render_field('owner', 'foreign', 'django.contrib.auth.models.User')
    eq_(target_field, test_field)


def test_render_genericipaddressfield():
    target_field = u'ip = models.GenericIPAddressField()\n'
    test_field = MODELS_GENERATOR.render_field('ip', 'genericip')
    eq_(target_field, test_field)


def test_render_imagefield():
    target_field = u"image = models.ImageField(upload_to='uploaded_files')\n"
    test_field = MODELS_GENERATOR.render_field('image', 'image')
    eq_(target_field, test_field)


def test_render_integerfield():
    target_field = u'int = models.IntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('int', 'int')
    eq_(target_field, test_field)


def test_render_ipaddressfield():
    target_field = u'ip = models.IPAddressField()\n'
    test_field = MODELS_GENERATOR.render_field('ip', 'ip')
    eq_(target_field, test_field)


@raises(GeneratorError)
def test_render_manytomanyfield_without_other_model():
    MODELS_GENERATOR.render_field('friends', 'many')


def test_render_manytomanyfield_with_other_model():
    target_field = u"friends = models.ManyToManyField('User')\n"
    test_field = MODELS_GENERATOR.render_field('friends', 'many', 'User')
    eq_(target_field, test_field)


def test_render_nullbooleanfield():
    target_field = u'nulbol = models.NullBooleanField()\n'
    test_field = MODELS_GENERATOR.render_field('nulbol', 'nullbool')
    eq_(target_field, test_field)


@raises(GeneratorError)
def test_render_onetoonefield_without_other_model():
    MODELS_GENERATOR.render_field('case', 'one')


def test_render_onetoonefield_with_other_model():
    target_field = u"case = models.OneToOneField('Case')\n"
    test_field = MODELS_GENERATOR.render_field('case', 'onetoone', 'Case')
    eq_(target_field, test_field)


def test_render_positiveintegerfield():
    target_field = u'posint = models.PositiveIntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('posint', 'positiveint')
    eq_(target_field, test_field)


def test_render_positivesmallintegerfield():
    target_field = u'posmall = models.PositiveSmallIntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('posmall', 'positivesmallint')
    eq_(target_field, test_field)


def test_render_slugfield():
    target_field = u'slug = models.SlugField(max_length=200)\n'
    test_field = MODELS_GENERATOR.render_field('slug', 'slug')
    eq_(target_field, test_field)


def test_render_smallintegerfield():
    target_field = u'small = models.SmallIntegerField()\n'
    test_field = MODELS_GENERATOR.render_field('small', 'smallint')
    eq_(target_field, test_field)


def test_render_textfield():
    target_field = u'test = models.TextField()\n'
    test_field = MODELS_GENERATOR.render_field('test', 'text')
    eq_(target_field, test_field)


def test_render_timefield():
    target_field = u'time = models.TimeField()\n'
    test_field = MODELS_GENERATOR.render_field('time', 'time')
    eq_(target_field, test_field)


def test_render_urlfield():
    target_field = u'url = models.URLField()\n'
    test_field = MODELS_GENERATOR.render_field('url', 'url')
    eq_(target_field, test_field)


@raises(GeneratorError)
def test_render_model_already_exists():
    MODELS_GENERATOR.render_model('PreExistingModel', [['foo', 'text']])


@raises(GeneratorError)
def test_render_model_already_exists_with_capitalization():
    MODELS_GENERATOR.render_model('preExistingModel', [['foo', 'text']])


@raises(GeneratorError)
def test_render_model_bad_field_args():
    MODELS_GENERATOR.render_model('BrandNewModel', ['doo', 'boop', 'bebop'])


def test_render_model_without_timestamps():
    test_model = MODELS_GENERATOR.render_model(
        'BrandNewModel', [['foo', 'text'],], add_timestamp=False)
    target_model = (u"""
class BrandNewModel(models.Model):
    foo = models.TextField()


    @models.permalink
    def get_absolute_url(self):
        return ('test_app_brandnewmodel_detail', (), {'pk': self.pk})
""", 'BrandNewModel')

    eq_(test_model, target_model)


# TODO - Should this raise an error?
# @raises(GeneratorError)
# def test_render_model_without_timestamps_or_fields():
#     MODELS_GENERATOR.render_model('BrandNewModel', [], add_timestamp=False)


def test_render_model_with_models_with_now():
    models_generator = ModelsGenerator('test_modelgen_with_models_with_now')
    fields = [['foo', 'text'],]
    test_model = models_generator.render_model('BrandNewModel', fields)
    target_model = (u"""
class BrandNewModel(models.Model):
    foo = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=now(),
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        default=now(),
        editable=False,
    )

    @models.permalink
    def get_absolute_url(self):
        return ('test_modelgen_with_models_with_now_brandnewmodel_detail', (), {'pk': self.pk})
""", 'BrandNewModel')

    eq_(test_model, target_model)


def test_render_model_with_models_without_now():
    models_generator = ModelsGenerator('test_modelgen_with_models_without_now')
    fields = [['foo', 'text'], ['bar', 'date'], ['biz', 'foreign', 'Blog']]
    test_model = models_generator.render_model('somemodel', fields)
    target_model = (u"""
from django.utils.timezone import now
class Somemodel(models.Model):
    foo = models.TextField()
    bar = models.DateField()
    biz = models.ForeignKey('Blog')
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=now(),
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        default=now(),
        editable=False,
    )

    @models.permalink
    def get_absolute_url(self):
        return ('test_modelgen_with_models_without_now_somemodel_detail', (), {'pk': self.pk})
""", 'Somemodel')

    eq_(test_model, target_model)


def test_render_model_without_models_with_now():
    models_generator = ModelsGenerator('test_modelgen_without_models_with_now')
    fields = []
    test_model = models_generator.render_model('a', fields)
    target_model = (u"""
from django.db import models
class A(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=now(),
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        default=now(),
        editable=False,
    )

    @models.permalink
    def get_absolute_url(self):
        return ('test_modelgen_without_models_with_now_a_detail', (), {'pk': self.pk})
""", 'A')

    eq_(test_model, target_model)


def test_render_model_without_models_without_now():
    models_generator = ModelsGenerator('test_modelgen_without_models_without_now')
    fields = [['a', 'bigint'],]
    test_model = models_generator.render_model('THISISALLCAPS', fields)
    target_model = (u"""
from django.db import models
from django.utils.timezone import now
class THISISALLCAPS(models.Model):
    a = models.BigIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=now(),
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        default=now(),
        editable=False,
    )

    @models.permalink
    def get_absolute_url(self):
        return ('test_modelgen_without_models_without_now_thisisallcaps_detail', (), {'pk': self.pk})
""", 'THISISALLCAPS')

    eq_(test_model, target_model)
