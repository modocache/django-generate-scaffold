import os

from django.core.management.color import supports_color
from django.utils import termcolors


class VerboseCommandMixin(object):

    def __init__(self, *args, **kwargs):
        super(VerboseCommandMixin, self).__init__(*args, **kwargs)
        self.dry_run = False
        if supports_color():
            opts = ('bold',)
            self.style.EXISTS = \
                termcolors.make_style(fg='blue', opts=opts)
            self.style.APPEND = \
                termcolors.make_style(fg='yellow', opts=opts)
            self.style.CREATE = \
                termcolors.make_style(fg='green', opts=opts)
            self.style.REVERT = \
                termcolors.make_style(fg='magenta', opts=opts)
            self.style.BACKUP = \
                termcolors.make_style(fg='cyan', opts=opts)

    def msg(self, action, path):
        is_withholding_action = False
        non_actions = set(['create', 'append', 'revert'])
        if self.dry_run and action in non_actions:
            is_withholding_action = True

        if hasattr(self.style, action.upper()):
            s = getattr(self.style, action.upper())
            action = s(action)

        if is_withholding_action:
            action = self.style.NOTICE('did not ') + action

        output = '\t{0:>25}\t{1:<}\n'.format(action, os.path.relpath(path))
        self.stdout.write(output)

    def log(self, output):
        if self.verbose:
            self.stdout.write(output)
