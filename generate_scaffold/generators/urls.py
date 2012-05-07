from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import get_template

from generate_scaffold.generators.base import BaseGenerator
from generate_scaffold.utils.directories import get_templates_in_dir
from generate_scaffold.utils.strings import dumb_capitalized


class UrlsGenerator(BaseGenerator):

    def render_urls(self):
        pass

