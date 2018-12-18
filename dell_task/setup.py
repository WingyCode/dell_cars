import sys

__py_version = 3
__py_minor_version = 4

import setuptools
# from setuptools import setup

install_requires_list = ['peewee', 'requests', 'flask']
# install_requires_list = []

if sys.version_info < (__py_version, __py_minor_version):
    print("The {}.{}.{} version of python is not supported!".format(*sys.version_info[0:3]))
    print("Please, use Python {}.{} or newer".format(__py_version, __py_minor_version))
    exit(1)

setuptools.setup(
    python_requires=">=3.4",
    author="Evgeny Kertsman",
    author_email="evgenii.kertcman@gmail.com",
    name="dell_cars", 
    version="0.1",
    # packages=['client', 'server', 'common', 'tests'],
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True, 
    entry_points={
        'console_scripts': [
             'dell_start_client=client.consoleClient:main',
             'dell_start_server=server.api.RestApiApp:main'],
    },
    install_requires=install_requires_list
)