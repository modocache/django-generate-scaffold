import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from generate_scaffold.generators import ModelsGenerator, ViewsGenerator, \
                                         UrlsGenerator, TemplatesGenerator, \
                                         GeneratorError
from generate_scaffold.management.transactions import FilesystemTransaction
from generate_scaffold.management.verbosity import VerboseCommandMixin
from generate_scaffold.utils.cacheclear import clean_pyc_in_dir, \
                                               reload_django_appcache


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
        make_option('-n', '--dry-run',
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
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.verbose = False
        self.dry_run = False

    def handle(self, *args, **options):
        self.verbose = int(options.get('verbosity')) > 1
        self.dry_run = options.get('dry_run', False)
        self.is_timestamped = options.get('is_timestamped_model', True)

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

        app_views_dirpath = os.path.join(app_dirpath, 'views')
        model_views_filename = '{0}_views.py'.format(slugify(model_name))
        model_views_filepath = os.path.join(
            app_views_dirpath, model_views_filename)

        if os.path.isfile(model_views_filepath):
            raise CommandError(
                '{0} already exists.'.format(model_views_filepath))

        pos_args = [a.split(':') for a in args[2:]]
        model_field_args = []
        for a in pos_args:
            # Split for other_model relationship
            split = [item for sublist in a for item in sublist.split('=')]
            model_field_args.append(split)

        if not model_field_args:
            # TODO - Allow models with only a primary key?
            raise CommandError('Cannot generate model with no fields.')

        for arg in [a for a in model_field_args if len(a) < 2]:
            raise CommandError(
                'No field type specified for '
                'model field: {0}'.format(arg)
            )

        models_generator = ModelsGenerator(app_name)
        try:
            rendered_model = models_generator.render_model(
                model_name, model_field_args)
        except GeneratorError as err:
            raise CommandError(
                'Could not generate model.\n{0}'.format(err)
            )

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

            views_generator = ViewsGenerator(app_name)
            rendered_views = views_generator.render_views(
                model_name, self.is_timestamped)

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
                model_name, self.is_timestamped)

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

            try:
                model_fields = templates_generator.get_model_fields(model_name)
            except GeneratorError:
                if self.dry_run:
                    model_fields = []
                else:
                    raise

            rendered_templates = templates_generator.render_templates(
                model_name, model_fields, model_templates_dirpath)

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
