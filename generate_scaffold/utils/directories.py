import os

from django.template.loaders import app_directories


def get_templates_in_dir(dir_suffix):
    template_dirs = []
    for app_template_dir in app_directories.app_template_dirs:
        for root, _, _ in os.walk(app_template_dir):
            if root.endswith(dir_suffix):
                template_dirs.append(root)

    for template_dir in template_dirs:
        for root, _, files in os.walk(template_dir):
            public_files = [f for f in files if not f.startswith('.')]

            for f in sorted(public_files):
                yield os.path.join(root, f)
