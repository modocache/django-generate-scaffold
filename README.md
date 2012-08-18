# django-generate-scaffold [![build-status](https://secure.travis-ci.org/modocache/django-generate-scaffold.png)](http://travis-ci.org/#!/modocache/django-generate-scaffold) [![endorse](http://api.coderwall.com/modocache/endorsecount.png)](http://coderwall.com/modocache)

Generate a Django model, views, URLconf, and templates using a single command.


## Quickstart

A screencast introducing `django-generate-scaffold` is
available [here](http://vimeo.com/42399125).


## Usage

### Generating Models, Views, URL Patterns, and Templates

- Install `django-generate-scaffold`:

        $ pip install django-generate-scaffold

- Add `generate_scaffold` to your `INSTALLED_APPS`
- Run the `generatescaffold` management command:


        $ python manage.py generatescaffold --help
        ... displays usage

- Create a model using the syntax in the help message:

        $ python manage.py generatescaffold blogs Post title:string body:text is_public:bool blog:foreignkey=Blog
        ... Generates a Post model, with title (CharField), body (TextField),
        ...     is_public (BooleanField), and blog (ForeignKey) fields.

### Generating Views, etc. Based on Existing Models

- Alternatively, you can generate views, urlpatterns, and templates for an existing model:

        $ python manage.py generatescaffold blogs --model Post
        ... Generates views, etc. for Post


- Note that if the model specified with the `--model` option has a `DateField` or a `DateTimeField`,
  date-based generic views will be generated based on that field. To specify a specific field to use,
  pass in the `--timestamp-field` option:

        $ python manage.py generatescaffold blogs --model Post --timestamp-field ctime

#### Limitations When Using Existing Models

For best results, existing models should implement a `get_absolute_url` method
which conforms to the urlpatterns used by `django-generate-scaffold`:

        @models.permalink
        def get_absolute_url(self):
            return ('<app_name>_<model_name>_detail', (), {'pk': self.pk})

Not conforming to this model will lead to broken links and potentially other
issues when rendering templates.


## Development

`django-generate-scaffold` is currently in ALPHA.

### Running Tests

In order to run the test suite, install your local version of `django-generate-scaffold`
and start a Selenium server and issue the following commands:

        $ cd django-generate-scaffold
        $ python setup.py install --force
        $ cd test_project
        $ python test_app/tests/runtests.py

Consult `.travis.yml` for the exact steps necessary to run the test
suite.

#### Autotesting via watchr

By installing the gems in the Gemfile, you can automatically run all non-Selenium
based tests every time a file is modified:

        $ watchr autotest.rb

### How to Contribute

- Propose new features or report bugs by creating an issue on Github.
- Add new features, tests, or fix stuff and issue a pull request.
- Create a better, more eloquent screencast with less stammering.


## Issues

If you experience any issues, please
[create an issue on Github](https://github.com/modocache/django-generate-scaffold/issues).
