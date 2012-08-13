import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils import translation
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

from generate_scaffold.generators import ModelsGenerator, ViewsGenerator, \
                                         UrlsGenerator, TemplatesGenerator, \
                                         GeneratorError
from generate_scaffold.management.transactions import FilesystemTransaction
from generate_scaffold.management.verbosity import VerboseCommandMixin
from generate_scaffold.utils.cacheclear import clean_pyc_in_dir, \
                                               reload_django_appcache
from generate_scaffold.utils.modules import import_child


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
            help=_('Do not actually do anything, but print what '
                   'would have happened to the console.')
        ),
        make_option('-m', '--model',
            dest='existing_model',
            help=_('An existing model to generate views/templates for.')
        ),
        make_option('-t', '--timestamp-field',
            dest='timestamp_fieldname',
            help=_('The name of the field used as a timestamp for date-based '
                   'views. This option may only be used when passing a model '
                   'via the `--model` option.')
        ),
        make_option('-n', '--no-timestamps',
            action='store_false',
            dest='is_timestamped',
            default=True,
            help=_('Do not automatically append created_at and updated_at '
                   'DateTimeFields to generated models.')
        ),
    )

    def handle(self, *args, **options):
        if settings.USE_I18N:
            translation.activate(settings.LANGUAGE_CODE)

        try:
            self.generate_scaffold(*args, **options)
        finally:
            if settings.USE_I18N:
                translation.deactivate()


    def generate_scaffold(self, *args, **options):
        self.verbose = int(options.get('verbosity')) > 1
        self.dry_run = options.get('dry_run', False)
        self.is_timestamped = options.get('is_timestamped', True)
        self.existing_model = options.get('existing_model', None)
        self.timestamp_fieldname = options.get('timestamp_fieldname', None)

        if self.timestamp_fieldname and not self.existing_model:
            raise CommandError(smart_str(_(
                'The --timestamp-field option can only be used if --model '
                'is specified.')))

        try:
            app_name = args[0]
        except IndexError:
            raise CommandError('You must provide an app_name.')

        if app_name not in settings.INSTALLED_APPS:
            raise CommandError(smart_str(_(
                'You must add {0} to your INSTALLED_APPS '
                'in order for {1} to generate templates.'.format(
                    app_name, self.command_name))))

        try:
            app_module = __import__(app_name)
        except ImportError:
            raise CommandError(smart_str(_(
                'Could not import app with name: {0}'.format(app_name))))

        app_dirpath = app_module.__path__[0]

        if not self.existing_model:
            try:
                model_name = args[1]
            except IndexError:
                raise CommandError(
                    smart_str(_('You must provide a model_name.')))
        else:
            model_name = self.existing_model

        app_views_dirpath = os.path.join(app_dirpath, 'views')
        model_views_filename = '{0}_views.py'.format(slugify(model_name))
        model_views_filepath = os.path.join(
            app_views_dirpath, model_views_filename)

        # TODO - Append to views file if already exists
        if os.path.isfile(model_views_filepath):
            raise CommandError(smart_str(_(
                '{0} already exists.'.format(model_views_filepath))))

        pos_args = [a.split(':') for a in args[2:]]
        model_field_args = []
        for a in pos_args:
            # Split for other_model relationship
            split = [item for sublist in a for item in sublist.split('=')]
            model_field_args.append(split)

        if not model_field_args and not self.existing_model:
            # TODO - Allow models with only a primary key?
            raise CommandError(smart_str(_(
                'Cannot generate model with no fields.')))

        for arg in [a for a in model_field_args if len(a) < 2]:
            raise CommandError(smart_str(_(
                'No field type specified for model field: {0}'.format(arg))))

        if not self.existing_model:
            models_generator = ModelsGenerator(app_name)
            try:
                rendered_model, rendered_model_name = \
                    models_generator.render_model(
                        model_name, model_field_args, self.is_timestamped)
            except GeneratorError as err:
                raise CommandError(smart_str(_(
                    'Could not generate model.\n{0}'.format(err))))

        app_urls_filepath = os.path.join(app_dirpath, 'urls.py')
        if not os.path.isfile(app_urls_filepath) and self.dry_run:
            raise CommandError(smart_str(_(
                'It appears you don\'t have a valid URLconf in your '
                '{app_name} app. Please create a valid urls.py file '
                'and try again.\nAlternatively, you can try again without '
                'appending --dry-run to this command, in which case '
                '{cmd_name} will make a valid URLconf for you.'.format(
                    app_name=app_name, cmd_name=self.command_name))))


        with FilesystemTransaction(self.dry_run, self) as transaction:
            ### Generate model ###
            app_models_filepath = os.path.join(app_dirpath, 'models.py')

            if not self.existing_model:
                with transaction.open(app_models_filepath, 'a+') as f:
                    f.write(rendered_model)
                    f.seek(0)
                    self.log(f.read())

                # FIXME - Reload models, use namespace
                reload_django_appcache()
                exec('from {0}.models import *'.format(app_name))

            # The rest of the generators use model introspection to
            # generate views, urlpatterns, etc.
            if not self.existing_model and self.dry_run:
                # Since the model is not actually created on dry run,
                # execute the model code. This is probably a Very Bad
                # Idea.
                with open(app_models_filepath, 'r') as f:
                    code = compile(
                        f.read() + rendered_model, '<string>', 'exec')

                # Ensure django.db.models is available in namespace
                import_child('django.db.models')

                # FIXME - Use namespace dictionary
                exec code in globals()

                # Get reference to generated_model
                code_str = 'generated_model = {0}().__class__'.format(
                        rendered_model_name)
                code = compile(code_str, '<string>', 'exec')
                exec code in globals()
                generated_model = globals()['generated_model']
            else:
                generated_model = get_model(app_name, model_name)

            if not generated_model:
                raise CommandError(smart_str(_(
                    'Something when wrong when generating model '
                    '{0}'.format(model_name))))


            ### Generate views ###
            transaction.mkdir(app_views_dirpath)
            app_views_init_filepath = \
                os.path.join(app_views_dirpath, '__init__.py')

            if os.path.isdir(app_views_init_filepath):
                raise CommandError(smart_str(_(
                    'Could not create file: {0}\n'
                    'Please remove the directory at that location '
                    'and try again.'.format(app_views_init_filepath))))
            elif not os.path.exists(app_views_init_filepath):
                with transaction.open(app_views_init_filepath, 'a+') as f:
                    f.write('')
            else:
                self.msg('exists', app_views_init_filepath)

            views_generator = ViewsGenerator(app_name)
            rendered_views = views_generator.render_views(
                generated_model, self.timestamp_fieldname)

            with transaction.open(model_views_filepath, 'a+') as f:
                f.write(rendered_views)
                f.seek(0)
                self.log(f.read())


            ### Generate URLs ###
            if not os.path.isfile(app_urls_filepath):
                with transaction.open(app_urls_filepath, 'a+') as f:
                    s = 'from django.conf.urls import patterns, url\n\n'
                    f.write(s)
                    f.seek(0)
                    self.log(f.read())
            else:
                self.msg('exists', app_urls_filepath)

            urls_generator = UrlsGenerator(app_name)
            rendered_urls = urls_generator.render_urls(
                generated_model, self.timestamp_fieldname)

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

            templates_generator = TemplatesGenerator(app_name)

            rendered_templates = templates_generator.render_templates(
                generated_model,
                model_templates_dirpath,
                self.timestamp_fieldname
            )

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
