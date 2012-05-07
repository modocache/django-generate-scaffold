from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator
from generate_scaffold.utils.directories import get_templates_in_dir
from generate_scaffold.utils.strings import dumb_capitalized


class ViewsGenerator(BaseGenerator):

    # FIXME - Should inspect model and check if it has a 
    #           a datetime field which could be used.
    def render_views(self, model_name, is_timestamped):
        views_class_templates = \
            get_templates_in_dir('generate_scaffold/views/views')

        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        rendered_views_classes = []
        for view_class_template in views_class_templates:

            t = get_template(view_class_template)
            c = {
                'app_name': self.app_name,
                'model_slug': model_slug,
                'class_name': class_name,
                'is_timestamped': is_timestamped,
            }
            rendered_views_classes.append(t.render(Context(c)))

        views_template = get_template('generate_scaffold/views/views.txt')
        views_context = {
            'app_name': self.app_name,
            'class_name': class_name,
            'model_slug': model_slug,
            'views': rendered_views_classes,
            'is_timestamped': is_timestamped,
        }
        return views_template.render(Context(views_context))
