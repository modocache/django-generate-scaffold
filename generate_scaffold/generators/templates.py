import os

from django.db.models import get_model
from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator, GeneratorError
from generate_scaffold.utils.directories import get_templates_in_dir
from generate_scaffold.utils.strings import dumb_capitalized


class TemplatesGenerator(BaseGenerator):

    def get_model_fields(self, model_name):
        model = get_model(self.app_name, model_name)

        if model:
            model_fields = \
                [f.name for f in model._meta.fields if f.name != 'id']
        else:
            raise GeneratorError(
                'Could not load model: {0}'.format(model_name)
            )

        return model_fields

    def render_templates(
            self, model_name, model_fields, model_templates_dirpath, is_timestamped=True):

        template_templates = \
            get_templates_in_dir('generate_scaffold/tpls')

        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        for template_template in template_templates:

            if not is_timestamped and '_archive' in template_template:
                # Do not render templates for date-based views.
                break

            filename = os.path.basename(template_template)
            dst_filename = filename.replace('MODEL_NAME', slugify(model_name))
            dst_abspath = os.path.join(model_templates_dirpath, dst_filename)
            t = get_template(template_template)
            c = {
                'app_name': self.app_name,
                'model_slug': model_slug,
                'model_fields': model_fields,
                'class_name': class_name,
                'filename': dst_abspath,
                'is_timestamped': is_timestamped,
            }
            rendered_template = t.render(Context(c))
            yield dst_abspath, rendered_template
