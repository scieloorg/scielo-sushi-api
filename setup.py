from setuptools import setup


requires = [
    'mysqlclient',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_tm',
    'sqlalchemy',
    'waitress',
    'zope.sqlalchemy',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]

setup(
    name='scielo-sushiapi',
    version='0.1',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = api:main'
        ],
        'console_scripts': [
            'initialize_db = api.initialize_db:main'
        ],
    },
)
