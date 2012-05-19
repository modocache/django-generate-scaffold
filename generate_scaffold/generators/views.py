from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator
from generate_scaffold.utils.directories import get_templates_in_dir


class ViewsGenerator(BaseGenerator):

    def render_views(self, model, timestamp_fieldname=None):
        views_class_templates = \
            get_templates_in_dir('generate_scaffold/views/views')

        class_name = model._meta.concrete_model.__name__
        model_slug = slugify(class_name)

        timestamp_field = self.get_timestamp_field(
            model, timestamp_fieldname)
        is_timestamped = True if timestamp_field else False

        views_context = {
            'app_name': self.app_name,
            'model_slug': model_slug,
            'class_name': class_name,
            'is_timestamped': is_timestamped,
        }
        if is_timestamped:
            views_context['timestamp_field'] = timestamp_field.name

        rendered_views_classes = []
        for view_class_template in views_class_templates:
            t = get_template(view_class_template)
            rendered_views_classes.append(t.render(Context(views_context)))

        views_template = get_template('generate_scaffold/views/views.txt')
        views_context['views'] = rendered_views_classes
        return views_template.render(Context(views_context))
