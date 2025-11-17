from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in electronic_invoice/__init__.py
from electronic_invoice import __version__ as version

setup(
	name="electronic_invoice",
	version=version,
	description="sales invoice with QRCode",
	author="mariam",
	author_email="eng.mariam87@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
