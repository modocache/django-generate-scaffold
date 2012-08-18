import inspect

from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator, GeneratorError, \
                                              FIELD_ALIASES, \
                                              RELATIONSHIP_FIELDS
from generate_scaffold.utils.strings import dumb_capitalized, \
                                            get_valid_variable


class ModelsGenerator(BaseGenerator):

    def get_field_key(self, name):
        for field_key, aliases in FIELD_ALIASES.items():
            if name in aliases:
                return field_key

        return None

    def render_field(self, field_name, field_key_alias, other_model=None):
        original_field_name = field_name
        field_name = get_valid_variable(field_name)
        if not field_name:
            raise GeneratorError(
                '{0} is not a valid field name.'.format(original_field_name))
        field_name = field_name.lower()

        field_key = self.get_field_key(field_key_alias)
        if not field_key:
            raise GeneratorError(
                '{0} is not a recognized django.db.models.fields '
                'type.'.format(field_key))

        if field_key in RELATIONSHIP_FIELDS and other_model is None:
            raise GeneratorError(
                '{0} requires a related model to be '
                'specified.'.format(field_key)
            )

        tpl_name = \
            'generate_scaffold/models/fields/{0}.txt'.format(field_key)
        tpl = get_template(tpl_name)
        c = {
            'field_name': field_name,
            'other_model': other_model,
        }
        context = Context(c)
        return tpl.render(context)

    def render_model(self, model_name, fields, add_timestamp=True):
        # FIXME - Ensure model_name is valid
        rendered_fields = [self.render_field(*field) for field in fields]

        app_models_module = self.get_app_module('models')

        if hasattr(app_models_module, model_name):
            raise GeneratorError('{0}.models.{1} already exists.'.format(
                self.app_name, model_name))
        elif hasattr(app_models_module, dumb_capitalized(model_name)):
            raise GeneratorError('{0}.models.{1} already exists.'.format(
                self.app_name, dumb_capitalized(model_name)))

        available_modules = inspect.getmembers(
            app_models_module, inspect.ismodule)

        import_db_models = False
        if not [m for m in available_modules
          if m[0] == 'models' and m[-1].__name__ == 'django.db.models']:
            import_db_models = True

        app_models_functions = inspect.getmembers(
            app_models_module, inspect.isfunction)

        import_now = add_timestamp
        if [f for f in app_models_functions
          if f[0] == 'now' and f[-1].__module__ == 'django.utils.timezone']:
            import_now = False

        model_template = get_template('generate_scaffold/models/models.txt')
        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)
        c = {
            'import_db_models': import_db_models,
            'import_now': import_now,
            'app_name': self.app_name,
            'model_slug': model_slug,
            'class_name': class_name,
            'fields': rendered_fields,
            'is_timestamped_model': add_timestamp,
        }
        return model_template.render(Context(c)), class_name
