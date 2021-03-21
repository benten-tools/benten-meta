from setuptools import setup
import os

requires = ["PyYAML>=5.3.1"]
scripts  = ["scripts/benten-meta.py"]

if os.name == "nt" : # Windows
    scripts.extend(["scripts/benten-meta.bat"])

with open('README.md') as f:
    readme = f.read()

setup(
    name='benten-meta',
    version='0.0.1.post2',
    description='benten metadata tool',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/benten-tools/benten-meta',
    author='Takahiro Matsumoto',
    author_email='matumot@spring8.or.jp',
    license='Apache License 2.0',
    keywords='benten metadata tool',
    scripts=scripts,
    packages=[
        "benten_meta",
    ],
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
