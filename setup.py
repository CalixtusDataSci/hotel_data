#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hotel Data Cleaning and Analysis Package
Professional Data Science & Machine Learning Project

Author: Nwaeke Calixtus, Esq
License: MIT (see LICENSE file)
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hotel-data-cleaner",
    version="1.0.0",
    author="Nwaeke Calixtus, Esq",
    author_email="calixtusnwaeke@gmail.com",
    description="Professional hotel booking data cleaning, analysis, and ML-ready dataset preparation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CalixtusDataSci/hotel_data",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Data Scientists",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Professionals",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "isort>=5.0",
            "pylint>=3.0",
            "mypy>=1.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "xgboost>=2.0.0",
            "scipy>=1.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "clean-hotel-data=scripts.clean_data:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
