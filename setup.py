from setuptools import setup


setup(
    name='irekia',
    version='0.1.0',
    url='https://github.com/eillarra/irekia',
    author='eillarra',
    author_email='eneko@illarra.com',
    license='MIT',
    description='Python client for the Open Data Euskadi REST API.',
    long_description=open('README.rst').read(),
    keywords='opendata api euskadi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['irekia'],
    package_dir={'irekia': 'irekia'},
    package_data={'irekia': ['data/*.json']},
    install_requires=['requests'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)
