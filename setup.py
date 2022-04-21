#!/usr/bin/env python3

from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="knarrow",
    version="0.6.0",
    description="Shoot a knarrow to the knee",
    # Use UTF-8 encoding for README even on Windows by using the encoding argument.
    long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords=["python"],
    author="Marijan Smetko",
    author_email="msmetko@msmetko.xyz",
    url="https://github.com/InCogNiTo124/knarrow",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    # pip 9.0+ will inspect this field when installing to help users install a
    # compatible version of the library for their Python version.
    python_requires=">=3.7",
    # There are some peculiarities on how to include package data for source
    # distributions using setuptools. You also need to add entries for package
    # data to MANIFEST.in.
    # See https://stackoverflow.com/questions/7522250/
    include_package_data=True,
    # This file is required to inform mypy that inline type hints are used.
    #   See: https://mypy.readthedocs.io/en/stable/installed_packages.html
    package_data={"knarrow": ["py.typed"]},
    # This is a trick to avoid duplicating dependencies between both setup.py and
    # requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    # It does not work for all types of dependencies (e.g. VCS dependencies).
    # For VCS dependencies, use pip >= 19 and the PEP 508 syntax.
    #   Example: 'requests @ git+https://github.com/requests/requests.git@branch_or_tag'
    #   See: https://github.com/pypa/pip/issues/6162
    install_requires=project_dir.joinpath("requirements.txt").read_text().split("\n"),
    zip_safe=False,
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    entry_points={"console_scripts": ["knarrow=knarrow.cli.__main__:main"]},
)
