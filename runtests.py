""" run tests for pagetree

$ virtualenv ve
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
            'django_nose',
        ),
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',

        NOSE_ARGS=[
            '--cover-package=pageblocks',
        ],
        PROJECT_APPS=[
            'pageblocks',
        ],
        ROOT_URLCONF=[],
        PAGEBLOCKS=['pagetree.TestBlock', ],

        # Django replaces this, but it still wants it. *shrugs*
        DATABASES={
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

    django.setup()

    # Fire off the tests
    call_command('test')


if __name__ == '__main__':
    main()
