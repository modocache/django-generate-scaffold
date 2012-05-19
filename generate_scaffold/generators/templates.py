import os

from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator
from generate_scaffold.utils.directories import get_templates_in_dir


class TemplatesGenerator(BaseGenerator):

    def get_model_fields(self, model):
        return [f.name for f in model._meta.fields if f.name != 'id']

    def render_templates(
            self, model, model_templates_dirpath, timestamp_fieldname=None):

        template_templates = \
            get_templates_in_dir('generate_scaffold/tpls')

        class_name = model._meta.concrete_model.__name__
        model_slug = slugify(class_name)
        model_fields = self.get_model_fields(model)

        timestamp_field = self.get_timestamp_field(
            model, timestamp_fieldname)
        is_timestamped = True if timestamp_field else False

        for template_template in template_templates:

            if not is_timestamped and '_archive' in template_template:
                # Do not render templates for date-based views.
                continue

            filename = os.path.basename(template_template)
            dst_filename = filename.replace('MODEL_NAME', model_slug)
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
            if is_timestamped:
                c['timestamp_field'] = timestamp_field.name

            rendered_template = t.render(Context(c))
            yield dst_abspath, rendered_template
