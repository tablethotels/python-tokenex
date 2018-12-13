import os
from setuptools import setup, find_packages
from io import open
from tokenex import __version__


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'requirements_dev.txt')) as f:
    test_required = f.read().splitlines()
    if test_required[0] == "-r requirements.txt":
        test_required.pop(0)

setup(
    name='python-tokenex',
    version=__version__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tokenex = tokenex.cli.__main__:main'
        ]
    },
    install_requires=required,
    tests_require=test_required,
    include_package_data=True,
    license='MIT License',
    description='Tablet Base Configuration module',
    author='Tablet, Inc',
    author_email='ops@tablethotels.com',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
