import django


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'tree_test',
            }
        },
        INSTALLED_APPS=(
            'tree',
            'tests',
        ),
    )

    django.setup()
