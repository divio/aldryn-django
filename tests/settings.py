#!/usr/bin/env python
HELPER_SETTINGS = {
    'INSTALLED_APPS': [],
    'LANGUAGE_CODE': 'en',
    'ALLOWED_HOSTS': ['localhost'],
}


def run():
    from app_helper import runner
    runner.run('aldryn_django')


if __name__ == '__main__':
    run()
