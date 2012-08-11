from nose.tools import ok_, eq_, raises

from generate_scaffold.generators import UrlsGenerator, GeneratorError
from test_app.models import PreExistingModel, PreExistingDatedModel
from test_urlgen_with_urlpatterns.models import URLPreExistingDatedModel


TEST_APP_NAME = 'test_app'
URLS_GENERATOR = UrlsGenerator(TEST_APP_NAME)
DATED_MODEL = PreExistingDatedModel()
NON_DATED_MODEL = PreExistingModel()


@raises(GeneratorError)
def test_render_urls_no_module():
    urls_generator = UrlsGenerator('test_urlgen_without_urls')
    urls_generator.render_urls(NON_DATED_MODEL)


def test_render_urls_with_timestamp():
    test_urlpattern = URLS_GENERATOR.render_urls(DATED_MODEL)
    target_urlpattern = u"""

from test_app.views.preexistingdatedmodel_views import *
urlpatterns = patterns('',
    url(
        regex=r'^preexistingdatedmodel/archive/$',
        view=PreExistingDatedModelArchiveIndexView.as_view(),
        name='test_app_preexistingdatedmodel_archive_index'
    ),
    url(
        regex=r'^preexistingdatedmodel/create/$',
        view=PreExistingDatedModelCreateView.as_view(),
        name='test_app_preexistingdatedmodel_create'
    ),
    url(
        regex=r'^preexistingdatedmodel/(?P<year>\\d{4})/'
               '(?P<month>\\d{1,2})/'
               '(?P<day>\\d{1,2})/'
               '(?P<pk>\\d+?)/$',
        view=PreExistingDatedModelDateDetailView.as_view(),
        name='test_app_preexistingdatedmodel_date_detail'
    ),
    url(
        regex=r'^preexistingdatedmodel/archive/(?P<year>\\d{4})/'
               '(?P<month>\\d{1,2})/'
               '(?P<day>\\d{1,2})/$',
        view=PreExistingDatedModelDayArchiveView.as_view(),
        name='test_app_preexistingdatedmodel_day_archive'
    ),
    url(
        regex=r'^preexistingdatedmodel/(?P<pk>\\d+?)/delete/$',
        view=PreExistingDatedModelDeleteView.as_view(),
        name='test_app_preexistingdatedmodel_delete'
    ),
    url(
        regex=r'^preexistingdatedmodel/(?P<pk>\\d+?)/$',
        view=PreExistingDatedModelDetailView.as_view(),
        name='test_app_preexistingdatedmodel_detail'
    ),
    url(
        regex=r'^preexistingdatedmodel/$',
        view=PreExistingDatedModelListView.as_view(),
        name='test_app_preexistingdatedmodel_list'
    ),
    url(
        regex=r'^preexistingdatedmodel/archive/(?P<year>\\d{4})/'
               '(?P<month>\\d{1,2})/$',
        view=PreExistingDatedModelMonthArchiveView.as_view(),
        name='test_app_preexistingdatedmodel_month_archive'
    ),
    url(
        regex=r'^preexistingdatedmodel/today/$',
        view=PreExistingDatedModelTodayArchiveView.as_view(),
        name='test_app_preexistingdatedmodel_today_archive'
    ),
    url(
        regex=r'^preexistingdatedmodel/(?P<pk>\\d+?)/update/$',
        view=PreExistingDatedModelUpdateView.as_view(),
        name='test_app_preexistingdatedmodel_update'
    ),
    url(
        regex=r'^preexistingdatedmodel/archive/(?P<year>\\d{4})/'
               '(?P<month>\\d{1,2})/'
               'week/(?P<week>\\d{1,2})/$',
        view=PreExistingDatedModelWeekArchiveView.as_view(),
        name='test_app_preexistingdatedmodel_week_archive'
    ),
    url(
        regex=r'^preexistingdatedmodel/archive/(?P<year>\\d{4})/$',
        view=PreExistingDatedModelYearArchiveView.as_view(),
        name='test_app_preexistingdatedmodel_year_archive'
    ),
)
"""
    eq_(test_urlpattern, target_urlpattern)


# FIXME - Use regex to test. Whitespace in between urlpattern
#         definitions, for example, should not be tested.
def test_render_urls_without_timestamp():
    test_urlpattern = URLS_GENERATOR.render_urls(NON_DATED_MODEL)
    target_urlpattern = u"""

from test_app.views.preexistingmodel_views import *
urlpatterns = patterns('',

    url(
        regex=r'^preexistingmodel/create/$',
        view=PreExistingModelCreateView.as_view(),
        name='test_app_preexistingmodel_create'
    ),


    url(
        regex=r'^preexistingmodel/(?P<pk>\\d+?)/delete/$',
        view=PreExistingModelDeleteView.as_view(),
        name='test_app_preexistingmodel_delete'
    ),
    url(
        regex=r'^preexistingmodel/(?P<pk>\\d+?)/$',
        view=PreExistingModelDetailView.as_view(),
        name='test_app_preexistingmodel_detail'
    ),
    url(
        regex=r'^preexistingmodel/$',
        view=PreExistingModelListView.as_view(),
        name='test_app_preexistingmodel_list'
    ),


    url(
        regex=r'^preexistingmodel/(?P<pk>\\d+?)/update/$',
        view=PreExistingModelUpdateView.as_view(),
        name='test_app_preexistingmodel_update'
    ),


)
"""
    eq_(test_urlpattern, target_urlpattern)


def test_render_urls_with_urlpattern():
    model = URLPreExistingDatedModel()
    test_urlpattern = UrlsGenerator(
        'test_urlgen_with_urlpatterns').render_urls(model)
    target_match = "urlpatterns += patterns"

    ok_(target_match in test_urlpattern)
