from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in qp_validateconnection/__init__.py
from qp_validateconnection import __version__ as version

setup(
	name='qp_validateconnection',
	version=version,
	description='Vaidate connection',
	author='Rafael Licett',
	author_email='rafael.licett@mentum.group',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
