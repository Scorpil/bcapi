import codecs
from setuptools import setup, find_packages


__author__ = 'Andrew Savchyn'
__version__ = '0.0.1-dev'
__licence__ = 'BSD'
description = "Wrapper for BlockChain.info API's."

install_requires = [
    'requests>=2.2.1'
]

tests_require = [
    'mock',
]

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()

setup(
    name='bcapi',
    version=__version__,
    description=description,
    long_description=long_description(),
    download_url='https://github.com/scorpil/bcapi',
    author=__author__,
    author_email='webdev@scorpil.com',
    license=__licence__,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    zip_safe=True,
    keywords='bitcoin blockchain api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Utilities'
    ])
