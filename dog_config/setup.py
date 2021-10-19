#!/usr/bin/env python3
from os import chdir
from os import pardir
from os.path import abspath
from os.path import join
from os.path import normpath

from setuptools import setup


INSTALL_REQUIRES = ['dog_apps']
chdir(normpath(join(abspath(__file__), pardir)))
setup(
    name='dog_config',
    use_scm_version={
        "root": "..",
        "fallback_version": ""
    },
    setup_requires=['setuptools_scm'],
    packages=['dog_project'],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    license='GPLv3',
    description='CLARIN Digital Object Gate, a Django application. ',
    long_description='See README.md',
    url='',
    author=['Michał Gawor'],
    author_email=['michal@clarin.eu'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
