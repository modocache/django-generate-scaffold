from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator
from generate_scaffold.utils.directories import get_templates_in_dir
from generate_scaffold.utils.strings import dumb_capitalized


class UrlsGenerator(BaseGenerator):

    def render_urls(self, model_name, is_timestamped=True):
        urls_module = self.get_app_module('urls')
        is_urlpatterns_available = \
            hasattr(urls_module, 'urlpatterns')

        url_pattern_templates = \
            get_templates_in_dir('generate_scaffold/urls/urls')
        model_slug = slugify(model_name)
        class_name = dumb_capitalized(model_name)

        rendered_url_patterns = []
        for url_pattern_template in url_pattern_templates:
            t = get_template(url_pattern_template)
            c = {
                'app_name': self.app_name,
                'model_slug': model_slug,
                'class_name': class_name,
                'is_timestamped': is_timestamped,
            }
            rendered_url_patterns.append(t.render(Context(c)))

        url_patterns_operator = '+=' if is_urlpatterns_available else '='
        urls_template = get_template('generate_scaffold/urls/urls.txt')
        c = {
            'app_name': self.app_name,
            'model_slug': model_slug,
            'url_patterns_operator': url_patterns_operator,
            'urls': rendered_url_patterns,
        }
        return urls_template.render(Context(c))
