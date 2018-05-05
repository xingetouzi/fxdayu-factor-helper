import codecs

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)


def readme():
    with codecs.open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


def version():
    return "0.1.0"


requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]
setup(
    name='fxdayu_factor_helper',
    version=version(),
    packages=find_packages(exclude=["examples", "tests", "tests.*", "docs"]),
    author='xingetouzi',
    author_email='public@fxdayu.com',
    license='Apache License v2',
    url='https://github.com/xingetouzi/fxdayu-factor-helper',
    install_requires=requirements,
    long_description=readme(),
    entry_points={
        "console_scripts": [
            "dyfactor = fxdayu_factor_helper.__main__:main"
        ]
    },
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)