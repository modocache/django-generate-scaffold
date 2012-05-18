# django-generate-scaffold [![endorse](http://api.coderwall.com/modocache/endorsecount.png)](http://coderwall.com/modocache)

Generate a Django model, views, URLconf, and templates using a single command.

## Quickstart

A screencast introducing `django-generate-scaffold` is
available [here](http://vimeo.com/42399125).

## Usage

1. Install `django-generate-scaffold`

    $ pip install django-generate-scaffold

2. Add `generate_scaffold` to your `INSTALLED_APPS`
3. Run the `generatescaffold` management command

    $ python manage.py generatescaffold --help
    ... displays usage
    $ python manage.py generatescaffold blogs Post title:string body:text is_public:bool blog:foreignkey=Blog
    ... Generates a Post model, with title (CharField), body (TextField), is_public (BooleanField),
    ...     and blog (ForeignKey) fields.


## Development

`django-generate-scaffold` is currently in ALPHA.
Everything works, but tests are not available at this time.

## Issues

If you experience any issues, please
[create an issue on Github](https://github.com/modocache/django-generate-scaffold/issues).

## How to Contribute

- Propose new features or report bugs by creating an issue on Github.
- Add new features, tests, or fix stuff and issue a pull request.
- Create a better, more eloquent screencast with less stammering.
