import inspect
import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.management.transactions import FilesystemTransaction
from generate_scaffold.management.utils.cacheclear import clean_pyc_in_dir, \
                                                          reload_django_appcache
from generate_scaffold.management.utils.directories import get_templates_in_dir
from generate_scaffold.management.utils.modules import import_child
from generate_scaffold.management.utils.strings import dumb_capitalized, \
                                                       get_valid_variable
from generate_scaffold.management.verbosity import VerboseCommandMixin


class Command(VerboseCommandMixin, BaseCommand):
    command_name = os.path.split(__file__)[-1].split('.')[0]
    help = (
        'Rails-like view/template generator.\n\n'
        'manage.py {cmd_name} <app_name> [options] <model_name> '
        '[field_name:field_type ...]\n\n'
        'For example, to generate a scaffold for a model named "Post" '
        'in an app named "blogs",\nyou can issue the following command:\n\n'
        'manage.py {cmd_name} blogs Post title:char body:text '
        'blog:foreignkey=Blog'.format(cmd_name=command_name)
    )
    option_list = BaseCommand.option_list + (
        make_option('-d', '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Do not actually do anything, but print what '
                 'would have happened to the console.'
        ),
        make_option('-t', '--no-timestamps',
            action='store_false',
            dest='is_timestamped_model',
            default=True,
            help='Create models with created_at and updated_at '
                 'DateTimeFields.'
        ),
        make_option('--naive-time',
            action='store_true',
            dest='is_naive_time',
            default=False,
            help='Use Python datetime in place of Django timezone-'
                 'aware datetimes.'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.verbose = False
        self.dry_run = False
        self.field_aliases = {
            'autofield': ['auto', 'autofield'],
            'bigintegerfield': ['bigint', 'biginteger', 'bigintfield', 'bigintegerfield'],
            'booleanfield': ['bool', 'boolean', 'booleanfield'],
            'charfield': ['string', 'char', 'charfield'],
            'commaseparatedintegerfield': ['comma', 'commaseparatedint', 'commaseparatedinteger', 'commaseparatedintegerfield'],
            'datefield': ['date', 'datefield'],
            'datetimefield': ['datetime', 'datetimefield'],
            'decimalfield': ['decimal', 'decimalfield'],
            'emailfield': ['email', 'emailfield'],
            'filefield': ['file', 'filefield'],
            'filepathfield': ['path', 'filepath', 'filepathfield'],
            'floatfield': ['float', 'floatfield'],
            'foreignkey': ['foreign', 'foreignkey', 'foreignkeyfield'],
            'genericipaddressfield': ['genericip', 'genericipaddress', 'genericipaddressfield'],
            'imagefield': ['image', 'imagefield'],
            'integerfield': ['int', 'integer', 'integerfield'],
            'ipaddressfield': ['ip', 'ipaddress', 'ipaddressfield'],
            'manytomanyfield': ['many', 'manytomany', 'manytomanyfield'],
            'nullbooleanfield': ['nullbool', 'nullboolean', 'nullbooleanfield'],
            'onetoonefield': ['one', 'onetoone', 'onetoonefield'],
            'positiveintegerfield': ['posint', 'positiveint', 'positiveinteger', 'positiveintegerfield'],
            'slugfield': ['slug', 'slugfield'],
            'smallintegerfield': ['smallint', 'smallinteger', 'smallintegerfield'],
            'textfield': ['text', 'textfield'],
            'timefield': ['time', 'timefield'],
            'urlfield': ['url', 'urlfield'],
        }

    def _get_rendered_model_field(self, field_name, field_type):
        # Only use lower case for field names
        original_field_name = field_name
        field_name = get_valid_variable(field_name).lower()
        if not field_name:
            raise CommandError(
                '{0} is not a valid field name. '
                'Please choose a different name.'.format(original_field_name)
            )

        other_model = None
        relationship_fields = \
            set(['foreignkey', 'manytomanyfield', 'onetoonefield'])

        if '=' in field_type:
            field_type, other_model = field_type.split('=')

        for field_key, aliases in self.field_aliases.items():

            if field_type in aliases:
                tpl_name = \
                    'generate_scaffold/models/fields/{0}.txt'.format(
                        field_key
                    )
                tpl = get_template(tpl_name)
                c = {'field_name': field_name}

                if other_model:
                    c['other_model'] = other_model
                elif field_key in relationship_fields:
                    raise CommandError(
                        '{fk} requires a related model to be specified.\n'
                        'Example: {fn}:{fk}=OtherModel'.format(
                            fk=field_key, fn=field_name
                        )
                    )

                context = Context(c)
                return tpl.render(context)

        raise CommandError(
            'Could not process {0} field type: {1}'.format(
                field_name, field_type)
        )

    def _get_rendered_model(
        self, app_name, app_models_module, model_name, model_field_args):

        rendered_fields = []
        for model_field_arg in model_field_args:
            field_name, field_type = model_field_arg.split(':')
            rendered_field = \
                self._get_rendered_model_field(field_name, field_type)
            rendered_fields.append(rendered_field)

        app_models_modules = inspect.getmembers(
            app_models_module, inspect.ismodule)

        if not [m for m in app_models_modules
          if m[0] == 'models' and m[-1].__name__ == 'django.db.models']:
            raise CommandError(
                'Sorry, {0} requires the `django.db.models` '
                'module be imported in your models.py file.\n'
                'Please add the following statement to your '
                'models.py file and try again:\n'
                'from django.db import models'.format(self.command_name)
            )

        app_models_functions = inspect.getmembers(
            app_models_module, inspect.isfunction)

        import_now = self.is_timestamped
        if [f for f in app_models_functions
          if f[0] == 'now' and f[-1].__module__ == 'django.utils.timezone']:
            self.log('from django.utils.timezone import now detected')
            import_now = False

        model_template = get_template('generate_scaffold/models/models.txt')
        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)
        c = {
            'import_now': import_now,
            'app_name': app_name,
            'model_slug': model_slug,
            'class_name': class_name,
            'fields': rendered_fields,
            'is_timestamped_model': self.is_timestamped,
        }
        return model_template.render(Context(c))

    def _get_rendered_views(self, app_name, model_name):
        views_class_templates = \
            get_templates_in_dir('generate_scaffold/views/views')

        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        rendered_views_classes = []
        for view_class_template in views_class_templates:

            t = get_template(view_class_template)
            c = {
                'app_name': app_name,
                'model_slug': model_slug,
                'class_name': class_name,
                'is_timestamped': self.is_timestamped,
            }
            rendered_views_classes.append(t.render(Context(c)))

        views_template = get_template('generate_scaffold/views/views.txt')
        views_context = {
            'app_name': app_name,
            'class_name': class_name,
            'model_slug': model_slug,
            'views': rendered_views_classes,
            'is_timestamped': self.is_timestamped,
        }
        return views_template.render(Context(views_context))

    def _get_rendered_urls(self, app_name, model_name, is_urlpatterns_available):
        url_pattern_templates = \
            get_templates_in_dir('generate_scaffold/urls/urls')
        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        rendered_url_patterns = []
        for url_pattern_template in url_pattern_templates:
            t = get_template(url_pattern_template)
            c = {
                'app_name': app_name,
                'model_slug': model_slug,
                'class_name': class_name,
                'is_timestamped': self.is_timestamped,
            }
            rendered_url_patterns.append(t.render(Context(c)))

        url_patterns_operator = '+=' if is_urlpatterns_available else '='
        urls_template = get_template('generate_scaffold/urls/urls.txt')
        c = {
            'app_name': app_name,
            'model_slug': model_slug,
            'url_patterns_operator': url_patterns_operator,
            'urls': rendered_url_patterns,
        }
        return urls_template.render(Context(c))

    def _get_rendered_templates(
            self, app_name, model_name, model_templates_dirpath):

        template_templates = \
            get_templates_in_dir('generate_scaffold/tpls')
        model = get_model(app_name, model_name)

        if model:
            model_fields = \
                [f.name for f in model._meta.fields if f.name != 'id']
        elif not self.dry_run:
            raise CommandError(
                'Could not load model: {0}\n'
                'Please report this issue.'.format(model_name)
            )
        else:
            # Cannot determine fields on dry run
            model_fields = []

        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        for template_template in template_templates:

            if not self.is_timestamped and '_archive' in template_template:
                # Do not render templates for date-based views.
                break

            filename = os.path.basename(template_template)
            dst_filename = filename.replace('MODEL_NAME', slugify(model_name))
            dst_abspath = os.path.join(model_templates_dirpath, dst_filename)
            t = get_template(template_template)
            c = {
                'app_name': app_name,
                'model_slug': model_slug,
                'model_fields': model_fields,
                'class_name': class_name,
                'filename': dst_abspath,
                'is_timestamped': self.is_timestamped,
            }
            rendered_template = t.render(Context(c))
            yield dst_abspath, rendered_template

    def handle(self, *args, **options):
        self.verbose = int(options.get('verbosity')) > 1
        self.dry_run = options.get('dry_run', False)
        self.is_timestamped = options.get('is_timestamped_model', True)
        self.is_naive_time = options.get('is_naive_time', False)

        try:
            app_name = args[0]
        except IndexError:
            raise CommandError('You must provide an app_name.')

        if app_name not in settings.INSTALLED_APPS:
            raise CommandError(
                'You must add {0} to your INSTALLED_APPS '
                'in order for {1} to generate templates.'.format(
                    app_name, self.command_name,
                )
            )

        try:
            app_module = __import__(app_name)
        except ImportError:
            raise CommandError(
                'Could not import app with name: {0}'.format(app_name))

        app_dirpath = app_module.__path__[0]

        try:
            model_name = args[1]
        except IndexError:
            raise CommandError('You must provide a model_name.')

        # Validate model name.
        original_model_name = model_name
        model_name = get_valid_variable(model_name)
        if not model_name:
            raise CommandError(
                '{0} is not a valid model name. '
                'Please choose a different name.'.format(original_model_name)
            )

        app_models_import_path = '{0}.models'.format(app_name)
        try:
            app_models_module = import_child(app_models_import_path)
        except ImportError:
            raise CommandError(
                'Could not import {0}\n'
                'Make sure your current models are valid '
                'and try again.'.format(app_models_import_path))

        if hasattr(app_models_module, dumb_capitalized(model_name)):
            raise CommandError('{0}.{1} already exists.'.format(
                app_models_import_path, dumb_capitalized(model_name)))

        app_views_dirpath = os.path.join(app_dirpath, 'views')
        model_views_filename = '{0}_views.py'.format(slugify(model_name))
        model_views_filepath = os.path.join(
            app_views_dirpath, model_views_filename)

        if os.path.isfile(model_views_filepath):
            raise CommandError(
                '{0} already exists.'.format(model_views_filepath))

        model_field_args = args[2:]
        if not model_field_args:
            # TODO - Allow models with only a primary key?
            raise CommandError('Cannot generate model with no fields.')

        for model_field_arg in model_field_args:
            if ':' not in model_field_arg:
                raise CommandError(
                    'No field type specified for '
                    'model field: {0}'.format(model_field_arg)
                )

        rendered_model = self._get_rendered_model(
            app_name, app_models_module, model_name, model_field_args)

        app_urls_filepath = os.path.join(app_dirpath, 'urls.py')
        if not os.path.isfile(app_urls_filepath) and self.dry_run:
            raise CommandError(
                'It appears you don\'t have a valid URLconf in your '
                '{app_name} app. Please create a valid urls.py file '
                'and try again.\nAlternatively, you can try again without '
                'appending --dry-run to this command, in which case '
                '{cmd_name} will make a valid URLconf for you.'.format(
                    app_name=app_name, cmd_name=self.command_name
                )
            )


        with FilesystemTransaction(self.dry_run, self) as transaction:
            ### Generate model ###
            app_models_filepath = os.path.join(app_dirpath, 'models.py')

            with transaction.open(app_models_filepath, 'a+') as f:
                f.write(rendered_model)
                f.seek(0)
                self.log(f.read())

            # FIXME - Reload models
            reload_django_appcache()
            exec('from {0}.models import *'.format(app_name))


            ### Generate views ###
            transaction.mkdir(app_views_dirpath)
            app_views_init_filepath = \
                os.path.join(app_views_dirpath, '__init__.py')

            if os.path.isdir(app_views_init_filepath):
                raise CommandError(
                    'Could not create file: {0}\n'
                    'Please remove the directory at that location '
                    'and try again.',format(app_views_init_filepath)
                )
            elif not os.path.exists(app_views_init_filepath):
                with transaction.open(app_views_init_filepath, 'a+') as f:
                    f.write('')
            else:
                self.msg('exists', app_views_init_filepath)

            rendered_views = self._get_rendered_views(app_name, model_name)

            with transaction.open(model_views_filepath, 'a+') as f:
                f.write(rendered_views)
                f.seek(0)
                self.log(f.read())


            ### Generate URLs ###
            is_user_defined_app_urls = False
            if not os.path.isfile(app_urls_filepath):
                with transaction.open(app_urls_filepath, 'a+') as f:
                    s = 'from django.conf.urls import patterns, url\n\n'
                    f.write(s)
                    f.seek(0)
                    self.log(f.read())
            else:
                is_user_defined_app_urls = True
                self.msg('exists', app_urls_filepath)

            app_urls_import_path = '{0}.urls'.format(app_name)
            try:
                urls_module = import_child(app_urls_import_path)
            except:
                if is_user_defined_app_urls:
                    raise CommandError(
                        'Could not import {0}\n'
                        'Make sure your URLConf is valid '
                        'and try again.'.format(app_urls_import_path))
                else:
                    raise CommandError(
                        'Something went wrong when creating {0}.\n'
                        'Please file a bug report.'
                    )

            is_urlpatterns_available = \
                hasattr(urls_module, 'urlpatterns')
            rendered_urls = self._get_rendered_urls(
                app_name, model_name, is_urlpatterns_available)

            with transaction.open(app_urls_filepath, 'a+') as f:
                f.write(rendered_urls)
                f.seek(0)
                self.log(f.read())


            ### Generate templates ###
            app_templates_root_dirpath = \
                os.path.join(app_dirpath, 'templates')
            transaction.mkdir(app_templates_root_dirpath)

            app_templates_app_dirpath = os.path.join(
                app_templates_root_dirpath, app_name)
            transaction.mkdir(app_templates_app_dirpath)

            model_templates_dirpath = os.path.join(
                app_templates_app_dirpath, slugify(model_name))
            transaction.mkdir(model_templates_dirpath)


            rendered_templates = self._get_rendered_templates(
                app_name, model_name, model_templates_dirpath)

            for dst_abspath, rendered_template in rendered_templates:
                if os.path.isfile(dst_abspath):
                    self.msg('exists', dst_abspath)
                else:
                    with transaction.open(dst_abspath, 'a+') as f:
                        f.write(rendered_template)
                        f.seek(0)
                        self.log(f.read())


        # Compiled files cause problems when run
        # immediately after generation
        clean_pyc_in_dir(app_dirpath)
