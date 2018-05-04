from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()


setup(
    name='irekia',
    version='0.1.1',
    author='eillarra',
    author_email='eneko@illarra.com',
    license='MIT',
    url='https://github.com/eillarra/irekia',
    project_urls={
        'Code': 'https://github.com/eillarra/irekia',
        'Issues': 'https://github.com/eillarra/irekia/issues',
    },
    description='Python client for the Open Data Euskadi REST API.',
    long_description=long_description,
    keywords='opendata api euskadi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['irekia'],
    package_dir={'irekia': 'irekia'},
    package_data={'irekia': ['data/*.json']},
    install_requires=['requests'],
    zip_safe=False
)
