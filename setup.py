import os
import sys
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.1'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='the-great-suspender-restore-urls',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    version=version,
    url='http://github.com/barseghyanartur/the-great-suspender-restore-urls',
    py_modules=['thegreatsuspender'],
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/the-great-suspender-restore-urls/issues",
        "Source Code": "https://github.com/barseghyanartur/the-great-suspender-restore-urls/",
        "Changelog": "https://github.com/barseghyanartur/the-great-suspender-restore-urls/blob/master/CHANGELOG.md",
    },
    entry_points={
        'console_scripts': [
            'restore-the-great-suspender-urls = thegreatsuspender:cli'
        ]
    },
    include_package_data=True,
    keywords='thegreatsuspender, the great suspender',
    description='Restore your thegreatsuspender tabs.',
    long_description=readme,
    license='GPL-2.0-only OR LGPL-2.1-or-later',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "License :: OSI Approved :: MIT License",
    ],
)
