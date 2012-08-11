from nose.tools import eq_, raises

from generate_scaffold.generators import ViewsGenerator, GeneratorError
from test_app.models import PreExistingModel, PreExistingDatedModel


TEST_APP_NAME = 'test_app'
VIEWS_GENERATOR = ViewsGenerator(TEST_APP_NAME)
TEST_MODEL = PreExistingModel()
TEST_TIMESTAMPED_MODEL = PreExistingDatedModel()


def test_render_views_no_timestamp():
    view = VIEWS_GENERATOR.render_views(TEST_MODEL)
    target_view = \
    '''from django.views.generic import ListView, DetailView, CreateView, \\
                                 DeleteView, UpdateView


from test_app.models import PreExistingModel


class PreExistingModelView(object):
    model = PreExistingModel

    def get_template_names(self):
        """Nest templates within preexistingmodel directory."""
        tpl = super(PreExistingModelView, self).get_template_names()[0]
        app = self.model._meta.app_label
        mdl = \'preexistingmodel\'
        self.template_name = tpl.replace(app, \'{0}/{1}\'.format(app, mdl))
        return [self.template_name]


class PreExistingModelBaseListView(PreExistingModelView):
    paginate_by = 10



class PreExistingModelCreateView(PreExistingModelView, CreateView):
    pass




class PreExistingModelDeleteView(PreExistingModelView, DeleteView):

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse(\'test_app_preexistingmodel_list\')


class PreExistingModelDetailView(PreExistingModelView, DetailView):
    pass


class PreExistingModelListView(PreExistingModelBaseListView, ListView):
    pass




class PreExistingModelUpdateView(PreExistingModelView, UpdateView):
    pass





'''
    eq_(view, target_view)


@raises(GeneratorError)
def test_render_views_invalid_timestamp_field():
    VIEWS_GENERATOR.render_views(TEST_MODEL, 'created_at')


def test_render_timestamped_views_no_timestamp():
    view = VIEWS_GENERATOR.render_views(TEST_TIMESTAMPED_MODEL)
    target_view = \
    '''from django.views.generic import ListView, DetailView, CreateView, \\
                                 DeleteView, UpdateView, \\
                                 ArchiveIndexView, DateDetailView, \\
                                 DayArchiveView, MonthArchiveView, \\
                                 TodayArchiveView, WeekArchiveView, \\
                                 YearArchiveView


from test_app.models import PreExistingDatedModel


class PreExistingDatedModelView(object):
    model = PreExistingDatedModel

    def get_template_names(self):
        """Nest templates within preexistingdatedmodel directory."""
        tpl = super(PreExistingDatedModelView, self).get_template_names()[0]
        app = self.model._meta.app_label
        mdl = 'preexistingdatedmodel'
        self.template_name = tpl.replace(app, '{0}/{1}'.format(app, mdl))
        return [self.template_name]


class PreExistingDatedModelDateView(PreExistingDatedModelView):
    date_field = 'created_at'
    month_format = '%m'


class PreExistingDatedModelBaseListView(PreExistingDatedModelView):
    paginate_by = 10


class PreExistingDatedModelArchiveIndexView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, ArchiveIndexView):
    pass


class PreExistingDatedModelCreateView(PreExistingDatedModelView, CreateView):
    pass


class PreExistingDatedModelDateDetailView(PreExistingDatedModelDateView, DateDetailView):
    pass


class PreExistingDatedModelDayArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, DayArchiveView):
    pass


class PreExistingDatedModelDeleteView(PreExistingDatedModelView, DeleteView):

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('test_app_preexistingdatedmodel_list')


class PreExistingDatedModelDetailView(PreExistingDatedModelView, DetailView):
    pass


class PreExistingDatedModelListView(PreExistingDatedModelBaseListView, ListView):
    pass


class PreExistingDatedModelMonthArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, MonthArchiveView):
    pass


class PreExistingDatedModelTodayArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, TodayArchiveView):
    pass


class PreExistingDatedModelUpdateView(PreExistingDatedModelView, UpdateView):
    pass


class PreExistingDatedModelWeekArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, WeekArchiveView):
    pass


class PreExistingDatedModelYearArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, YearArchiveView):
    make_object_list = True



'''
    eq_(view, target_view)


def test_render_timestamped_views_with_timestamp():
    view = VIEWS_GENERATOR.render_views(TEST_TIMESTAMPED_MODEL, 'created_at')
    target_view = \
    '''from django.views.generic import ListView, DetailView, CreateView, \\
                                 DeleteView, UpdateView, \\
                                 ArchiveIndexView, DateDetailView, \\
                                 DayArchiveView, MonthArchiveView, \\
                                 TodayArchiveView, WeekArchiveView, \\
                                 YearArchiveView


from test_app.models import PreExistingDatedModel


class PreExistingDatedModelView(object):
    model = PreExistingDatedModel

    def get_template_names(self):
        """Nest templates within preexistingdatedmodel directory."""
        tpl = super(PreExistingDatedModelView, self).get_template_names()[0]
        app = self.model._meta.app_label
        mdl = 'preexistingdatedmodel'
        self.template_name = tpl.replace(app, '{0}/{1}'.format(app, mdl))
        return [self.template_name]


class PreExistingDatedModelDateView(PreExistingDatedModelView):
    date_field = 'created_at'
    month_format = '%m'


class PreExistingDatedModelBaseListView(PreExistingDatedModelView):
    paginate_by = 10


class PreExistingDatedModelArchiveIndexView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, ArchiveIndexView):
    pass


class PreExistingDatedModelCreateView(PreExistingDatedModelView, CreateView):
    pass


class PreExistingDatedModelDateDetailView(PreExistingDatedModelDateView, DateDetailView):
    pass


class PreExistingDatedModelDayArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, DayArchiveView):
    pass


class PreExistingDatedModelDeleteView(PreExistingDatedModelView, DeleteView):

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('test_app_preexistingdatedmodel_list')


class PreExistingDatedModelDetailView(PreExistingDatedModelView, DetailView):
    pass


class PreExistingDatedModelListView(PreExistingDatedModelBaseListView, ListView):
    pass


class PreExistingDatedModelMonthArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, MonthArchiveView):
    pass


class PreExistingDatedModelTodayArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, TodayArchiveView):
    pass


class PreExistingDatedModelUpdateView(PreExistingDatedModelView, UpdateView):
    pass


class PreExistingDatedModelWeekArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, WeekArchiveView):
    pass


class PreExistingDatedModelYearArchiveView(
    PreExistingDatedModelDateView, PreExistingDatedModelBaseListView, YearArchiveView):
    make_object_list = True



'''
    eq_(view, target_view)
