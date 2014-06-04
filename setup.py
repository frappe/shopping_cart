from setuptools import setup, find_packages
import os
from shopping_cart.__version__ import __version__ as version

setup(
    name='shopping_cart',
    version=version,
    description='Online Shopping Cart integrated with ERPNext',
    author='Web Notes Technologies',
    author_email='info@erpnext.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
