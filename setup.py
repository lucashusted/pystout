# python setup.py sdist bdist_wheel
# twine upload dist/*

import io
import os

from setuptools import setup, find_packages

dir = os.path.dirname(__file__)

with io.open(os.path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pystout',
    version='0.0.5',
    description='A Package To Make Publication Quality Latex Tables From Python Regression Output',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lucashusted/pystout',
    author='Lucas Husted',
    author_email='lucas.f.husted@columbia.edu',
    license='GNU',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        ],
    install_requires=['numpy','pandas>=0.25'],
    python_requires='>=3',
    packages=find_packages()
)
