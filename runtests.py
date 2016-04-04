""" run tests for pagetree

$ virtualenv ve
$ ./ve/bin/pip install Django==1.8
$ ./ve/bin/pip install -r test_reqs.txt
$ ./ve/bin/python runtests.py
"""


import django
from django.conf import settings
from django.core.management import call_command


def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'pagetree',
            'pageblocks',
            'django_jenkins',
        ),
        TEST_RUNNER = 'django.test.runner.DiscoverRunner',

        JENKINS_TASKS = (
            'django_jenkins.tasks.with_coverage',
        ),
        PROJECT_APPS = [
            'pageblocks',
        ],
        COVERAGE_EXCLUDES_FOLDERS = ['migrations'],
        ROOT_URLCONF = [],
        PAGEBLOCKS = ['pagetree.TestBlock', ],
        SOUTH_TESTS_MIGRATE=False,

        # Django replaces this, but it still wants it. *shrugs*
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'HOST': '',
                'PORT': '',
                'USER': '',
                'PASSWORD': '',
                }
            }
    )

    try:
        # required by Django 1.7 and later
        django.setup()
    except AttributeError:
        pass

    # Fire off the tests
    call_command('test')

if __name__ == '__main__':
    main()
