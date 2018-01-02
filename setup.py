from setuptools import setup

setup(name='python-broadlink',
      version='0.1',
      description='A simple Python API for controlling IR controllers from Broadlink',
      url='https://github.com/mjg59/python-broadlink',
      author='Matthew Garrett',
      license='MIT',
      packages=['python-broadlink'],
      install_requires=[
          'pycrypto','netaddr'
      ],
      dependency_links=['https://github.com/mjg59/python-broadlink.git'],
      zip_safe=False)
